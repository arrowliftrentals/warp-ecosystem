# ATLAS Design Bible — Volume 2: Orchestrator & Conversation Loop

| Field | Value |
|---|---|
| **Doc ID** | `DB-V02-001` |
| **Name** | Volume 2: Orchestrator & Conversation Loop |
| **Purpose** | Design specification for the central conversation engine — intent parsing, routing, response generation, and personality |
| **Owner** | Design Bible / Volume 2 |
| **Status** | `phase-2-complete` (Part A + B.1-B.4 filled by Phase 1, B.5-B.13 filled by Phase 2) |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / Phase 1 Distillation Agent (B.1-B.4) / Phase 2 Distillation Agent (B.5-B.13) |
| **Version** | v6 |
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

**CORE/PERIPHERAL Classification** (per `DISTILLATION_PROTOCOL.md` Section 5):
- **CORE** (21 files): *Core orchestration:* `atlas.py`, `atlas_handlers.py`, `atlas_command_router.py`, `atlas_llm.py`, `atlas_streaming.py`, `react_engine.py`, `intent_router.py`. *Response pipeline:* `answer_governor.py`, `claim_extractor.py`, `confidence_model.py`, `evidence_store.py`, `evidence_contracts.py`, `response_validator.py`, `prompt_builder.py`. *Intent:* `parser.py`, `grammar.py`, `hybrid_parser.py`, `unified.py`, `decision_validator.py`. *Context:* `memory_context.py`, `services.py`
- **PERIPHERAL** (56 files): All personality/proactive (6), all autonomous (3), `intent_predictor.py`, `bert_classifier.py`, `llm_classifier.py`, `entities.py`, `prompt_constants.py`, `prompts.py`, `response_formatter.py`, `confirmation_manager.py`, `error_recovery.py`, and all "Other orchestrator files" (38)

### A.3 Context Brief

**What worked in Attempt 3:**
- Intent parsing with hybrid BERT
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

The Orchestrator subsystem is the central conversation engine that receives every user message, determines what the user wants (intent parsing), coordinates the appropriate subsystems to fulfill that intent, governs the output before it reaches the user, and records the interaction in memory. It must guarantee that a basic conversational round-trip — receive input, parse intent, retrieve context, generate response, govern output, return — works 100% of the time for any input, degrading gracefully when optional subsystems (LLM, ML classifiers, tools) are unavailable. It enforces Volume 0 principles P1 (ML advises, symbolic core decides), P9 (output governance), and R1 (working conversation loop first) as structural invariants, not aspirational goals. The rebuild must decompose the god-object Atlas class into focused, independently testable components with explicit Pydantic-validated interfaces at every boundary, with the entire subsystem fitting within 1,500 lines total (per P7: smaller and working beats larger and broken).

### B.2 Architecture Overview

**Major components and responsibilities:**

1. **ConversationEngine** (`engine.py`) — The single entry point. Receives a user message + session context, orchestrates the pipeline stages below, and returns a governed response. Stateless per-request; session state lives in Memory (Vol 1). Replaces the 8,000-line `Atlas` god-object.

2. **IntentParser** (`intent.py`) — Three-tier intent resolution: (1) Symbolic grammar matching (deterministic, free, fast), (2) ML classifier advisory (BERT, optional, confidence-gated), (3) LLM fallback (last resort, cheapest model, Pydantic-validated). Outputs a `UnifiedIntent` Pydantic model. The symbolic parser is the authority — ML and LLM only advise.

3. **ResponseGenerator** (`response.py`) — Given a resolved intent and context, produces the raw response. For simple intents (greeting, status), uses deterministic templates. For complex intents, delegates to ReAct engine for multi-step reasoning with tool use. All LLM calls flow through a single `LLMProvider` abstraction (from `shared/llm.py`) ensuring model independence (R6).

4. **OutputGovernor** (integration point, logic owned by Vol 9) — Every response passes through the governance pipeline before reaching the user: extract claims → ground against evidence → compute symbolic confidence → downgrade unsupported claims → emit `GovernedOutput`. Vol 2 calls the governor; Vol 9 owns the implementation.

5. **PersonalityManager** — Loads and caches the canonical personality model (Jarvis by default). Injects personality into system prompts. Personality is immutable at runtime per P10; changes require explicit human approval.

6. **MemoryContextRetriever** — Gathers relevant context from memory layers (L3 episodic, L4 declarative, L5 procedural, L8 goals, L9 social) to enrich the prompt before response generation. Owned by Vol 2, consumes Vol 1 interfaces.

**Data flow (happy path):**

```
User Message
    │
    ▼
┌─────────────────┐
│ ConversationEngine│
│  (engine.py)      │
└─────┬───────────┘
      │ 1. Parse intent
      ▼
┌─────────────────┐
│  IntentParser    │ ── symbolic grammar ──▶ match? → UnifiedIntent
│  (intent.py)     │ ── ML classifier ────▶ advisory confidence
│                   │ ── LLM fallback ────▶ last resort
└─────┬───────────┘
      │ 2. Retrieve memory context
      ▼
┌─────────────────┐
│ MemoryContext    │ ── queries L3-L9 ──▶ context dict
│ Retriever        │
└─────┬───────────┘
      │ 3. Generate response
      ▼
┌─────────────────┐
│ ResponseGenerator│ ── templates (simple) ──▶ raw text
│ (response.py)    │ ── ReAct engine (complex) ──▶ raw text + evidence
│                   │ ── tool calls via ToolRegistry (Vol 10)
└─────┬───────────┘
      │ 4. Govern output
      ▼
┌─────────────────┐
│ OutputGovernor   │ ── claim extraction ──▶ evidence grounding
│ (Vol 9 impl)     │ ── confidence model ──▶ authority_level
│                   │ ── speculation scrub ──▶ GovernedOutput
└─────┬───────────┘
      │ 5. Record interaction
      ▼
   Memory (Vol 1)
      │
      ▼
  GovernedOutput → User
```

**Key architectural decisions:**
- ConversationEngine is the ONLY public entry point. No other module calls subsystems directly.
- Every boundary uses Pydantic schemas (P8). No raw dicts cross component boundaries.
- The engine is async but each pipeline stage is independently testable in sync isolation.
- Tool invocation (ReAct) is gated by `DecisionValidator` (Vol 9) before execution.
- Streaming is a transport concern handled at the API layer (Vol 8), not in the engine.

### B.3 Interface Contracts

#### 3.1 ConversationEngine

**Public method:**
```
async def process_message(
    message: str,
    session_id: str,
    device_id: str = "default",
) -> ConversationResponse
```

**Input schema (`ConversationRequest` — defined in `contracts/api_schemas.py`):**
```
class ConversationRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User message text")
    session_id: str = Field(default_factory=lambda: str(uuid4()), description="Session identifier")
    device_id: str = Field(default="default", description="Source device")
    stream: bool = Field(default=False, description="Enable streaming")
```

**Output schema (`ConversationResponse`):**
```
class ConversationResponse(BaseModel):
    session_id: str
    response: str = Field(..., description="Governed response text")
    intent: ResolvedIntent
    evidence_refs: list[str] = Field(default_factory=list, description="EvidenceItem IDs grounding the response")
    authority_level: AuthorityLevel
    confidence: float = Field(ge=0.0, le=1.0)
    actions_taken: list[str] = Field(default_factory=list)
    metadata: ResponseMetadata
```

**Dependencies consumed:**
- `MemoryManager` (Vol 1) — session management, context retrieval, interaction storage
- `DecisionValidator` (Vol 9) — intent validation gate
- `AnswerGovernor` (Vol 9) — output governance
- `ToolRegistry` (Vol 10) — tool lookup and execution
- `LLMProvider` (shared) — model-independent LLM calls
- `AtlasConfig` (shared) — configuration

**Dependencies served:**
- Vol 8 (API) calls `process_message` from route handlers

#### 3.2 IntentParser

**Public method:**
```
def parse(command: str, context: dict | None = None) -> UnifiedIntent
```

**Output schema (`UnifiedIntent` — already exists, keep as-is):**
```
class UnifiedIntent(BaseModel):
    category: IntentCategory          # From 320-intent taxonomy
    domain: IntentDomain              # Auto-derived from category
    confidence: float                 # 0.0-1.0
    action: str | None                # Primary action verb
    target: str | None                # Primary target
    entities: list[ExtractedEntity]   # Extracted entities
    raw_command: str                  # Original text
    needs_llm: bool                   # Whether LLM needed for response
    classification_source: str        # 'symbolic', 'bert', 'llm', 'hybrid'
```

**Dependencies consumed:**
- `CommandGrammar` (internal) — symbolic verb/pattern matching
- `EntityExtractor` (internal) — regex-based entity extraction
- `ClassificationService` (optional, ML) — BERT classifier
- `LLMProvider` (shared) — LLM fallback classification

**Dependencies served:**
- `ConversationEngine` calls `parse()` on every incoming message

#### 3.3 ResponseGenerator

**Public method:**
```
async def generate(
    intent: UnifiedIntent,
    context: MemoryContext,
    session_id: str,
) -> RawResponse
```

**Output schema:**
```
class RawResponse(BaseModel):
    content: str                      # Raw response text
    phase: OutputPhase                # Which pipeline phase produced this
    evidence_store: EvidenceStore | None  # Tool execution evidence (for governance)
    tool_calls: list[ToolCallRecord]  # Record of tools invoked
    model_used: str | None            # LLM model if used, None if deterministic
```

**Dependencies consumed:**
- `LLMProvider` (shared) — for LLM-based responses
- `ToolRegistry` (Vol 10) — for ReAct tool execution
- `PersonalityManager` (internal) — for prompt personality injection
- `SystemPromptBuilder` (internal) — for modular prompt construction

#### 3.4 MemoryContextRetriever

**Public method:**
```
async def retrieve(
    command: str,
    session_id: str,
) -> MemoryContext
```

**Output schema:**
```
class MemoryContext(BaseModel):
    recent_episodes: list[dict]       # From L3 (max 5, current session)
    relevant_facts: list[dict]        # From L4 (keyword-matched)
    validated_skills: list[dict]      # From L5
    active_goals: list[dict]          # From L8
    user_preferences: dict            # From L9
    vector_matches: list[dict]        # From L10 (semantic search)
```

**Dependencies consumed:**
- `MemoryManager` (Vol 1) — all layer queries

#### 3.5 PersonalityManager

**Public methods:**
```
def get_system_prompt() -> str
def get_traits() -> PersonalityTraits
def get_conciseness_reinforcement() -> str
```

**Schema (`PersonalityTraits`):**
```
class PersonalityTraits(BaseModel):
    proactivity: float = 0.9         # 0.0-1.0
    verbosity: float = 0.3           # 0.0-1.0
    formality: float = 0.5           # 0.0-1.0
    assertiveness: float = 0.8       # 0.0-1.0
    humor: float = 0.2               # 0.0-1.0
    ask_before_action: bool = False
    explain_reasoning: bool = True
    terse_data_mode: bool = True
```

**Dependencies consumed:** None (reads from config/file at startup, then cached)

#### 3.6 Cross-Volume Interface Summary

- **Vol 1 → Vol 2:** `MemoryManager` provides session CRUD, layer queries (L1-L10). Vol 2 calls `memory.start_conversation()`, `memory.add_message()`, `memory.get_conversation()`, and per-layer query methods.
- **Vol 9 → Vol 2:** `DecisionValidator.validate(intent, command, context) -> ValidationDecision`. `AnswerGovernor.govern(content, phase, evidence_store) -> GovernedOutput`. Vol 2 calls these; Vol 9 defines them.
- **Vol 10 → Vol 2:** `ToolRegistry.execute(tool_name, arguments, context) -> dict`. `ToolRegistry.get_openai_schema() -> list[dict]`. Vol 2's ReAct engine calls tools; Vol 10 owns tool definitions.
- **Vol 8 → Vol 2:** API routes call `ConversationEngine.process_message()`. The engine returns `ConversationResponse`; Vol 8 serializes it to HTTP.
- **Vol 3 → Vol 2:** `ActiveLearner` receives intent corrections from Vol 2 when user provides feedback. `LearningManager.record_interaction()` for pattern learning.

### B.4 Scope Triage

#### REBUILD (13 components — redesigned from scratch)

**`atlas.py` (core orchestration) → `engine.py`**
REBUILD. The 8,000-line god-object is the root cause of integration failure. Replace with a ~300-line `ConversationEngine` that orchestrates focused components. The `__init__` alone was 400+ lines of wiring — this moves to a dependency injection pattern at startup.

**`atlas_command_router.py` → absorbed into `engine.py`**
REBUILD. The `process_command` / `_process_command_guarded` / `_route_command` chain had correct crash-guard and telemetry patterns. The routing logic (pending actions, interrupted tasks, confirmation flows, ReAct detection) is the core pipeline — it survives as the body of `engine.py`'s `process_message`.

**`atlas_handlers.py` → eliminated (handlers move to domain modules)**
REBUILD. Intent-specific handlers (UI commands, file operations, memory queries, introspection) were a mixin of 2,086 lines. Each handler category moves to its owning volume: UI handlers → Vol 10, file handlers → Vol 10, memory handlers → Vol 1 integration. The orchestrator only routes; it does not handle.

**`atlas_llm.py` → absorbed into `response.py`**
REBUILD. The LLM call orchestration (prompt building, function calling, streaming) becomes part of `ResponseGenerator`. The critical pattern — build system prompt, inject personality + context + tools, call LLM, validate response — is preserved.

**`react_engine.py` → `response.py` (ReAct subsystem)**
REBUILD. The ReAct (Reason+Act) loop is architecturally sound: THINK → ACT → OBSERVE → REFLECT → ANSWER with Pydantic-validated schemas at each phase. Rebuild with these changes: (a) all 4 LLM call sites must pass through `AnswerGovernor` (currently ungoverned), (b) evidence storage via `EvidenceStore` replaces lossy observation summaries, (c) max 5 iterations with a hard timeout.

**`intent_router.py` → `intent.py`**
REBUILD. The three-tier routing logic (symbolic → BERT → LLM) is correct. Rebuild simplified: remove the 1,957 lines of contraction expansion, implicit pattern matching, and affordance mapping into a cleaner tiered dispatch. The MH-IDP preprocessing pipeline was over-engineered for an intent parser.

**`parser.py` (intent) → `intent.py` (symbolic tier)**
REBUILD. The symbolic parser's core pattern (grammar verbs → IntentType, entity extraction, confidence scoring, disambiguation) is valuable. Rebuild as the deterministic first tier within the unified `IntentParser`.

**`grammar.py` → `intent.py` (grammar definitions)**
REBUILD. The `ActionPattern` / `CommandGrammar` pattern is the right abstraction. Rebuild with the same verb sets but using `IntentCategory` (320 values) instead of `IntentType` (9 values) as the target taxonomy from day one.

**`unified.py` → `intent.py` (UnifiedIntent schema)**
REBUILD. The `UnifiedIntent` Pydantic schema is the correct target representation. Rebuild as-is with minor cleanup (remove legacy mapping fields).

**`prompt_builder.py` → `response.py` (prompt construction)**
REBUILD. The priority-based section system with token budgeting is well-designed. Rebuild with the same `SectionPriority` concept but simpler (no chaining API, just a function that takes sections and a budget).

**`memory_context.py` → standalone module preserved**
REBUILD. The per-layer retrieval pattern (L3 episodes, L4 facts, L5 skills, L8 goals, L9 social) is the correct design. Rebuild with Pydantic-validated output schema (`MemoryContext`) instead of raw dicts.

**`services.py` → eliminated (DI at startup)**
REBUILD. The `Services` container was a workaround for the god-object's attribute explosion. In the rebuild, the `ConversationEngine` receives its dependencies via constructor injection — no container needed.

**`personality_loader.py` + `personality_models.py` → `personality.py`**
REBUILD. Merge into a single module. The Jarvis personality model definition and trait system are correct. Rebuild with the same `PersonalityTraits` dataclass and `get_system_prompt()` interface.

#### DEFER (8 components — build after MVA-1 passes)

**`answer_governor.py`, `claim_extractor.py`, `confidence_model.py`, `evidence_store.py`, `evidence_contracts.py`**
DEFER to Tier 4 (post MVA-1). The governed utterance pipeline (ADR-0031) is architecturally important (P9) but not required for MVA-1 (basic conversation). The engine calls `AnswerGovernor.govern()` via a thin interface; the initial implementation returns a pass-through `GovernedOutput` with `authority_level=ADVISORY`. The full pipeline (extract → ground → verify → downgrade) activates at Tier 4. Ownership: Vol 9.

**`response_validator.py`**
DEFER. The old `ResponseValidator` checked LLM claims against system state — a precursor to `AnswerGovernor`. Superseded by the ADR-0031 pipeline. The governor subsumes this functionality.

**`autonomous_executor.py`**
DEFER to Tier 6+. Multi-step autonomous execution (plan → sandbox → validate → propose) depends on sandbox (Vol 4) and the full tool ecosystem. Not needed for MVA-1 through MVA-4.

**`agent_loop.py`**
DEFER to Tier 6+. The persistent autonomous loop (presence detection → initiative generation → proactive execution) is a Jarvis-level capability that depends on proactive engine, initiative engine, and presence detector. Not needed for any MVA.

#### KILL (56 components — do not rebuild)

**`atlas_streaming.py`**
KILL. Streaming is a transport concern, not an orchestrator concern. Vol 8 (API) handles SSE/WebSocket streaming by consuming the engine's async generator. No streaming logic in the orchestrator.

**`proactive_component.py`, `proactive_engine.py`, `proactive_executor.py`**
KILL (for now — revisit post-MVA as DEFER). Three separate files for a feature that was permanently disabled via feature flags. The proactive concept is valid for later but rebuilding three modules for a disabled feature violates P7.

**`intent_predictor.py`**
KILL. Predictive intent (guessing the next command) was never wired. Aspirational feature without integration.

**`personalization.py`**
KILL. User-adaptive response personalization was a thin wrapper around L9 queries. The `MemoryContextRetriever` already retrieves L9 preferences; personalization logic belongs in the prompt builder, not a separate module.

**`confirmation_manager.py`**
KILL as standalone module. Confirmation flow logic ("are you sure?") is a few lines within the engine's routing, not a separate manager class.

**`error_recovery.py`**
KILL as standalone module. Error recovery patterns (retry, circuit breaker) belong in `shared/errors.py` as utilities, not an orchestrator component.

**`bert_classifier.py`**
KILL as Vol 2 component. BERT model loading and inference is an ML concern. Rebuild as part of the `ClassificationService` in `shared/` or a dedicated `ml/` package. The `IntentParser` consumes it via an abstract `Classifier` protocol — it does not own the model.

**`llm_classifier.py`**
KILL as standalone module. LLM-based classification is 145 lines and becomes a method within `IntentParser` (the LLM fallback tier). No separate module needed.

**`entities.py`**
KILL as standalone module. Entity extraction (200 lines) becomes an internal function of `IntentParser`. The regex patterns are preserved.

**`hybrid_parser.py`**
KILL. The `HybridIntentParser` class was a thin wrapper that called symbolic then LLM. This logic is now the core of `IntentParser`'s three-tier dispatch — no separate wrapper needed.

**`decision_validator.py`**
KILL from Vol 2. Ownership confirmed as Vol 9 (Governance) per AGENT_COMM.md pre-registered boundaries. Vol 2 consumes it via the interface.

**`prompt_constants.py`, `prompts.py`**
KILL as separate files. Prompt templates are co-located with the `SystemPromptBuilder` in `response.py`. Two separate prompt files created confusion about which was authoritative.

**`response_formatter.py`**
KILL. Response formatting (markdown, code blocks) is a concern of the API layer or the personality system, not a separate orchestrator module.

**`tool_registry.py`, `tool_schemas.py`**
KILL from Vol 2. Ownership confirmed as Vol 10 (External Tools) per AGENT_COMM.md. Vol 2 consumes the registry; Vol 10 defines it.

**`autonomous_task_manager.py`**
KILL from Vol 2. Task lifecycle management belongs with the autonomous executor (DEFERRED to Tier 6+).

**All 38 "Other orchestrator files":**
`architecture_discovery.py`, `assessment_manager.py`, `awareness_cache.py`, `background_control.py`, `benchmark_fetcher.py`, `codebase_awareness.py`, `cognitive_fabric.py`, `comparative_analyzer.py`, `critical_assessments.py`, `degradation_matrix.py`, `dynamic_assessment.py`, `external_apis.py`, `file_resolver.py`, `git_state_provider.py`, `goal_manager.py`, `initiative_engine.py`, `integration_bridge.py`, `intelligence_integration.py`, `interrupted_tasks.py`, `live_exercise_runner.py`, `market_analyzer.py`, `meta_assessment.py`, `meta_assessment_v2.py`, `meta_assessment_v3.py`, `meta_diff.py`, `meta_storage.py`, `ml_training_analyzer.py`, `narrative_generator.py`, `pending_actions.py`, `policy_engine.py`, `presence_detector.py`, `resource_manager.py`, `scheduler.py`, `task_decomposition.py`, `telemetry_bridge.py`, `tool_registry.py`, `tool_schemas.py`, `verified_orchestrator.py`
KILL from Vol 2. These are scope explosion artifacts — each belongs to another volume (Learning, Intelligence, Self-Modification, Governance) or should not exist. The three `meta_assessment` versions are a textbook A1 (feature factory) violation. `goal_manager.py` belongs to Vol 1 (L8 goals memory). `initiative_engine.py` and `presence_detector.py` belong to a future proactive subsystem (Tier 6+). `codebase_awareness.py` and `cognitive_fabric.py` belong to Vol 5 (Intelligence). None belong in the conversation engine.

#### Scope Triage Summary

- **REBUILD:** 13 components → 4 files (`engine.py`, `intent.py`, `response.py`, `personality.py`) + `memory_context.py`
- **DEFER:** 8 components (governance pipeline: Tier 4; autonomous: Tier 6+)
- **KILL:** 56 components (scope explosion, wrong volume, duplication, or absorbed into rebuilt components)

### B.5 Technology Choices

**Defaults retained (no justification needed):**
- Python 3.11+ — type unions (`X | None`), `StrEnum`, `match` statements
- Pydantic v2 — all orchestrator schemas use `model_validator`, `field_validator`, discriminated unions
- structlog — structured JSON logging throughout orchestrator pipeline

**Subsystem-specific choices:**

| Technology | Use | Justification |
|---|---|---|
| `re` (stdlib) | Symbolic intent parsing in `grammar.py` — ~30 compiled regex patterns covering greetings, system commands, file ops, memory queries, learning triggers | Regex provides deterministic, zero-latency intent classification for known patterns. Attempt 3's `grammar.py` proves this works. No external dependency needed. |
| `torch` + `transformers` | Optional BERT-based intent classifier (`bert_classifier.py`) | Gated behind `ATLAS_ENABLE_BERT` feature flag (default: OFF). Used only when symbolic parser returns low confidence (<0.6). The rebuild starts symbolic-only; BERT is Phase 3+. |
| LLMProvider Protocol (`shared/llm.py`) | All LLM calls in orchestrator (response generation, ReAct reasoning, LLM-fallback classification) | R6 model independence. Attempt 3's `atlas_llm.py` hard-coded OpenAI client with provider-specific kwargs scattered across 15+ call sites. The rebuild uses a single Protocol so switching providers requires zero orchestrator changes. |
| `hashlib` (stdlib) | SHA-256 evidence integrity in `evidence_store.py` | EvidenceItem hashes are required by shared-contracts §1.2. No external crypto library needed for hash-only integrity. |

**Departures from defaults:** None. The orchestrator uses no storage engine directly (memory access is through Vol 1 MemoryManager), no custom web framework (API layer is Vol 8), and no custom serialization (Pydantic handles all schema conversion).

### B.6 Data Model

Schemas owned by Volume 2 (per shared-contracts §1.6, location: `atlas/orchestrator/schemas.py`):

**B.6.1 UnifiedIntent**
```
class UnifiedIntent(BaseModel):
    category: IntentCategory          # StrEnum with 320 values from taxonomy
    domain: str | None                # e.g. "file_operations", "memory", "system" — None for general
    confidence: float                  # 0.0-1.0, from classification source
    action: str | None                # specific action verb: "read", "search", "store", "explain"
    target: str | None                # object of action: file path, memory layer, topic
    entities: list[ExtractedEntity]   # extracted entities (names, paths, values)
    raw_command: str                   # original user input, unmodified
    needs_llm: bool                    # True if symbolic parser cannot handle this intent
    classification_source: ClassificationSource  # StrEnum: SYMBOLIC, BERT, LLM_FALLBACK, HYBRID

    @field_validator("confidence")
    def confidence_bounded(cls, v): ...  # clamp to [0.0, 1.0]
```
Note: Attempt 3's `unified.py` uses IntentCategory (320 values) with auto-derived IntentDomain. The rebuild preserves this taxonomy. `IntentCategory` enum location: defined in `orchestrator/schemas.py`, re-exported from `shared/types.py` for Vol 3 and Vol 9 consumption.
Persists to: L3 (episodic — logged with every interaction), L5 (procedural — intent patterns that improve over time).

**B.6.2 ExtractedEntity**
```
class ExtractedEntity(BaseModel):
    name: str                          # entity label: "file_path", "layer_name", "query_term"
    value: str                         # extracted value: "/src/main.py", "L4", "Python"
    entity_type: EntityType            # StrEnum: PATH, LAYER, TOPIC, NUMBER, NAME, COMMAND
    span: tuple[int, int] | None       # character offsets in raw_command, None if inferred
    confidence: float                  # entity extraction confidence
```
Persists to: embedded in UnifiedIntent (not stored independently).

**B.6.3 ConversationRequest**
```
class ConversationRequest(BaseModel):
    query: str                         # user input text
    session_id: str | None = None      # existing session or None for new
    device_id: str = "default"         # multi-device support (P10 Jarvis path)
    stream: bool = False               # SSE streaming (per C-12 resolution: single endpoint)

    @field_validator("query")
    def query_not_empty(cls, v): ...   # strip + non-empty check
```

**B.6.4 ConversationResponse**
```
class ConversationResponse(BaseModel):
    session_id: str                    # always present in response
    response: str                      # governed text (post-AnswerGovernor)
    intent: UnifiedIntent              # classified intent for this turn
    evidence_refs: list[EvidenceRef]   # grounding evidence (from Vol 9 EvidenceStore)
    authority_level: AuthorityLevel    # GROUNDED / ADVISORY / SPECULATIVE (from Vol 9)
    confidence: float                  # overall response confidence
    actions_taken: list[ToolCallRecord]  # tool calls executed during ReAct loop
    metadata: ResponseMetadata         # timing, token counts, classification path
```
Note: Vol 8 maps this to `ChatResponse` for HTTP (per C-13 resolution). Field mapping: `response` → `answer`, `evidence_refs` → `evidence`.

**B.6.5 MemoryContext**
```
class MemoryContext(BaseModel):
    recent_messages: list[dict]        # from L1/L2 via MemoryManager.get_recent_messages()
    relevant_facts: list[dict]         # from L4 semantic search
    relevant_episodes: list[dict]      # from L3 temporal query
    user_profile: dict | None          # from L9 if available
    active_goals: list[dict]           # from L8 if available
    assembled_at: datetime             # timestamp of context assembly
    token_estimate: int                # estimated token count for LLM context window
```

**B.6.6 RawResponse**
```
class RawResponse(BaseModel):
    content: str                       # LLM-generated text (pre-governance)
    evidence_store: str                # reference to EvidenceStore session ID
    tool_calls: list[ToolCallRecord]   # tools invoked during generation
    generation_model: str              # which LLM model produced this
    token_usage: dict                  # prompt_tokens, completion_tokens
```
This is the pre-governance artifact. It enters AnswerGovernor.govern() and exits as GovernedOutput (Vol 9 schema).

**B.6.7 ToolCallRecord**
```
class ToolCallRecord(BaseModel):
    tool_name: str                     # registry name of tool called
    arguments: dict                    # arguments passed to tool
    result_summary: str | None         # truncated result for metadata
    success: bool                      # tool execution succeeded
    execution_time_ms: float           # latency tracking
    evidence_id: str | None            # EvidenceStore ID if stored
```

**B.6.8 ResponseMetadata**
```
class ResponseMetadata(BaseModel):
    processing_time_ms: float          # total request processing time
    classification_source: ClassificationSource  # how intent was classified
    classification_time_ms: float      # intent classification latency
    react_steps: int                   # number of ReAct think-act-observe cycles
    tokens_used: dict                  # prompt/completion token breakdown
    governance_applied: bool           # whether AnswerGovernor processed the response
    evidence_count: int                # number of evidence items grounding the response
```

**B.6.9 PersonalityTraits**
```
class PersonalityTraits(BaseModel):
    name: str = "Atlas"                # canonical name
    tone: str = "professional_conversational"  # per P10
    proactivity: float = 0.9           # 0.0 (reactive only) to 1.0 (aggressively proactive)
    verbosity: float = 0.3            # terse by default — executive summaries only
    formality: float = 0.5             # uses "sir" selectively, not every line
    assertiveness: float = 0.8         # confident and direct
    humor: float = 0.2                 # subtle wit, mostly serious
    ask_before_action: bool = False
    explain_reasoning: bool = True
    terse_data_mode: bool = True       # strip unnecessary words from data/diagnostics

    class Config:
        frozen = True                  # immutable — self-modification cannot alter without human approval (P10)
```
Note: Attempt 3 uses a `dataclass` for `PersonalityTraits` (not Pydantic). The rebuild converts to `BaseModel` with `frozen=True` to enforce immutability via Pydantic validation (P8). Loaded from config file at startup, not stored in memory layers. Version-controlled in `config/personality.yaml`.

### B.7 Error Handling

All orchestrator errors inherit from `AtlasError` (defined in `shared/errors.py` per shared-contracts §5.1).

**B.7.1 Error Types**

| Error Class | Inherits From | When Raised | Severity |
|---|---|---|---|
| `IntentParsingError` | `AtlasError` | Symbolic parser, BERT, and LLM fallback all fail to classify intent | `warning` — falls back to UNKNOWN intent, does not crash |
| `ResponseGenerationError` | `AtlasError` | LLM call fails, times out, or returns empty/malformed content | `error` — returns user-facing error message, logs full context |
| `MemoryContextError` | `AtlasError` | MemoryManager.assemble_context() fails (DB unavailable, corrupt data) | `warning` — proceeds with empty context, logs degraded state |
| `ReActLoopError` | `AtlasError` | ReAct loop exceeds max iterations or tool execution fails unrecoverably | `error` — returns partial response with evidence gathered so far |

**B.7.2 Error Propagation Rules (P5 compliance)**

1. **No silent swallowing.** Every `except` block must: (a) log the exception with structlog at appropriate level, (b) include `exc_info=True` for stack trace, (c) set a measurable degradation flag on ResponseMetadata.
2. **Graceful degradation over crash.** Intent parsing failure → UNKNOWN intent → generic LLM response. Memory unavailable → empty context → reduced-quality response. Tool failure → skip tool, note in evidence. The conversation loop must ALWAYS return a response to the user.
3. **Error classification.** All errors carry `category` and `severity` fields (from AtlasError base). Categories: `INTENT`, `GENERATION`, `MEMORY`, `TOOL`, `GOVERNANCE`. Severities: `info`, `warning`, `error`, `critical`.
4. **Learning system integration.** All errors with severity ≥ `warning` are forwarded to Vol 3 (Learning) via `OutcomeSignal` with `outcome_type=FAILURE`. This enables the learning system to detect recurring failure patterns and propose mitigations.

**B.7.3 Recovery Strategies**

| Error | Recovery | Fallback |
|---|---|---|
| IntentParsingError | Retry with LLM fallback classifier | Classify as UNKNOWN, route to generic handler |
| ResponseGenerationError | Retry with different LLM provider (if configured) | Return canned error message: "I encountered an issue generating a response. Here's what I gathered: [evidence summary]" |
| MemoryContextError | Proceed with empty MemoryContext | Log degraded mode, include `memory_degraded: true` in metadata |
| ReActLoopError | Return partial response from last successful observe step | Include partial evidence, flag `incomplete: true` in metadata |

**B.7.4 Forbidden Patterns**
- `except Exception: pass` — FORBIDDEN (P5)
- `except: pass` — FORBIDDEN (P5)
- Logging without re-raising or handling — must either recover or propagate
- Generic `raise Exception("error")` — must use typed error hierarchy

### B.8 Testing Strategy

**B.8.1 Acceptance Tests (MANDATORY)**

**AT-1: Basic Conversation Round-Trip**
- Input: `POST /v1/atlas/chat` with `{"query": "hello"}` (no session_id)
- Expected: HTTP 200, response body contains `session_id` (non-empty string), `response` (non-empty string, coherent greeting), `governed: true`, `authority_level: "GROUNDED"` or `"ADVISORY"`
- Entry point: Live server on port 8000
- Pass criteria: Response received within 5 seconds, all required fields present and typed correctly
- Regression target: A.4 item 2 ("Hi atlas" fails)

**AT-2: Intent Classification Accuracy**
- Input: 10 representative queries covering all IntentCategory values: "hello" (GREETING), "what is Python?" (QUESTION), "read file /src/main.py" (FILE_OP), "remember that X" (MEMORY), "search for Y" (COMMAND), etc.
- Expected: Each query classified to correct IntentCategory with confidence ≥ 0.6
- Entry point: `POST /v1/atlas/chat` for each query
- Pass criteria: ≥ 8/10 correct classifications (80% accuracy floor)
- Regression target: A.4 item 1 (god object — proves decomposed engine still routes correctly)

**AT-3: Evidence-Grounded Response**
- Input: `POST /v1/atlas/chat` with `{"query": "read file /src/atlas/shared/config.py and tell me what it contains"}`
- Expected: Response references actual file contents (not hallucinated), `evidence_refs` contains at least one entry with `source: "file_read"`, `authority_level: "GROUNDED"`
- Entry point: Live server, requires file system access
- Pass criteria: Evidence refs non-empty, response content verifiable against actual file
- Regression target: A.4 item 3 (ungoverned output — proves governance pipeline active)

**AT-4: Error Recovery Under Memory Failure**
- Input: `POST /v1/atlas/chat` with valid query while memory DB is intentionally unavailable (stop DB, corrupt path)
- Expected: HTTP 200 (NOT 500), response body contains degradation notice, `metadata.memory_degraded: true`
- Entry point: Live server with memory layer disabled
- Pass criteria: User receives a response (not a crash), error is logged with full context
- Regression target: A.4 item 2 (unreliable conversation) + P5 (no silent failure)

**B.8.2 Integration Tests**

| Test | Components | What It Proves |
|---|---|---|
| Intent→Engine→Response pipeline | IntentParser + ConversationEngine + ResponseGenerator | A parsed intent flows through the full engine and produces a ConversationResponse with all required fields |
| ReAct tool execution loop | ConversationEngine + ToolRegistry (Vol 10) + EvidenceStore (Vol 9) | Tool calls during ReAct are executed, results stored in EvidenceStore, and referenced in final response |
| Memory context assembly | ConversationEngine + MemoryManager (Vol 1) | Engine calls assemble_context() and uses returned MemoryContext to enrich the LLM prompt |
| Governance pipeline | ResponseGenerator + AnswerGovernor (Vol 9) + EvidenceStore | Raw LLM output passes through AnswerGovernor, claims are extracted and grounded, GovernedOutput is produced |

**B.8.3 Unit Tests**

| Component | Key Unit Tests |
|---|---|
| IntentParser (symbolic) | Each grammar pattern matches expected inputs; unknown inputs return UNKNOWN with low confidence |
| PromptBuilder | Context assembly produces well-formed prompts under token budget; personality traits are injected correctly |
| MemoryContext assembly | Token estimation is accurate within 10%; context prioritization respects recency and relevance |
| UnifiedIntent validation | Pydantic validators reject invalid confidence ranges, empty raw_command, mismatched entity types |

**B.8.4 Attempt 3 Regression Tests**

| ID | A.4 Failure | Test Description | Pass Criteria |
|---|---|---|---|
| RT-1 | God object (A.4.1) | Verify no single Python file in `orchestrator/` exceeds 500 lines | `wc -l` on all .py files in orchestrator/ returns max < 500 |
| RT-2 | "Hi atlas" fails (A.4.2) | Send "hi", "hello", "hey atlas" 100 times consecutively | 100/100 receive valid responses (zero failures) |
| RT-3 | Ungoverned output (A.4.3) | Send query requiring tool use, verify `governed: true` in response | AnswerGovernor.govern() was called (mock verification or metadata check) |
| RT-4 | Triple meta-assessment (A.4.4) | Grep orchestrator/ for "meta_assessment" or "MetaAssessment" | Zero matches — meta-assessment is KILLED |
| RT-5 | Disabled proactive (A.4.5) | Verify proactive components are not imported in REBUILD-scope files | No imports of proactive_engine, proactive_component, proactive_executor in engine.py, intent.py, response.py |

### B.9 Configuration

All orchestrator configuration loads through `AtlasConfig(BaseSettings)` from `shared/config.py` (per shared-contracts §5.2). Environment variable prefix: `ATLAS_`.

**B.9.1 Environment Variables**

| Variable | Type | Default | Description |
|---|---|---|---|
| `ATLAS_DEFAULT_MODEL` | str | `"gpt-4"` | Default LLM model for response generation |
| `ATLAS_FALLBACK_MODEL` | str | `"gpt-3.5-turbo"` | Fallback model when primary fails or for low-priority queries |
| `ATLAS_MAX_REACT_STEPS` | int | `5` | Maximum ReAct think-act-observe iterations before forced termination. Note: Attempt 3 defaults to 15 in `react_engine.py` but 5 is the correct rebuild default per P7 (smaller and working). |
| `ATLAS_INTENT_CONFIDENCE_THRESHOLD` | float | `0.6` | Below this confidence, intent is classified as UNKNOWN or escalated to LLM |
| `ATLAS_MAX_CONTEXT_TOKENS` | int | `4096` | Maximum tokens allocated to memory context in LLM prompt |
| `ATLAS_RESPONSE_TIMEOUT_SECONDS` | float | `30.0` | Maximum time for a single response generation (including tool calls) |
| `ATLAS_ENABLE_BERT` | bool | `False` | Feature flag: enable BERT-based intent classification (Phase 3+) |
| `ATLAS_ENABLE_PROACTIVE` | bool | `False` | Feature flag: enable proactive suggestion engine (DEFERRED) |
| `ATLAS_PERSONALITY_PATH` | str | `"config/personality.yaml"` | Path to personality configuration file |
| `ATLAS_LOG_LEVEL` | str | `"INFO"` | Logging level for orchestrator components |

**B.9.2 Feature Flags**

Only two feature flags exist for the orchestrator. Both default to OFF (disabled). This is deliberate — Attempt 3 had 15+ feature flags all set to FALSE, meaning the features were dead code. The rebuild only adds a flag when there is a concrete Phase 3+ plan to enable it.

| Flag | Default | Enables | Phase |
|---|---|---|---|
| `ATLAS_ENABLE_BERT` | `False` | BERT intent classifier as secondary classification source | Phase 3 (after symbolic parser proves stable) |
| `ATLAS_ENABLE_PROACTIVE` | `False` | Proactive suggestion engine (proactive_engine.py scope) | Phase 4+ (DEFERRED per B.4) |

**B.9.3 Configuration Loading**

Configuration is loaded once at startup via `AtlasConfig()` which reads from environment variables and `.env` file (pydantic-settings `env_file` support). No runtime configuration changes — if config changes, the server restarts. This prevents the configuration drift that plagued Attempt 3 where runtime config mutations caused inconsistent behavior.

### B.10 Subsystem Lessons Learned

**B.10.1 The God-Object Orchestrator**
- **What happened:** `atlas.py` grew to 2800+ lines with 80+ attributes initialized in a 400+ line `__init__`, handling intent parsing, response generation, memory assembly, tool execution, personality loading, service initialization, health reporting, streaming, error recovery, and proactive triggering — all in one class.
- **Why it happened:** No architectural boundary enforcement. Each new feature was added to the Atlas class because it was the easiest place to wire it in. The Services class attempted to extract initialization but became another bag of references.
- **What the rebuild does differently:** The orchestrator is decomposed into four focused modules: `engine.py` (conversation loop coordination, <300 lines), `intent.py` (parsing pipeline), `response.py` (generation + governance integration), and `schemas.py` (Pydantic models). No module exceeds 500 lines. The engine delegates to IntentParser, ResponseGenerator, and MemoryManager — it does not implement their logic.

**B.10.2 Deferred Initialization Anti-Pattern**
- **What happened:** `atlas.py` `__init__` initialized 30+ subsystem instances, setting many to `None` first then populating them in `_init_deferred_subsystems()`. Attributes like `self.decision_validator = None`, `self.proactive_executor = None` etc. (lines 335-374 of atlas.py) created a minefield where any method could encounter None attributes at runtime.
- **Why it happened:** No dependency injection. Components were instantiated in a fixed order. Circular dependencies required deferred attribute assignment.
- **What the rebuild does differently:** Dependency injection via constructor parameters. The API server (Vol 8) constructs components in dependency order and passes them to ConversationEngine. If a component fails to construct, startup fails immediately with a clear error — no partial initialization.

**B.10.3 Ungoverned ReAct Loop**
- **What happened:** `react_engine.py` defined Pydantic schemas (ReActThought, ReActToolCall, ReActObservation, ReflectResponse) for the think-act-observe cycle but the 4 LLM call sites (`_think`, `_observe`, `_reflect`, `_answer`) did not pass results through AnswerGovernor. ADR-0031 identified this gap.
- **Why it happened:** The ReAct engine was built before ADR-0031 defined the governed utterance pipeline. Retrofitting governance into an existing loop required changes to every LLM call site.
- **What the rebuild does differently:** The ReAct loop's final output (after all think-act-observe cycles) passes through `AnswerGovernor.govern()` before reaching the user. Intermediate think/observe steps are logged but not user-facing. The loop itself is governed by `max_react_steps` configuration and a hard timeout.

**B.10.4 Over-Engineered Intent Router**
- **What happened:** `intent_router.py` implemented a Multi-Head Intent Disambiguation Pipeline (MH-IDP) with contraction expansion, affordance mapping (`_TOOL_AFFORDANCE_MAP`), implicit pattern matching (`_IMPLICIT_PATTERNS`), and legacy-to-category mapping — all applied to every query including "hello". The router was 1957 lines.
- **Why it happened:** Feature factory mentality (A1). Each new classification approach was added as a new "head" without evaluating whether the existing approach was insufficient.
- **What the rebuild does differently:** Three-stage fallback: (1) symbolic parser (regex, <1ms), (2) BERT classifier (if enabled, ~50ms), (3) LLM fallback (last resort, ~500ms). Stage 2 is only invoked if stage 1 confidence < threshold. Stage 3 is only invoked if stage 2 also fails. No ensemble voting, no weighted scoring. Accuracy is validated by AT-2 acceptance test.

**B.10.5 The Services Band-Aid**
- **What happened:** `services.py` was created as a typed dataclass container (`Services.from_atlas(atlas_instance)`) to extract attribute access from the god object. But it became a second indirection layer — components accessed other components via `self.services.memory_manager` instead of `self.memory`.
- **Why it happened:** Extracting initialization without extracting architecture. Moving references to a container doesn't fix coupling — it just adds indirection.
- **What the rebuild does differently:** No Services class. Each component receives its dependencies via constructor injection with typed parameters. Dependencies are explicit, typed, and visible in the constructor signature.

### B.11 Discoveries

Design decisions found during deep dive not captured in Volume 0:

**B.11.1 Speculation Scrubbing Pattern**
`answer_governor.py` (lines 62-108) implements a deterministic speculation scrubber using 30+ compiled regex patterns that replace hedging language ("likely due to" → "due to", "appears to be" → "is", "may be" → "is") and remove filler sentences ("Further investigation is recommended", "It seems..."). This is applied to every governed answer before delivery. Volume 0 P9 says "claims that cannot be grounded must be flagged as speculative" but does not describe the concrete mechanism. **Recommendation:** Promote to Volume 0 as an implementation note under P9.

**B.11.2 Evidence Contracts Pattern**
`evidence_contracts.py` defines 15 default `EvidenceContract` objects — a mapping from intent patterns (regex) to required evidence types and tools. Example: a file read intent MUST have `file_content` evidence from `file_read` tool; a code execution intent MUST have `execution_result` evidence. If required evidence is absent after the ReAct loop, the failure_action degrades authority (block_answer, flag_insufficient, or inject_disclaimer). This is a pre-condition pattern Volume 0 does not describe. **Recommendation:** Promote to Volume 0 as a design pattern under P9.

**B.11.3 Prompt Priority System**
`prompt_builder.py` implements a priority-based prompt assembly where context sections compete for a token budget (default 3500 tokens). Priorities from `SectionPriority`: IDENTITY=1 > KNOWLEDGE_CONTEXT=2 > FACTS=3 > DIALOGUE_CONTEXT=4 > LEARNED_PATTERNS=4 > FUNCTION_TOOLS=5 > RESEARCH_MODE=6 > MULTI_TURN=7 > EXAMPLES=8. When budget is exceeded, lower-priority sections are dropped first. This prevents the Attempt 3 problem where long conversation history pushed out relevant facts. **Recommendation:** Document in Volume 0 as a design pattern for prompt engineering.

**B.11.4 Premature Parallel Optimization**
Attempt 3's `memory_context.py` (line 23-26) uses a `ThreadPoolExecutor(max_workers=8)` and switches to parallel execution only above a 10K record threshold (`PARALLEL_THRESHOLD`). In the orchestrator itself, `asyncio.gather()` was used in 12+ locations for parallel subsystem calls, causing race conditions where memory context arrived after the LLM call had already started. The rebuild uses sequential orchestration for the critical path: parse intent → assemble context → generate response → govern output. Parallelism is permitted only for independent operations (e.g., logging to L3 while returning the response). **Recommendation:** Add to Volume 0 as anti-pattern A10.

**B.11.5 Crash Recovery via Interrupted Tasks**
`core/atlas_command_router.py` (lines 97-138) implements a crash guard pattern: if `process_command` throws, the error is (a) logged with full context, (b) persisted as a conversation message so follow-up messages retain context, and (c) stored via `InterruptedTaskManager` with `CrashPhase.PRE_ROUTING` for potential resumption. This pattern prevents the conversation from having a gap when the assistant crashes mid-response. The rebuild should preserve this crash-guard-and-persist pattern at the ConversationEngine boundary.

### B.12 Oversight Self-Review

**1. What would a programming agent still not know after reading this?**

Reviewed all sections. Identified and addressed the following gaps:
- **IntentCategory enum location:** The enum is referenced in UnifiedIntent (B.6.1) but its canonical location was not specified. Resolution: define in `orchestrator/schemas.py` and re-export from `shared/types.py`. Documented in agent-comm/vol-02.md.
- **ReAct prompt template content:** B.5 specifies the ReAct loop exists and B.10.3 describes the governance fix, but the actual prompt structure for think-act-observe is not specified. Resolution: the programming agent should use a standard ReAct prompt template ("Thought: ... Action: ... Observation: ...") with the specific tool schemas injected by `ToolRegistry.get_openai_schema_for_query()`. The prompt template belongs in `orchestrator/prompts.py` — specific wording is left to the programming agent as it depends on the chosen LLM's optimal prompting style.
- **Session lifecycle:** ConversationRequest has `session_id` but session creation/resumption logic is not detailed. Resolution: if `session_id` is None, the engine creates a new session via `MemoryManager.start_conversation()`. If provided, it resumes. Session expiry is a Vol 1 (Memory) concern.

**2. What failure modes from Attempt 3 are not explicitly prevented?**

All 5 A.4 items are explicitly addressed:

| A.4 Item | Prevention Mechanism | Verified In |
|---|---|---|
| A.4.1: God object | Max 500 lines per module, 4-module decomposition (B.10.1) | RT-1 regression test |
| A.4.2: "Hi atlas" fails | AT-1 acceptance test (single hello), RT-2 regression test (100 consecutive) | AT-1, RT-2 |
| A.4.3: Ungoverned output | All responses pass through AnswerGovernor.govern() (B.10.3), evidence contracts enforce grounding (B.11.2) | AT-3, RT-3 |
| A.4.4: Three meta-assessments | All three versions KILLED in B.4 scope triage | RT-4 (grep test) |
| A.4.5: Proactive disabled | DEFERRED to Phase 4+, gated behind feature flag, not imported in REBUILD scope (B.9.2) | RT-5 (import test) |

Additional Attempt 3 failure mode not in A.4 but addressed: **silent error swallowing** (50+ empty except blocks). B.7.4 explicitly forbids this pattern.

**3. Are there cross-volume dependencies that aren't documented?**

Two new dependencies discovered during deep dive:
- **IntentCategory enum:** Must be importable by Vol 3 (for correction records) and Vol 9 (for governance rules). Documented in agent-comm/vol-02.md.
- **ReAct schemas cross-reference:** The ReAct loop's tool calling uses `ToolRegistry.get_openai_schema_for_query()` (Vol 10). The schema format (OpenAI function calling format) should be explicitly documented. Flagged in agent-comm/vol-02.md.

All other dependencies are covered in shared-contracts §2.1-§2.7.

**4. Does the scope triage (B.4) have any omissions?**

B.4 was filled in Phase 1. Verified: 13 REBUILD + 8 DEFER + 56 KILL = 77 components, matching all files in A.2 Source Manifest. No omissions.

**5. Are the interface contracts (B.3) specific enough to code against?**

B.3 was filled in Phase 1 with method signatures, Pydantic schemas, and cross-volume summaries. Combined with the B.6 data model (field-level types, validators, constraints) and shared-contracts §2.1-§2.7, a programming agent has exact method signatures and schema definitions for all orchestrator interfaces. No ambiguity identified.

**6. Does every design decision support Atlas-level performance?**

Reviewed each major design choice against Jarvis-level vision:
- **ConversationRequest.device_id field** (B.6.3): Preserves multi-device path.
- **PersonalityTraits.frozen = True** (B.6.9): Immutable personality preserves identity consistency.
- **Sequential critical path** (B.11.4): Does NOT block real-time interaction — completes within the 30-second timeout. Streaming (SSE) provides incremental output during generation. Voice (Vol 6) will need an optimized path (~200ms budget) — this is intentionally DEFERRED.
- **Evidence contracts** (B.11.2): Scales to Jarvis-level because requirements can be extended per-domain without changing the core pipeline.
- **Crash recovery** (B.11.5): Preserves conversation continuity through failures, essential for a trusted assistant.
- **Potential limitation:** The current design does not specify multi-turn planning (breaking complex goals into sub-tasks across turns). This is intentionally DEFERRED — the autonomous executor handles multi-step tasks in Phase 4+.

### B.13 Design Quality Scorecard

**Existence Justification:**

- **EJ-1: Right to exist — 5/5.** Atlas cannot function without a conversation loop. The orchestrator is R1 (the first thing built) and the skeleton everything hangs on.

- **EJ-2: Scope discipline — 5/5.** Every component in the REBUILD scope has a concrete use case in the conversation loop. BERT, proactive, autonomous, meta-assessment are all DEFERRED or KILLED. No speculative features remain.

- **EJ-3: Not reinventing — 4/5.** The symbolic intent parser is genuinely novel (regex-based classification for a personal AI's command vocabulary). The ReAct loop pattern is established but evidence contracts integration is novel. Deducted 1 point because the prompt builder's priority system could potentially use an existing prompt management library.

**Design Fitness:**

- **DF-1: Attempt 3 lessons applied — 5/5.** Every A.4 failure has a structural prevention mechanism (B.12 question 2). The god object is decomposed (500-line max), "hi atlas" is acceptance-tested (AT-1, RT-2), output is governed (AT-3, RT-3), meta-assessments are killed (RT-4), proactive is deferred (RT-5). Silent error swallowing is forbidden (B.7.4).

- **DF-2: Integration-first — 5/5.** The orchestrator works end-to-end with memory (Vol 1) + governance (Vol 9) + tools (Vol 10). All dependencies are through shared-contracts interfaces with exact signatures. AT-1 proves the full loop works against the live server.

- **DF-3: Evolvability — 4/5.** Extension points: device_id enables multi-device, feature flags gate BERT and proactive, IntentCategory enum is extensible, evidence contracts can be added per-domain. Deducted 1 point because the sequential critical path may need revisiting for real-time voice interaction (Vol 6) where latency budgets are ~200ms.

**Buildability:**

- **BA-1: Specification completeness — 5/5.** Every Pydantic schema has field-level types and validators. Every error type has recovery strategy. Every interface has method signatures.

- **BA-2: Testability — 5/5.** AT-1 through AT-4 have concrete inputs and expected outputs. RT-1 through RT-5 are mechanically verifiable.

- **BA-3: Size budget — 4/5.** The REBUILD scope is 4 modules with 500-line max each (~1500-2000 lines total). Proportional to value. Deducted 1 point because PersonalityTraits config loading adds a small but non-trivial configuration surface.

**Overall: 42/45** — Passing (minimum 30/45).

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (70+ code files, 30+ docs), context brief, and 5 known failure warnings including god-object orchestrator and unreliable "hi atlas" | Created the orchestrator analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V02-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 source manifest per DISTILLATION_PROTOCOL.md Section 5 | Tagged files as essential vs. nice-to-have for the rebuild analysis |
| v5 | 2026-03-10 | Oz (Vol 2 distillation) | Filled B.1-B.4: Subsystem Purpose, Architecture Overview (6 components + data flow), Interface Contracts (5 component contracts + cross-volume summary), Scope Triage (13 REBUILD, 8 DEFER, 56 KILL) | Completed the design analysis for the conversation engine |
| v6 | 2026-03-11 | Phase 2 Distillation Agent | Phase 2 distillation — B.5-B.13: 9 Pydantic schemas (B.6), 4 error types with recovery (B.7), 4 acceptance tests + 5 regression tests (B.8), 10 env vars + 2 feature flags (B.9), 5 subsystem lessons (B.10), 5 discoveries including speculation scrubbing, evidence contracts, and crash recovery (B.11), full oversight self-review addressing all 5 A.4 items (B.12), scorecard 42/45 (B.13) | Completed the deep technical specification for the orchestrator — defined all data structures, error handling, tests, configuration, lessons from past mistakes, and scored 42/45 on quality |
