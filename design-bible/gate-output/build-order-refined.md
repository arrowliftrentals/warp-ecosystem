# Integration Gate — Refined Build Order

| Field | Value |
|---|---|
| **Doc ID** | `DB-G01-003` |
| **Name** | Phase 1 Refined Build Order |
| **Purpose** | Refined dependency-driven build sequence based on actual Phase 1 interface contracts |
| **Owner** | Design Bible / Integration Gate |
| **Status** | `active` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Integration Gate Agent |
| **Version** | v1 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## Comparison with Volume 0 Section 13

Volume 0 defines 7 tiers (0-6+). Phase 1 analysis reveals the following adjustments needed:

**Change 1: Governance (Vol 9) must be Tier 0, not Tier 4.**
Volume 0 placed full governance at Tier 4. But Vol 9's DecisionValidator and the GovernedOutput pass-through stub are required from the first line of code per P1 and P9. The graduated strategy (Vol 9 B.1) correctly identifies this: 3 hard rules at Tier 0, full pipeline at Tier 4. The build order must reflect this split.

**Change 2: Memory (Vol 1) and Core Loop (Vol 2) can develop in parallel at Tier 2.**
Volume 0 sequences Memory (Tier 3) after Core Loop (Tier 2). But the core loop needs memory from the start (session management, message storage). Vol 2's `MemoryContextRetriever` directly depends on Vol 1. Building them in parallel with the memory façade interface defined first allows both to progress.

**Change 3: Tool infrastructure (Vol 10) moves to Tier 2.**
Volume 0 places all tools at Tier 6+. But the conversation engine's ReAct loop requires `ToolRegistry.execute()` to function. Core tools (file, git, memory, web) are needed for MVA-1 (a coherent response often requires tool use). Tool infrastructure should be Tier 2 alongside the core loop.

**Change 4: Console (Vol 7) can start at Tier 2 for the chat panel.**
Volume 0 places Console at Tier 6+. But the chat panel depends only on stable API contracts (`POST /v1/atlas/chat`). Once Tier 1 establishes the health endpoint and Tier 2 establishes the chat endpoint, the console chat panel can begin. Dashboard views follow later.

---

## Refined Build Order

### Tier 0: Foundation (no dependencies)
**Subsystems:** `shared/` (errors, config, logging, types, llm)
**Files:** `shared/errors.py`, `shared/config.py`, `shared/logging.py`, `shared/types.py`, `shared/llm.py`
**Owner:** Cross-cutting (Vol 8 owns errors/config, shared ownership for rest)
**Gate:** `ruff` + `mypy` pass on all shared files. Import from any module works.
**MVA:** None.
**Difference from Vol 0:** Identical.

### Tier 1: Skeleton (depends on Tier 0)
**Subsystems:** API server + health endpoint + governance stubs
**Files:**
- `api/server.py` — FastAPI app factory, startup/shutdown (Vol 8)
- `api/middleware.py` — timeout, error handler, request logging (Vol 8)
- `api/routes/health.py` — `/health` endpoint (Vol 8)
- `governance/validator.py` — DecisionValidator stub (always returns SAFE) (Vol 9)
- `governance/schemas.py` — GovernedOutput, AuthorityLevel, ValidationDecision (Vol 9)
- `governance/output.py` — AnswerGovernor stub (pass-through, authority_level=ADVISORY) (Vol 9)
**Gate:** Server boots in <3s. `/health` returns 200. `ruff` + `mypy` pass.
**MVA:** None (MVA-5 partially — server boots without errors).
**Difference from Vol 0:** Added governance stubs. Vol 0 Tier 1 had only server + validator. Governance schemas must exist here because ConversationResponse (Tier 2) references GovernedOutput.

### Tier 2: Core Loop + Memory + Tools (depends on Tier 0, 1)
**Subsystems:** Orchestrator, Memory, Tool Registry (core tools)
**Files:**
- `memory/schemas.py` — all memory Pydantic schemas (Vol 1)
- `memory/manager.py` — MemoryManager facade (Vol 1)
- `memory/l1_working.py` through `memory/l10_vector.py` — all 10 layers (Vol 1)
- `memory/connection_manager.py`, `memory/consolidation.py` (Vol 1)
- `orchestrator/engine.py` — ConversationEngine (Vol 2)
- `orchestrator/intent.py` — IntentParser (3-tier) (Vol 2)
- `orchestrator/response.py` — ResponseGenerator + ReAct (Vol 2)
- `orchestrator/personality.py` — PersonalityManager (Vol 2)
- `orchestrator/memory_context.py` — MemoryContextRetriever (Vol 2)
- `tools/registry.py` — ToolRegistry (Vol 10)
- `tools/schemas.py` — ToolDefinition, ToolResult (Vol 10)
- `tools/file.py`, `tools/git.py`, `tools/memory.py`, `tools/web.py`, `tools/system.py`, `tools/conversation.py` — core tools (Vol 10)
- `api/routes/chat.py` — `/v1/atlas/chat` with SSE streaming (Vol 8)
- `contracts/api_schemas.py` — ChatRequest, ChatResponse, EvidenceRef (Vol 8)
**Gate:** **MVA-1 passes** — send `{"query": "hello"}` to `/v1/atlas/chat`, receive coherent response within 5s. **MVA-3 passes** — store a fact, retrieve it in later query. **MVA-5 passes** — server boots with zero errors, health reports accurate status.
**Difference from Vol 0:** Merged Vol 0 Tiers 2 (Core Loop) and 3 (Memory) into one tier because they are mutually dependent. Added tool infrastructure (was Tier 6+ in Vol 0) because ReAct loop requires it.

### Tier 3: Output Governance (depends on Tier 2)
**Subsystems:** Full governance pipeline
**Files:**
- `governance/output.py` — AnswerGovernor full implementation (Vol 9)
- `governance/claims.py` — ClaimExtractor (Vol 9)
- `governance/confidence.py` — ConfidenceModel (Vol 9)
- `governance/evidence.py` — EvidenceStore (Vol 9)
- `governance/contracts.py` — EvidenceContractRegistry (Vol 9)
**Gate:** **MVA-2 passes** — factual question receives evidence-grounded response, not hallucinated.
**Difference from Vol 0:** Moved from Tier 4 to Tier 3. The governance pipeline is the enforcement of P9 and must be active before learning or self-modification are added.

### Tier 4: Learning (depends on Tier 2, 3)
**Subsystems:** Active learning, correction pipeline, retraining
**Files:**
- `learning/active_learner.py` — correction collection (Vol 3)
- `learning/model_trainer.py` — retraining pipeline (Vol 3)
- `learning/model_registry.py` — model version management (Vol 3)
- `learning/effectiveness_tracker.py` — A/B testing (Vol 3)
- `learning/outcome_detector.py` — implicit signals (Vol 3)
- `learning/retrain_triggers.py` — trigger detection (Vol 3)
- `learning/feedback_processor.py` — feedback handling (Vol 3)
- `learning/learning_manager.py` — facade (Vol 3)
- `learning/pattern_learner.py` — behavioral patterns (Vol 3)
- `learning/statistical_analysis.py` — hypothesis testing (Vol 3)
- `learning/schemas.py`, `learning/errors.py` (Vol 3)
- `learning/content_ingester.py`, `learning/domain_classifier.py`, `learning/domain_tool_router.py`, `learning/knowledge_synthesizer.py`, `learning/contradiction_detector.py` — knowledge pipeline (Vol 3)
- `learning/extractors/base.py`, `learning/extractors/general.py` (Vol 3)
- `learning/auto_retrain_daemon.py`, `learning/ab_testing.py` (Vol 3)
- `api/routes/learning_feedback.py` — correction endpoint (Vol 8)
**Gate:** **MVA-4 passes** — correct a classification, verify persistence.
**Difference from Vol 0:** Identical intent (Vol 0 Tier 5). Renumbered to Tier 4 due to governance moving earlier.

### Tier 5: Self-Modification (depends on Tier 2, 3, 4)
**Subsystems:** Proposal pipeline, sandbox, verification
**Files:**
- `self_modify/modifier.py` — SelfModifier (Vol 4)
- `self_modify/verification.py` — VerificationTracker (Vol 4)
- `self_modify/monitor.py` — MetaCognitiveMonitor (Vol 4)
- `self_modify/risk.py` — RiskAssessor (Vol 4)
- `self_modify/approval.py` — ApprovalAutomator (Vol 4)
- `self_modify/validation.py` — ValidationOrchestrator (Vol 4)
- `self_modify/api_contracts.py` — APIContractValidator (Vol 4)
- `self_modify/code_analyzer.py` — CodeAnalyzer (Vol 4)
- `self_modify/integrity.py` — IntegrityGuard (Vol 4)
- `self_modify/sandbox/manager.py`, `sandbox/executor.py`, `sandbox/docker_executor.py`, `sandbox/docker_provider.py` (Vol 4)
- `api/routes/sandbox.py`, `api/routes/proposals.py` (Vol 8)
**Gate:** Submit a code change proposal, verify it runs in sandbox, verify cryptographic proof stored in L4.
**Difference from Vol 0:** Vol 0 placed self-modification at Tier 6+. Elevated to Tier 5 because it is a moat capability (Section 3.2) and the pipeline depends on learning (Tier 4) for outcome recording.

### Tier 6+: Capabilities (parallel, depends on Tier 2-5 as noted)
**Intelligence (Vol 5):** IntelligenceCoordinator, AnalogicalReasoner, HypothesisGenerator, SocraticChallenger, GrowthTracker. Depends on Tier 2 (memory), Tier 4 (learning provides RefinedKnowledge).
**Voice (Vol 6):** VoiceController, PiperTTS, TextNormalizer, STT stub, voice schemas, voice API routes. Depends on Tier 2 (orchestrator), Tier 3 (governance for GovernedOutput).
**Console (Vol 7):** Full dashboard, memory view, goals view, tasks view, 3D visualization. Chat panel can start at Tier 2; full console at Tier 6+.
**Extended Tools (Vol 10):** STEM backends, security tools, screen control, email/calendar/messaging. Depends on Tier 2 (tool registry) + domain-specific subsystems.

---

## Dependency DAG Validation

```
Tier 0 (shared)
  ↓
Tier 1 (server + governance stubs)
  ↓
Tier 2 (memory + orchestrator + core tools + chat endpoint)
  ↓
Tier 3 (full governance pipeline)
  ↓
Tier 4 (learning)
  ↓
Tier 5 (self-modification)
  ↓
Tier 6+ (intelligence, voice, console dashboard, extended tools)
```

No cycles. Each tier depends only on previous tiers. Tier 6+ items are independent of each other and can proceed in parallel.

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Integration Gate Agent | Initial creation — 7-tier build order refined from Phase 1 analysis with 4 changes from Volume 0: governance moved earlier, memory/orchestrator merged, tools elevated, console chat panel earlier | Created the refined build sequence showing exactly what to build in what order based on actual dependency analysis |
