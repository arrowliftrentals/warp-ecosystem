# Integration Gate — Refined MVA

| Field | Value |
|---|---|
| **Doc ID** | `DB-G01-004` |
| **Name** | Phase 1 Refined MVA |
| **Purpose** | Refined Minimum Viable Atlas acceptance criteria based on Phase 1 interface contract analysis |
| **Owner** | Design Bible / Integration Gate |
| **Status** | `active` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Integration Gate Agent |
| **Version** | v1 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## Changes from Volume 0 Section 12

### MVA-1: Basic Conversation — MODIFIED
**Original:** Send `{"query": "hello"}` to `POST /v1/atlas/chat`. Receive coherent, personality-consistent response within 5 seconds.
**Refined:** Same, plus:
- Response must be a valid `ChatResponse` (Pydantic-validated per Vol 8 B.3.3).
- Response must include `session_id` (proves session management works).
- Response must include `governed: true` (proves governance pass-through is wired, even if stub).
- Intent must be parseable by symbolic parser (no LLM required for "hello").
**Justification:** Phase 1 revealed that Vol 2's ConversationEngine returns `ConversationResponse`, which Vol 8 maps to `ChatResponse`. The acceptance test must validate the full pipeline including schema mapping and governance stub.

### MVA-2: Evidence-Grounded Response — MODIFIED
**Original:** Send a factual question. Receive a response that cites specific evidence rather than hallucinating.
**Refined:** Same, plus:
- Response `evidence` list must be non-empty (at least one `EvidenceRef`).
- Each `EvidenceRef.source` must correspond to a real tool call or memory retrieval.
- `authority_level` field (from GovernedOutput) must be GROUNDED or ADVISORY, not SPECULATIVE.
- Test query: "What memory layers does Atlas have?" — answer must reference L1-L10 from memory retrieval, not LLM training data.
**Justification:** Vol 9's governance pipeline (AnswerGovernor) is the mechanism that produces evidence-grounded responses. The test must verify the full claim extraction → evidence grounding → confidence scoring pipeline.

### MVA-3: Memory Round-Trip — UNCHANGED
**Original:** Store a fact via conversation. In a later query, ask about that fact. Verify the system retrieves it from memory.
**Refined:** Same. Additionally:
- The stored fact must persist in L4 declarative memory (verifiable via `GET /v1/memory/layers/l4`).
- The retrieval query must show the fact in `evidence` list, proving it came from memory, not LLM.
**Justification:** Vol 1's memory system is the foundation. This test proves L4 write + read works end-to-end through the conversation loop.

### MVA-4: Learning Round-Trip — UNCHANGED
**Original:** Correct a wrong classification. Issue the correction. In a subsequent identical query, verify the classification is now correct.
**Refined:** Same. Additionally:
- The correction must be recorded via `ActiveLearner.record_correction()` (Vol 3).
- The correction must persist across server restart (stored in L5 procedural memory, not just in-memory).
- If retraining threshold is not yet met, the correction must still influence classification via the correction lookup path.
**Justification:** Vol 3's learning pipeline has two paths: immediate correction lookup and full retraining. The MVA test must work via the immediate path (threshold not met after one correction).

### MVA-5: Server Health — MODIFIED
**Original:** Server boots with zero errors. `GET /health` returns all initialized subsystems as healthy.
**Refined:** Same, plus:
- Health response must conform to `HealthResponse` schema (Vol 8 B.3.2).
- Every subsystem reported as `healthy=True` must pass a functional check (R5 — no stubs claiming healthy).
- Subsystems that are not yet built must report `status="disabled"`, not `status="ok"`.
- Boot time must be under 3 seconds (Vol 8 B.1).
- Zero `except: pass` blocks in the codebase (P5, A4).
**Justification:** Attempt 3's health endpoint reported stubs as healthy (A2 anti-pattern). The refined test explicitly validates R5 honest health reporting.

### MVA-6: Output Governance Gate — NEW
**What:** Send a query that requires tool use (e.g., "Read the file README.md"). Verify the response includes evidence references tied to the tool execution. Then send a query where the LLM might hallucinate (e.g., "What is my favorite programming language?"). Verify the response is flagged as SPECULATIVE or includes a disclaimer, not stated as fact.
**Justification:** Vol 9's output governance pipeline (P9) is a core rebuild principle. No dedicated MVA tested it in Volume 0. This test validates the claim extraction → grounding → confidence pipeline end-to-end. It addresses the single biggest failure mode from Attempt 3: ungoverned LLM output.
**Tier gate:** Tier 3.

### MVA-7: Console Chat — NEW
**What:** Open the console in a browser. Type a message. Receive a streamed response with visible thinking steps and tool calls. Verify the response renders correctly with markdown formatting.
**Justification:** The console (Vol 7) is the user's primary interaction surface. Volume 0 does not have a dedicated console acceptance test, but R8 (observable and debuggable) requires the console to work. This test proves the SSE streaming pipeline (Vol 8 → Vol 7) and the chat panel rendering work end-to-end.
**Tier gate:** Tier 2 (chat panel starts at Tier 2 per refined build order).

---

## MVA Summary

| MVA | Description | Tier Gate | Status |
|---|---|---|---|
| MVA-1 | Basic conversation with schema validation | Tier 2 | Modified |
| MVA-2 | Evidence-grounded response | Tier 3 | Modified |
| MVA-3 | Memory round-trip | Tier 2 | Minor additions |
| MVA-4 | Learning round-trip | Tier 4 | Minor additions |
| MVA-5 | Server health with honest reporting | Tier 2 | Modified |
| MVA-6 | Output governance gate | Tier 3 | **New** |
| MVA-7 | Console chat with streaming | Tier 2 | **New** |

All 7 MVAs must pass for Atlas v4 to be called a working system. MVA-6 and MVA-7 were added because Phase 1 revealed that output governance and console interaction are critical paths that lacked explicit acceptance criteria.

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Integration Gate Agent | Initial creation — refined 5 original MVAs with stricter validation criteria, added 2 new MVAs (output governance gate, console chat) based on Phase 1 findings | Updated the finish-line tests to be more rigorous and added two new tests that were missing from the original plan |
