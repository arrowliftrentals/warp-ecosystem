# ATLAS Design Bible — Volume 2: Orchestrator & Conversation Loop

| Field | Value |
|---|---|
| **Doc ID** | `DB-V02-001` |
| **Name** | Volume 2: Orchestrator & Conversation Loop |
| **Purpose** | Design specification for the central conversation engine — intent parsing, routing, response generation, and personality |
| **Owner** | Design Bible / Volume 2 |
| **Status** | `draft` (scaffold — Part A pre-loaded, Part B awaiting distillation agent) |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / TBD distillation agent (Part B) |
| **Version** | v3 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## Part A: Context (Pre-loaded)

### A.1 Subsystem Identity
- **Volume 2: Orchestrator & Conversation Loop**
- **Purpose:** The central brain that receives user input, parses intent, coordinates subsystems, generates responses, and returns output. This is the conversation loop — R1 from Volume 0.
- **Rebuild phase:** Phase 0 (the very first thing built). The conversation loop is the skeleton everything hangs on.

### A.2 Source Manifest

**Code files to read** (paths relative to `atlas/`):

*Core orchestration:*
- `src/orchestrator/atlas.py` — main orchestrator class (~2800+ lines)
- `src/orchestrator/atlas_handlers.py` — intent-specific handlers
- `src/orchestrator/atlas_command_router.py` — command routing
- `src/orchestrator/atlas_llm.py` — LLM integration
- `src/orchestrator/atlas_streaming.py` — streaming response handling
- `src/orchestrator/react_engine.py` — ReAct reasoning loop
- `src/orchestrator/intent_router.py` — intent classification routing
- `src/orchestrator/intent_predictor.py` — predictive intent

*Response pipeline:*
- `src/orchestrator/answer_governor.py` — output governance (ADR-0031)
- `src/orchestrator/claim_extractor.py` — factual claim extraction
- `src/orchestrator/confidence_model.py` — evidence-based confidence
- `src/orchestrator/evidence_store.py` — verbatim evidence storage
- `src/orchestrator/evidence_contracts.py` — evidence requirements
- `src/orchestrator/response_validator.py` — response validation
- `src/orchestrator/response_formatter.py` — response formatting
- `src/orchestrator/prompt_builder.py` — prompt construction
- `src/orchestrator/prompt_constants.py` — prompt templates
- `src/orchestrator/prompts.py` — additional prompts

*Intent system:*
- `src/intent/parser.py` — symbolic intent parser
- `src/intent/grammar.py` — intent grammar definitions
- `src/intent/bert_classifier.py` — BERT-based classification
- `src/intent/hybrid_parser.py` — hybrid symbolic+ML parsing
- `src/intent/llm_classifier.py` — LLM fallback classifier
- `src/intent/entities.py` — entity extraction
- `src/intent/unified.py` — unified intent interface
- `src/intent/decision_validator.py` — validation (shared with Vol 9)

*Personality & proactive:*
- `src/orchestrator/personality_loader.py` — personality from config
- `src/orchestrator/personality_models.py` — personality data models
- `src/orchestrator/personalization.py` — user-adaptive behavior
- `src/orchestrator/proactive_component.py` — proactive suggestions
- `src/orchestrator/proactive_engine.py` — proactive reasoning
- `src/orchestrator/proactive_executor.py` — proactive execution

*Context & state:*
- `src/orchestrator/memory_context.py` — memory retrieval for context
- `src/orchestrator/confirmation_manager.py` — user confirmation flows
- `src/orchestrator/error_recovery.py` — error recovery
- `src/orchestrator/services.py` — service initialization

*Autonomous:*
- `src/orchestrator/autonomous_executor.py` — autonomous task execution
- `src/orchestrator/autonomous_task_manager.py` — task lifecycle
- `src/orchestrator/agent_loop.py` — agent reasoning loop

*Other orchestrator files:*
- `src/orchestrator/architecture_discovery.py`
- `src/orchestrator/assessment_manager.py`
- `src/orchestrator/awareness_cache.py`
- `src/orchestrator/background_control.py`
- `src/orchestrator/benchmark_fetcher.py`
- `src/orchestrator/codebase_awareness.py`
- `src/orchestrator/cognitive_fabric.py`
- `src/orchestrator/comparative_analyzer.py`
- `src/orchestrator/critical_assessments.py`
- `src/orchestrator/degradation_matrix.py`
- `src/orchestrator/dynamic_assessment.py`
- `src/orchestrator/external_apis.py`
- `src/orchestrator/file_resolver.py`
- `src/orchestrator/git_state_provider.py`
- `src/orchestrator/goal_manager.py`
- `src/orchestrator/initiative_engine.py`
- `src/orchestrator/integration_bridge.py`
- `src/orchestrator/intelligence_integration.py`
- `src/orchestrator/interrupted_tasks.py`
- `src/orchestrator/live_exercise_runner.py`
- `src/orchestrator/market_analyzer.py`
- `src/orchestrator/meta_assessment.py`
- `src/orchestrator/meta_assessment_v2.py`
- `src/orchestrator/meta_assessment_v3.py`
- `src/orchestrator/meta_diff.py`
- `src/orchestrator/meta_storage.py`
- `src/orchestrator/ml_training_analyzer.py`
- `src/orchestrator/narrative_generator.py`
- `src/orchestrator/pending_actions.py`
- `src/orchestrator/policy_engine.py`
- `src/orchestrator/presence_detector.py`
- `src/orchestrator/resource_manager.py`
- `src/orchestrator/scheduler.py`
- `src/orchestrator/task_decomposition.py`
- `src/orchestrator/telemetry_bridge.py`
- `src/orchestrator/tool_registry.py`
- `src/orchestrator/tool_schemas.py`
- `src/orchestrator/verified_orchestrator.py`

**Documentation to read:**
- `docs/architecture/react-engine.md`
- `docs/architecture/answer-governor.md`
- `docs/architecture/claim-extractor.md`
- `docs/architecture/confidence-model.md`
- `docs/architecture/evidence-store.md`
- `docs/architecture/evidence-contracts.md`
- `docs/architecture/intent-router.md`
- `docs/architecture/intent-predictor.md`
- `docs/architecture/atlas-command-router.md`
- `docs/architecture/atlas-handlers.md`
- `docs/architecture/atlas-llm.md`
- `docs/architecture/atlas-streaming.md`
- `docs/architecture/personality-loader.md`
- `docs/architecture/personality-models.md`
- `docs/architecture/personalization.md`
- `docs/architecture/proactive-component.md`
- `docs/architecture/proactive-engine.md`
- `docs/architecture/proactive-executor.md`
- `docs/architecture/response-validator.md`
- `docs/architecture/response-formatter.md`
- `docs/architecture/prompt-builder.md`
- `docs/architecture/prompt-constants.md`
- `docs/architecture/autonomous-executor.md`
- `docs/architecture/autonomous-task-manager.md`
- `docs/architecture/agent-loop.md`
- `docs/architecture/all-intents.md`
- `docs/architecture/decision-validator.md`
- `docs/architecture/conversation.md`
- `docs/development/atlas-personality.md`
- `docs/adr/0031-governed-utterance-pipeline.md`
- `docs/adr/0033-adaptive-prompt-optimization.md`

**Test files to read:**
- `tests/orchestrator/` (entire directory)
- `tests/intent/` (if exists)

### A.3 Context Brief

**What worked in Attempt 3:**
- Intent parsing with hybrid BERT + symbolic fallback (84% intent accuracy, 93% domain accuracy)
- ReAct reasoning loop implemented
- 81 REST endpoints functioning
- Basic conversation handling (when it didn't fail)
- Tool registry with 80+ tools registered

**What failed or was never wired:**
- Basic "hi atlas" fails inconsistently — the core conversation loop is unreliable
- Answer governor (ADR-0031) was designed but implementation status unclear
- Three versions of meta-assessment (v1, v2, v3) — duplication with no clear active version
- Feature flags all set to FALSE — proactive engine, initiative engine, etc. exist but are disabled
- 50+ exception handlers silently swallow errors
- ReAct loop has 4 ungoverned LLM call sites (identified in ADR-0031)
- Orchestrator file is ~2800+ lines — too large, does too much

**What was simulated/fake:**
- Some health reporting claims subsystems are healthy when they are stubs

**Relevant Volume 0 principles:**
- P1: ML advises, symbolic core decides (intent routing)
- P3: Nothing ships without integration
- P5: Silent failure is a system fault
- P9: Output governance — not just action governance
- P10: Atlas has a defined personality
- R1: Start with a working conversation loop
- R6: Model independence
- R8: Observable and debuggable

### A.4 Known Failures & Warnings
1. **The orchestrator is a god object**: `atlas.py` at 2800+ lines does everything. The rebuild must decompose this into focused components with clear responsibilities.
2. **"Hi atlas" fails**: The most basic interaction is unreliable. The rebuild's first milestone is making this work 100% of the time.
3. **Ungoverned output**: ADR-0031 is the most important design document for this volume. The distillation agent must decide how much of the governed utterance pipeline to include in the initial rebuild.
4. **Three meta-assessments**: v1, v2, v3 are all present. This is A1 (feature factory). Decide which (if any) survives.
5. **Proactive system disabled**: Three proactive files exist but are feature-flagged off. Decide if this is REBUILD, DEFER, or KILL.

---

## Part B: Design Specification (Agent Fills Out)

### B.1 Subsystem Purpose (Rebuild)
*[To be filled by distillation agent]*

### B.2 Architecture Overview
*[To be filled by distillation agent]*

### B.3 Interface Contracts
*[To be filled by distillation agent]*

### B.4 Scope Triage
*[To be filled by distillation agent — every component in A.2 must get a REBUILD/DEFER/KILL verdict]*

### B.5 Technology Choices
*[To be filled by distillation agent]*

### B.6 Data Model
*[To be filled by distillation agent]*

### B.7 Error Handling
*[To be filled by distillation agent]*

### B.8 Testing Strategy
*[To be filled by distillation agent]*

### B.9 Configuration
*[To be filled by distillation agent]*

### B.10 Subsystem Lessons Learned
*[To be filled by distillation agent]*

### B.11 Discoveries
*[To be filled by distillation agent]*

### B.12 Oversight Self-Review
*[To be filled by distillation agent — MANDATORY before submission]*

### B.13 Design Quality Scorecard
*[To be filled by distillation agent — MANDATORY. Minimum passing score: 30/45]*

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (70+ code files, 30+ docs), context brief, and 5 known failure warnings including god-object orchestrator and unreliable "hi atlas" | Created the orchestrator analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V02-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
