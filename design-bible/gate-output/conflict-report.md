# Integration Gate — Conflict Report

| Field | Value |
|---|---|
| **Doc ID** | `DB-G01-001` |
| **Name** | Phase 1 + Phase 2 Conflict Report |
| **Purpose** | Exhaustive inventory of cross-volume conflicts detected during Integration Gate review (Phase 1 B.1-B.4 + Phase 2 B.5-B.13) |
| **Owner** | Design Bible / Integration Gate |
| **Status** | `active` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Integration Gate Agent |
| **Version** | v2 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-11 |

---

## Conflict Inventory

### C-01: Governance Schema Ownership (Vol 1 vs Vol 9)
**What:** GovernedOutput, ExtractedClaim, EvidenceItem, EvidenceContract, AuthorityLevel, ClaimType, ClaimStatus, OutputPhase are governance-domain schemas currently co-located in `src/memory/schemas.py` (Vol 1 territory). Vol 9 claims ownership. Vol 1's pre-registered rule says it owns "all Pydantic schemas for data entering/leaving memory layers."
**Volumes:** 1 vs 9
**Evidence:**
- Vol 1 B.3.3: "Governance-related schema families currently present in this file … Boundary decision for rebuild: keep only Volume 1 memory schemas in this module; move governance/learning/librarian/orchestrator-specific schema families to owning volumes."
- Vol 9 B.4 item 7: "GovernedOutput, ExtractedClaim … should be extracted to a governance-owned schema file."
- AGENT_COMM.md pre-registered: "Volume 1 (Memory) — All Pydantic schemas for data entering/leaving memory layers are defined by Volume 1."
**Recommended resolution:** GovernedOutput et al. are output governance schemas, NOT data entering memory layers. Extract to `governance/schemas.py` owned by Vol 9. Vol 1 retains memory-storage schemas (WorkingMemoryItem, Message, Episode, Fact, etc.). The pre-registered rule applies to data-at-rest schemas, not egress governance schemas.
**Status:** resolved
**Resolution:** Approved as recommended. Vol 9 owns governance schemas. Vol 1 owns data-at-rest schemas.

### C-02: Knowledge-Pipeline Schema Location (Vol 1 vs Vol 3)
**What:** Knowledge-pipeline Pydantic schemas (NormalizedContent, ExtractionResult, DomainClassification, RefinedKnowledge, SynthesizedKnowledge, DomainKnowledgeEntry, ContradictionResult, ConflictType, etc.) are currently in `src/memory/schemas.py` (Vol 1) but are knowledge-pipeline-specific.
**Volumes:** 1 vs 3
**Evidence:**
- AGENT_COMM.md conflict flag: "Knowledge-pipeline Pydantic schemas … are currently in src/memory/schemas.py owned by Volume 1, but they are knowledge-pipeline-specific, not memory-specific."
- Vol 3 B.3 cross-volume summary: "Consumes from Volume 1 (Memory): … NormalizedContent, ContentType, DomainClassification…"
- Vol 1 B.4 scope notes: "APEX prompt strategy schema family belongs to Volume 3/5 boundary."
**Recommended resolution:** Schemas consumed exclusively by the learning pipeline should move to `learning/schemas.py` (Vol 3). Schemas shared across subsystems (e.g., Fact, OutcomeSignal) stay in Vol 1. A thin re-export in Vol 1 can ease migration.
**Status:** resolved
**Resolution:** Approved as recommended. Learning-specific schemas move to Vol 3. Shared schemas stay in Vol 1.

### C-03: Intelligence Schema Ownership (Vol 1 vs Vol 5)
**What:** StructuralAnalogy, Hypothesis, ResearchGap, SocraticChallenge, IntellectualProfile, CalibratedConfidence, ProvenanceChain are stored in/queried from memory layers (L4, L9, L10) but are semantically intelligence-domain schemas.
**Volumes:** 1 vs 5
**Evidence:**
- AGENT_COMM.md conflict flag: "Volume 1 owns all Pydantic schemas for data entering/leaving memory layers. These schemas … are stored in and queried from memory layers, so they belong to Volume 1."
- Vol 5 B.3: Lists these schemas as "Pydantic Schemas Required (defined by Volume 1 Memory or Volume 5 Intelligence)."
**Recommended resolution:** Since these schemas cross the memory boundary (stored in L4/L9), Vol 1 defines the data schemas per pre-registered rule. Vol 5 consumes them. If Vol 5 needs intelligence-specific fields not relevant to storage, Vol 5 can define extension schemas that compose Vol 1 base schemas.
**Status:** resolved
**Resolution:** Approved as recommended. Vol 1 owns base data schemas. Vol 5 consumes and may extend via composition.

### C-04: cross_layer_linker.py Ownership (Vol 1 vs Vol 3)
**What:** `cross_layer_linker.py` creates connections between memory layers — this is memory infrastructure, not learning.
**Volumes:** 1 vs 3
**Evidence:**
- AGENT_COMM.md conflict: "cross_layer_linker.py creates connections between memory layers — this is memory infrastructure, not learning."
- Vol 3 B.4: "DEFER … Belongs more to Volume 1 (Memory) — flag as potential ownership conflict."
**Recommended resolution:** Assign to Vol 1 (Memory). Cross-layer linking is a MemoryManager responsibility. Vol 3 DEFERs it appropriately.
**Status:** resolved
**Resolution:** Approved as recommended. Vol 1 owns cross-layer linking.

### C-05: hybrid_retriever.py Ownership (Vol 1 vs Vol 3)
**What:** `hybrid_retriever.py` combines FTS5 + FAISS + graph retrieval — this is memory retrieval infrastructure, not learning.
**Volumes:** 1 vs 3
**Evidence:**
- AGENT_COMM.md conflict: "hybrid_retriever.py combines FTS5 + FAISS + graph retrieval — this is memory retrieval infrastructure."
- Vol 3 B.4: "DEFER … Belongs partially to Volume 1 — flag as potential ownership conflict."
**Recommended resolution:** Assign to Vol 1 (Memory). Multi-source retrieval is a memory-layer concern.
**Status:** resolved
**Resolution:** Approved as recommended. Vol 1 owns hybrid retrieval.

### C-06: memory_guard.py Ownership (Vol 1 vs Vol 3 vs Vol 9)
**What:** `memory_guard.py` validates memory operations — governance or memory concern, not learning.
**Volumes:** 1 vs 3 vs 9
**Evidence:**
- AGENT_COMM.md conflict: "Volume 3 KILLs this component. Volume 9 (Governance) or Volume 1 (Memory) should own memory validation if rebuilt."
- Vol 3 B.4: "KILL. Belongs in Volume 1 (Memory) or Volume 9 (Governance), not learning."
**Recommended resolution:** Memory write validation is a boundary enforcement concern — assign to Vol 9 (Governance). Vol 9's DecisionValidator can incorporate memory-write validation rules. Vol 3 correctly KILLs it from its scope.
**Status:** resolved (OVERRIDDEN)
**Resolution:** Overridden — assign to Vol 1 (Memory), not Vol 9. Memory should enforce its own write boundaries via schema validation and a lightweight write guard. Vol 9 governs user-facing output and intent safety, not data layer integrity. Pydantic schema validation at the memory boundary is the primary enforcement mechanism; a thin MemoryWriteGuard in Vol 1 handles any additional constraints.

### C-07: Verification Schema Ownership (Vol 1 vs Vol 4)
**What:** CommandEvidence, ValidationClaim, ValidationClaimType are verification schemas that Vol 4 uses but Vol 1 may own as data-at-rest schemas.
**Volumes:** 1 vs 4
**Evidence:**
- AGENT_COMM.md conflict: "Volume 1 owns schemas (data entering memory). Volume 4 owns behavioral interface (sign, verify, claim)."
- Vol 4 B.3.2: Defines CommandEvidence, ValidationClaim, ValidationClaimType with explicit "Input schemas (from Volume 1 memory schemas)."
**Recommended resolution:** Vol 1 defines the Pydantic schemas (data-at-rest in L4). Vol 4 owns the behavioral methods (sign, verify, claim). This split is already agreed in AGENT_COMM.md.
**Status:** resolved
**Resolution:** Approved as recommended. Data schemas in Vol 1, behavioral methods in Vol 4.

### C-08: OperationalDiagnostician Ownership (Vol 5 vs Vol 8 vs Vol 9)
**What:** OperationalDiagnostician, InvariantEvaluator, RemediationEngine live in `src/intelligence/` but serve infrastructure/governance purposes.
**Volumes:** 5 vs 8 vs 9
**Evidence:**
- AGENT_COMM.md conflict: "OperationalDiagnostician lives in src/intelligence/ but its purpose (health truthfulness checking, data flow analysis, remediation patches) overlaps with Volume 8 (Infrastructure/observability) and Volume 9 (Governance/validation)."
- Vol 5 B.4: "DEFER … System self-diagnostics is infrastructure, not user-facing intelligence."
**Recommended resolution:** Health truthfulness is a governance concern (P4). Move OperationalDiagnostician + InvariantEvaluator to Vol 9 (Governance). RemediationEngine produces code changes — move to Vol 4 (Self-Modification). Vol 5 retains only user-facing amplification components.
**Status:** resolved
**Resolution:** Approved as recommended. Diagnostician + InvariantEvaluator → Vol 9. RemediationEngine → Vol 4. Vol 5 keeps user-facing intelligence only.

### C-09: TTS/STT Voice Logic in Console (Vol 6 vs Vol 7)
**What:** Voice logic (Cartesia/OpenAI TTS/STT) is currently inlined in `ChatPanel.tsx` (Vol 7) but belongs to Vol 6.
**Volumes:** 6 vs 7
**Evidence:**
- AGENT_COMM.md conflict: "Vol 6 owns TTS/STT implementation. Vol 7 extracts inlined Cartesia/OpenAI voice code from ChatPanel.tsx."
- Vol 7 B.2 item 3: ChatPanel "currently inlines TTS/voice logic (Cartesia, OpenAI providers) that must be extracted to Volume 6."
- Vol 6 B.1: "This volume covers audio voice I/O only."
**Recommended resolution:** Vol 6 owns the TTS/STT implementation. Vol 7 extracts the inlined voice code and consumes a clean interface provided by Vol 6 (via REST API or a lightweight JS SDK). Both volumes already agree on this.
**Status:** resolved
**Resolution:** Approved as recommended. Vol 6 owns voice implementation. Vol 7 consumes via API.

### C-10: Endpoint URL Prefix Inconsistency (Vol 7 vs Vol 8)
**What:** Console Vite proxy rewrites `/api/*` but backend uses `/v1/*` natively.
**Volumes:** 7 vs 8
**Evidence:**
- AGENT_COMM.md conflict: "Vol 8 defines the canonical prefix. Console proxy should pass-through /v1/* directly. Eliminate /api prefix in production."
- Vol 7 B.2: "Vite dev server proxies `/api/*` → `http://localhost:8000/*`."
- Vol 8 B.3.3: Canonical chat endpoint is `POST /v1/atlas/chat`.
**Recommended resolution:** Vol 8 owns the canonical prefix (`/v1/*`). Console proxy should rewrite `/v1/*` → `http://localhost:8000/v1/*` (pass-through), not `/api/*`. Remove the `/api` prefix mapping. Both development and production use `/v1/*` consistently.
**Status:** resolved
**Resolution:** Approved as recommended. `/v1/*` everywhere. Kill `/api` prefix.

### C-11: TypeScript Type Generation Ownership (Vol 7 vs Vol 8 vs Vol 9)
**What:** Who owns the Pydantic-to-TypeScript codegen pipeline?
**Volumes:** 7 vs 8 vs 9
**Evidence:**
- AGENT_COMM.md conflict: "Vol 8 (API and Infrastructure) owns the codegen tool and CI step. Vol 9 provides governance schemas as input. Vol 7 consumes the generated output."
- Vol 7 B.3.5: "Generation: A build-time script generates TypeScript interfaces from Pydantic models."
- PROJECT_CONVENTIONS.md Section 1: `contracts/generate_ts_types.py` exists in the project layout.
**Recommended resolution:** Vol 8 owns the codegen tool (`contracts/generate_ts_types.py`) and CI integration. Vol 1, Vol 2, Vol 9, and other volumes provide Pydantic schemas as input. Vol 7 consumes the generated `.ts` types. The tool lives in `contracts/` per PROJECT_CONVENTIONS.md.
**Status:** resolved
**Resolution:** Approved as recommended. Vol 8 owns codegen tool. Schemas are inputs. Vol 7 consumes output.

### C-12: Chat Endpoint Streaming Path (Vol 2 vs Vol 8)
**What:** Vol 2 says "Streaming is a transport concern handled at the API layer (Vol 8), not in the engine" and KILLs `atlas_streaming.py`. Vol 8 defines `POST /v1/atlas/chat/stream` as a separate endpoint. But Vol 7 expects streaming via `POST /v1/atlas/chat` with `Accept: text/event-stream`.
**Volumes:** 2 vs 7 vs 8
**Evidence:**
- Vol 2 B.2: "Streaming is a transport concern handled at the API layer (Vol 8)."
- Vol 8 B.3.4: Defines `POST /v1/atlas/chat/stream` as separate endpoint.
- Vol 7 B.3.1: "POST /v1/atlas/chat with Accept: text/event-stream" — single endpoint, content negotiation.
**Recommended resolution:** Use a single endpoint `POST /v1/atlas/chat` with content negotiation (Accept header) or a `stream` boolean in the request body, as Vol 7 specifies. Do NOT create a separate `/stream` endpoint. This aligns with Vol 2's `ConversationRequest.stream: bool` field.
**Status:** resolved
**Resolution:** Approved as recommended. Single endpoint with `stream: bool` in request body.

### C-13: ConversationResponse vs ChatResponse Schema Name (Vol 2 vs Vol 8)
**What:** Vol 2 defines `ConversationResponse` as the engine output. Vol 8 defines `ChatResponse` as the API response. These are different schemas with overlapping fields.
**Volumes:** 2 vs 8
**Evidence:**
- Vol 2 B.3.1: `ConversationResponse` with fields: session_id, response, intent, evidence_refs, authority_level, confidence, actions_taken, metadata.
- Vol 8 B.3.3: `ChatResponse` with fields: answer, session_id, evidence, tool_calls, governed, metadata.
**Recommended resolution:** `ConversationResponse` (Vol 2) is the internal engine output. `ChatResponse` (Vol 8) is the HTTP response. Vol 8 maps from `ConversationResponse` to `ChatResponse` in the route handler. Field name differences: `response` → `answer`, `evidence_refs` → `evidence`. This mapping is Vol 8's responsibility. Both schemas should be documented in `contracts/api_schemas.py`.
**Status:** resolved
**Resolution:** Approved as recommended. Internal vs HTTP response schemas. Vol 8 owns the mapping.

### C-14: GovernedOutput Supersedes ApprovedUtterance (Vol 6 vs Vol 9)
**What:** GovernedOutput replaces ApprovedUtterance for all output modalities including voice.
**Volumes:** 6 vs 9
**Evidence:**
- AGENT_COMM.md resolved conflict: "GovernedOutput replaces ApprovedUtterance. Volume 6 consumes GovernedOutput from Volume 9."
- Vol 6 B.4: "governance.py — KILL. ApprovedUtterance superseded by Vol 9's unified GovernedOutput."
- Vol 9 B.4 item 11: "KILL. Superseded by GovernedOutput."
**Recommended resolution:** Already resolved. GovernedOutput is the single egress schema. Vol 6 KILLs `governance.py` and consumes Vol 9's GovernedOutput.
**Status:** resolved

### C-15: enforcement_orchestrator.py Ownership (Vol 4 vs Vol 9)
**What:** enforcement_orchestrator.py and enforcement_state.py are in Vol 9's A.2 manifest but implement self-modification enforcement.
**Volumes:** 4 vs 9
**Evidence:**
- AGENT_COMM.md resolved conflict: "Volume 4 owns enforcement_orchestrator.py and enforcement_state.py. Volume 9 governs the DECISION; Volume 4 owns the EXECUTION."
- Vol 9 B.4 item 12: "KILL from Volume 9 scope … Self-modification security belongs to Volume 4."
**Recommended resolution:** Already resolved. Vol 4 owns execution enforcement. Vol 9 owns validation decisions.
**Status:** resolved

### C-16: Error Taxonomy Location (Vol 8 vs all consumers)
**What:** PROJECT_CONVENTIONS.md specifies `shared/errors.py`. Attempt 3 has `src/errors.py` at top level.
**Volumes:** 8 vs all
**Evidence:**
- AGENT_COMM.md resolved conflict: "Follow PROJECT_CONVENTIONS.md: atlas/shared/errors.py."
**Recommended resolution:** Already resolved. `atlas/shared/errors.py` per PROJECT_CONVENTIONS.md.
**Status:** resolved

### C-17: Chat Request Field Name (Vol 2 vs Vol 7 vs Vol 8)
**What:** The chat endpoint request field should be `query` (not `message` or `command`).
**Volumes:** 2 vs 7 vs 8
**Evidence:**
- AGENT_COMM.md resolved conflict: "Field name is 'query' everywhere."
- Vol 8 B.3.3: `ChatRequest.query`.
- Vol 2 B.3.1: `ConversationRequest.query`.
**Recommended resolution:** Already resolved. Field name is `query` everywhere.
**Status:** resolved

---

## Phase 2 Conflicts (B.5-B.13)

### C-18: process_query vs process_message Naming (Vol 2 vs Vol 6 vs Vol 8)
**What:** Vol 6 B.3 references `OrchestratorEngine.process_query(query, session_id)`. Vol 8 B.6 maps `ChatRequest.query → ConversationEngine.process_message(message, session_id, device_id)`. Class name (OrchestratorEngine vs ConversationEngine) and method name (process_query vs process_message) both differ.
**Volumes:** 2 vs 6 vs 8
**Evidence:**
- Vol 6 B.3: `OrchestratorEngine.process_query(query: str, session_id: str) -> str`
- Vol 8 B.6: Maps `ChatRequest.query` to `ConversationEngine.process_message(message=query, ...)`
- Vol 2 B.3.1: `ConversationEngine.process_message(message, session_id, device_id)`
**Recommended resolution:** Vol 2 owns the canonical name: `ConversationEngine.process_message()`. Vol 6 must update its B.3 dependency reference from `OrchestratorEngine.process_query()` to `ConversationEngine.process_message()`. Vol 8 mapping is correct.
**Status:** resolved
**Resolution:** Approved as recommended. `ConversationEngine.process_message()` is canonical. Vol 6 updates its reference.

### C-19: IntellectualProfile as First-Class L9 Field (Vol 1 vs Vol 5)
**What:** Vol 5 B.10 L-INT-05 requires IntellectualProfile to become a first-class field on the L9 UserProfile schema (currently nested in `metadata['intellectual_profile']`). This requires Vol 1 to add the field.
**Volumes:** 1 vs 5
**Evidence:**
- Vol 5 B.10 L-INT-05: "Rebuild should make IntellectualProfile a first-class field on L9 UserProfile schema."
- Vol 5 B.13 criterion 9: Deducted 1pt noting "IntellectualProfile L9 field needs Vol 1 change."
- Vol 1 B.6: UserProfile schema does not currently include IntellectualProfile as a field.
**Recommended resolution:** Vol 1 adds `intellectual_profile: IntellectualProfile | None = None` to the L9 UserProfile schema when Vol 5 is built (Phase 4). Not blocking for Tier 0-3.
**Status:** resolved
**Resolution:** Approved as recommended. Deferred to Phase 4. Vol 1 will add the field when Vol 5 begins implementation.

### C-20: Governance Schema Migration Path (Vol 1 → Vol 9)
**What:** Vol 9 B.6 specifies all governance schemas live in `governance/schemas.py`. But these schemas currently reside in `src/memory/schemas.py` (Vol 1). C-01 resolved ownership but the migration path and timing are unspecified.
**Volumes:** 1 vs 9
**Evidence:**
- C-01 resolution: "Vol 9 owns governance schemas. Vol 1 owns data-at-rest schemas."
- Vol 9 B.6: "All governance Pydantic schemas live in `atlas/governance/schemas.py` per C-01 resolution."
- Vol 9 B.3 Dependency 1: Acknowledges schemas "currently defined in `src/memory/schemas.py` owned by Volume 1."
**Recommended resolution:** During Tier 0 implementation, create `governance/schemas.py` with Vol 9's schema definitions. Vol 1 removes governance schemas from its file. No re-export needed — all consumers import from `governance/schemas.py` directly. This must happen as the first coordination step.
**Status:** resolved
**Resolution:** Approved as recommended. Tier 0 task: create governance schema file, update all imports.

### C-21: OperationalDiagnostician Implementation Approach (Vol 5 vs Vol 9)
**What:** Vol 5 B.11 D-INT-04 transfers OperationalDiagnostician to Vol 9 as a standalone component per C-08. Vol 9 B.12 plans to absorb it into DecisionValidator at Tier 4+ rather than maintaining it as a separate component.
**Volumes:** 5 vs 9
**Evidence:**
- Vol 5 B.11 D-INT-04: "Move diagnostician + evaluator to Vol 9 (Governance)."
- Vol 9 B.12: "Incorporate health truthfulness validation into DecisionValidator as a Tier 4+ feature, not as a separate component."
- C-08 resolution: "Diagnostician + InvariantEvaluator → Vol 9."
**Recommended resolution:** Vol 9 owns the capability (per C-08). The implementation approach (standalone vs. absorbed into DecisionValidator) is Vol 9's decision. Vol 9's absorption approach is preferred — fewer components, less maintenance. Vol 5 does not need to specify the implementation form.
**Status:** resolved
**Resolution:** Approved as recommended. Vol 9 absorbs diagnostics into DecisionValidator at Tier 4+.

### C-22: Undocumented SSE Event Types (Vol 2 vs Vol 7 vs Vol 8)
**What:** Vol 7 B.11 D7 identifies `engagement_step` and `implementation_event` SSE event types consumed by the console but not documented in Vol 2 or Vol 8 shared contracts. Vol 8 B.6 defines 6 SSE event types (THINKING, TOOL_CALL, TOOL_RESULT, CHUNK, DONE, ERROR) — the two extra types are not listed.
**Volumes:** 2 vs 7 vs 8
**Evidence:**
- Vol 7 B.11 D7: "The SSE parser in ChatPanel.tsx handles engagement_step and implementation_event event types … not documented in any backend API spec."
- Vol 8 B.6: StreamEvent type field is `Literal["THINKING", "TOOL_CALL", "TOOL_RESULT", "CHUNK", "DONE", "ERROR"]` — only 6 types.
**Recommended resolution:** Decide at implementation time: (a) if these event types are needed in the rebuild, add them to Vol 8's StreamEvent Literal type and document in shared-contracts.md, or (b) if they are Attempt 3 artifacts, remove support from the console SSE parser. The programming agent should ask Vol 2 whether the orchestrator produces these events.
**Status:** resolved
**Resolution:** Deferred to programming agent. If the orchestrator produces these events, Vol 8 must document them. If not, Vol 7 removes support.

### C-23: ChatResponse Field Rename Contract (Vol 2 vs Vol 8)
**What:** Vol 8 B.6 documents a field rename from `ConversationResponse.response` (Vol 2) to `ChatResponse.answer` (Vol 8). This transform is documented locally in Vol 8 but not in shared-contracts.md as a binding agreement.
**Volumes:** 2 vs 8
**Evidence:**
- Vol 8 B.6: "Mapping responsibility: Route handler maps ConversationResponse (Vol 2) → ChatResponse (Vol 8). Field renames: response → answer, evidence_refs → evidence."
- shared-contracts.md Section 2.1: Does not specify the field rename mapping.
**Recommended resolution:** Add the mapping to shared-contracts.md Section 2.1 as a binding contract. Vol 8 owns the mapping; Vol 2 and Vol 7 must be aware of the field names they produce/consume.
**Status:** resolved
**Resolution:** Approved as recommended. Added to shared-contracts.md Section 6 (new section).

### C-24: Speculation Scrubbing Ownership (Vol 0 vs Vol 5 vs Vol 9)
**What:** Vol 9 B.11.1 identifies speculation scrubbing (`_scrub_speculation` regex replacements) as a system-wide concern, recommending promotion to `shared/text.py`. Vol 5 has its own text processing. No volume claims ownership of `shared/text.py`.
**Volumes:** 0 vs 5 vs 9
**Evidence:**
- Vol 9 B.11.1: "Speculation scrubbing … applicable to ALL LLM-generated text in the system. Candidate for promotion to Volume 0 as a shared utility."
- Vol 5 B.11 D-INT-02: "Two-layer contradiction detection pattern is reusable. Recommend promoting to atlas/shared/text.py."
**Recommended resolution:** Vol 8 (Infrastructure) owns `shared/` modules per its ownership of `shared/errors.py` and `shared/config.py`. Create `shared/text.py` with speculation scrubbing (from Vol 9) and two-layer contradiction detection (from Vol 5). Vol 8 owns the file; Vol 9 and Vol 5 contribute the implementations.
**Status:** resolved
**Resolution:** Approved as recommended. Vol 8 owns shared/text.py. Vol 9 and Vol 5 contribute utilities.

### C-25: Tool Result → EvidenceStore Integration Path (Vol 2 vs Vol 9 vs Vol 10)
**What:** After tool execution, results must be stored in EvidenceStore (Vol 9) for claim grounding. Vol 10 produces ToolResult, Vol 2 orchestrates the tool call, and Vol 9 owns EvidenceStore. The responsibility chain (who calls `EvidenceStore.store()`) is implicit.
**Volumes:** 2 vs 9 vs 10
**Evidence:**
- Vol 10 B.12 Q4: "Vol 10's ToolResult is the input … Vol 10 does not call EvidenceStore directly; Vol 2 does."
- Vol 9 B.3 Contract 3: `EvidenceStore.store(tool_name, args, result) → EvidenceItem` consumed by Vol 2.
- shared-contracts.md Section 2.7: Vol 9 provides EvidenceStore, Vol 2 consumes.
**Recommended resolution:** Vol 2 (Orchestrator) calls `EvidenceStore.store()` after each tool execution in the ReAct loop. Vol 10 returns `ToolResult` to Vol 2. Vol 2 extracts `tool_name`, `arguments`, and `result` from ToolResult and passes them to EvidenceStore. This is already documented in shared-contracts.md Section 2.7 — no code change needed, just explicit acknowledgment.
**Status:** resolved
**Resolution:** Approved as documented. Vol 2 is the integration point. Already contracted in shared-contracts.md 2.7.

---

## Summary
- **Total conflicts:** 25 (17 Phase 1 + 8 Phase 2)
- **Open:** 0
- **Resolved:** 25 (all)
- **Overridden:** 1 (C-06 — memory_guard assigned to Vol 1 instead of Vol 9)
- **User action required:** None — all conflicts resolved. Implementation may proceed.

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Integration Gate Agent | Initial creation — 17 conflicts identified (13 open, 4 already resolved) across schema ownership, component boundaries, endpoint conventions, and naming | Created the master list of disagreements between subsystem designs that must be resolved before coding begins |
| v2 | 2026-03-11 | Integration Gate Agent (Final Review) | Added 8 Phase 2 conflicts (C-18 through C-25) covering naming mismatches, schema migration, undocumented events, field rename contracts, shared utility ownership, and tool-evidence integration path — all resolved | Added new disagreements found during the deep-dive design sections and resolved them all |
