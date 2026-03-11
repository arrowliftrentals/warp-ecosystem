# ATLAS Design Bible — Volume 2: Orchestrator & Conversation Loop

| Field | Value |
|---|---|
| **Doc ID** | `DB-V02-001` |
| **Name** | Volume 2: Orchestrator & Conversation Loop |
| **Purpose** | Design specification for the central conversation engine — intent parsing, routing, response generation, and personality |
| **Owner** | Design Bible / Volume 2 |
| **Status** | `phase-2-complete` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / TBD distillation agent (Part B) |
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

**1. Pydantic v2** — All inter-component data crosses boundaries as validated Pydantic `BaseModel` instances. The schemas in B.3 and B.6 are the single source of truth for data shapes. Pydantic v2's Rust-backed validation is required (not v1) for performance in the per-message pipeline. Volume 0 P8 mandates this.

**2. structlog** — Structured logging replaces the Attempt 3 loguru dependency. Every pipeline stage logs with bound context (`session_id`, `intent_category`, `phase`) so that request traces are reconstructable from logs alone (R8: observable and debuggable). The existing codebase uses `structlog.get_logger()` with `structlog.stdlib.BoundLogger` throughout.

**3. asyncio** — `ConversationEngine.process_message()` is `async`. LLM calls, memory queries, and tool execution are I/O-bound and benefit from async concurrency. Each pipeline stage (parse → context → generate → govern) is independently awaitable. The existing `atlas.py` already uses `async def` throughout — this is continuation, not introduction.

**4. PyTorch (optional, ML tier only)** — The BERT intent classifier (`bert_classifier.py`) requires `torch` and `transformers` for model loading. This dependency is optional: when unavailable, `IntentParser` skips the ML tier and falls directly to LLM fallback. The system must operate correctly with ML disabled (`ML_ENABLED=false`). Per P1, ML only advises.

**5. pydantic-settings** — Configuration loading uses a `BaseSettings` subclass for environment variable binding with type validation and defaults. Replaces the scattered `os.environ.get()` calls across Attempt 3.

**6. No ORM** — The orchestrator does not interact with databases directly. All persistence flows through Vol 1 (Memory) interfaces. The orchestrator is stateless per-request.

**Rejected alternatives:**
- **LangChain / LlamaIndex:** Rejected per R6 (model independence). These frameworks couple to specific LLM provider APIs. The orchestrator uses a thin `LLMProvider` abstraction instead.
- **FastAPI dependency injection:** Rejected for intra-component wiring. FastAPI's `Depends()` is a request-scoped pattern for HTTP handlers (Vol 8's domain). The orchestrator uses constructor injection.
- **loguru:** Used in some Attempt 3 modules, but the rebuild standardizes on structlog for structured output and stdlib compatibility.

### B.6 Data Model

All schemas are defined in `contracts/orchestrator_schemas.py` and imported by any module that needs them. No module defines ad-hoc dicts for cross-boundary data.

**1. UnifiedIntent** (from B.3 §3.2 — canonical intent representation):
- `category: IntentCategory` — Enum with 320 values from the intent taxonomy
- `domain: IntentDomain` — Auto-derived from category (conversation, memory, tool, system, learning)
- `confidence: float` — 0.0–1.0, computed by the classification tier that produced this intent
- `action: str | None` — Primary action verb (e.g., "search", "create", "explain")
- `target: str | None` — Primary target noun (e.g., "file", "memory", "status")
- `entities: list[ExtractedEntity]` — Named entities extracted from the command
- `raw_command: str` — Original unmodified user text
- `needs_llm: bool` — Whether response generation requires an LLM call
- `classification_source: str` — Which tier: `"symbolic"`, `"bert"`, `"llm"`, `"hybrid"`
- **Validator:** `confidence` must be ≥ 0.1 for `bert`/`llm` sources (below that, the classification is noise)

**2. ExtractedEntity:**
- `name: str` — Entity name (e.g., "filename", "date_range", "project_name")
- `value: str` — Extracted value
- `entity_type: str` — Type classification (e.g., "PATH", "DATE", "IDENTIFIER")
- `span: tuple[int, int] | None` — Character offsets in the original command
- `confidence: float` — Extraction confidence (1.0 for regex, lower for ML)

**3. ConversationRequest** (from B.3 §3.1):
- `query: str` — User message text (`min_length=1`). Field name is `query` everywhere per shared contract C-17.
- `session_id: str` — Session identifier (default: generated UUID)
- `device_id: str` — Source device identifier (default: "default")
- `stream: bool` — Enable streaming (default: `False`). Presence of this flag per shared contract C-12.

**4. ConversationResponse** (from B.3 §3.1):
- `session_id: str`
- `response: str` — Governed response text
- `intent: ResolvedIntent` — Resolved intent (subset of UnifiedIntent safe for serialization)
- `evidence_refs: list[str]` — EvidenceItem IDs grounding the response
- `authority_level: AuthorityLevel` — Governance authority classification
- `confidence: float` — Overall response confidence (0.0–1.0)
- `actions_taken: list[str]` — Actions performed during response generation
- `metadata: ResponseMetadata`

**5. MemoryContext** (from B.3 §3.4):
- `recent_episodes: list[dict]` — L3 episodic memory (max 5, current session)
- `relevant_facts: list[dict]` — L4 declarative facts (keyword-matched)
- `validated_skills: list[dict]` — L5 procedural skills
- `active_goals: list[dict]` — L8 goal memory
- `user_preferences: dict` — L9 social/preference data
- `vector_matches: list[dict]` — L10 semantic search matches
- **Constraint:** Total token count of serialized context must not exceed `MAX_CONTEXT_TOKENS` (configurable, default 4096)

**6. RawResponse** (from B.3 §3.3):
- `content: str` — Raw response text before governance
- `phase: OutputPhase` — Enum: `DETERMINISTIC`, `REACT`, `LLM_DIRECT`
- `evidence_store: EvidenceStore | None` — Evidence collected during tool execution
- `tool_calls: list[ToolCallRecord]` — Tools invoked during response generation
- `model_used: str | None` — LLM model identifier, or `None` for deterministic responses

**7. PersonalityTraits** (from B.3 §3.5):
- Seven float traits (`proactivity`, `verbosity`, `formality`, `assertiveness`, `humor`) each 0.0–1.0
- Three boolean flags (`ask_before_action`, `explain_reasoning`, `terse_data_mode`)
- **Frozen:** `model_config = ConfigDict(frozen=True)` — immutable at runtime per P10

**8. ResponseMetadata:**
- `processing_time_ms: float` — Wall-clock time from request to response
- `intent_classification_source: str` — Which tier classified the intent
- `llm_calls: int` — Number of LLM calls made during this request
- `tools_invoked: list[str]` — Tool names invoked
- `memory_layers_consulted: list[str]` — Which memory layers were queried
- `governance_applied: bool` — Whether AnswerGovernor was active

**9. ToolCallRecord:**
- `tool_name: str` — Tool identifier
- `arguments: dict` — Arguments passed to the tool
- `result: dict` — Tool execution result
- `execution_time_ms: float` — Execution duration
- `validated: bool` — Whether DecisionValidator approved this call

**ReAct-specific schemas** (internal to ResponseGenerator):
- `ThinkStep`, `ActStep`, `ObserveStep`, `ReflectStep`, `AnswerStep` — One Pydantic model per ReAct phase. Each includes `phase: str`, `content: str`, `iteration: int`. `ActStep` additionally includes `tool_name: str`, `arguments: dict`. All ReAct LLM outputs are parsed via `model_validate_json()` — unparseable outputs trigger a retry with explicit format instructions (max 2 retries, then fallback to direct LLM response without tool use).

**Shared contract bindings:**
- `ConversationRequest.query` field name satisfies C-17 (field name is `query` everywhere)
- `ConversationRequest.stream` field satisfies C-12 (single endpoint with stream flag)
- `ConversationResponse` maps to `ChatResponse` at Vol 8's boundary per C-13
- Orchestrator schemas live in `contracts/orchestrator_schemas.py` per shared-contracts Section 1.6

### B.7 Error Handling

**Error taxonomy (6 types, all subclass `AtlasError` from `shared/errors.py`):**

**1. `IntentParseError`** — All three classification tiers failed. Trigger: symbolic returns no match, BERT is unavailable or below threshold, LLM returns unparseable output or times out. Recovery: return a `UnifiedIntent` with `category=GENERAL_CONVERSATION`, `confidence=0.0`, `classification_source="fallback"`. The user gets a generic conversational response. Never silent — the error is logged with full context (R8).

**2. `MemoryContextError`** — Memory layer queries fail (Vol 1 unavailable, timeout, or schema validation failure on returned data). Recovery: `MemoryContext` with all fields as empty lists/dicts. The pipeline continues without context enrichment. The response will be less contextual but still valid. Logged as warning with which layers failed.

**3. `LLMProviderError`** — The LLM provider returns an error, times out, or returns malformed output. Recovery depends on pipeline phase: (a) during intent classification → fall back to next tier or `IntentParseError`; (b) during response generation → return a deterministic "I'm unable to process that right now" response with `authority_level=NONE`. Never retry more than once (cost control).

**4. `GovernanceError`** — The `AnswerGovernor` (Vol 9) fails or returns invalid output. Recovery: the response is marked with `authority_level=UNVERIFIED` and delivered with a metadata flag. Governance failure never blocks response delivery — the user always gets a response. Design trade-off: availability over governance strictness, with full auditability.

**5. `ToolExecutionError`** — A tool invoked during ReAct fails. Recovery: the `ObserveStep` records the failure, and the ReAct loop's `ReflectStep` decides whether to retry, try a different tool, or answer without the tool result. Max 2 tool retries per iteration. If all tools fail, the response is generated from available context without tool results.

**6. `PipelineTimeoutError`** — The entire `process_message` pipeline exceeds `REQUEST_TIMEOUT_SECONDS` (default 30). Recovery: return whatever partial result is available (if response generation completed, return ungoverned response; if only intent parsing completed, return a timeout message).

**Crash-guard pattern (from Attempt 3, preserved):**
`ConversationEngine.process_message()` wraps the entire pipeline in a top-level exception handler. Any uncaught exception produces a safe `ConversationResponse` with `response="I encountered an unexpected error. Please try again."`, `authority_level=NONE`, and the exception logged with full stack trace. This guarantees the user always gets a response (R1: working conversation loop). The crash guard catches `BaseException` to also handle `asyncio.CancelledError`.

**What is NOT tolerated:**
- Silent exception swallowing (`except: pass`). The existing codebase has 50+ instances. Every exception is logged with context. The `AtlasError` hierarchy ensures structured error information.
- Bare `raise Exception(...)`. All errors use typed exceptions with structured fields.
- Missing error context. Every error includes `session_id`, `phase` (which pipeline stage), and `elapsed_ms`.

### B.8 Testing Strategy

**Acceptance tests (5 tests — these gate everything):**

1. **MVA-1: "Hi Atlas" round-trip** — Send `"Hi Atlas"` via `ConversationEngine.process_message()`. Assert: returns `ConversationResponse` with non-empty `response`, `intent.category` is `GREETING` or `GENERAL_CONVERSATION`, `confidence > 0.0`, completes within 5 seconds. This is the single gate for the entire subsystem — nothing else ships until this passes.

2. **MVA-1: Empty input rejection** — Send `""` via `process_message`. Assert: returns a valid `ConversationResponse` with a polite rejection message (not a crash, not a 500, not silence). Validates the `query: str = Field(..., min_length=1)` constraint.

3. **MVA-1: Intent classification three-tier** — Send a known command (e.g., `"show status"`). Assert: `classification_source` is `"symbolic"`. Disable symbolic parser, resend. Assert: `classification_source` is `"bert"` or `"llm"`. Validates the fallback chain.

4. **MVA-1: Memory context integration** — Send a message in a session with prior messages stored. Assert: `metadata.memory_layers_consulted` is non-empty. Validates Vol 1 integration.

5. **MVA-1: Governance pass-through** — Send a message and assert `authority_level` is present in the response. Initially `ADVISORY` (pass-through governor). Validates the Vol 9 integration point exists.

**Integration tests (4 tests):**

1. **Vol 1 boundary** — `ConversationEngine` calls `MemoryManager.start_conversation()`, `add_message()`, and `get_conversation()` across a full request lifecycle. Assert session persistence.
2. **Vol 9 boundary** — `ConversationEngine` calls `DecisionValidator.validate()` before tool execution and `AnswerGovernor.govern()` before response return. Assert both are called with correct schemas.
3. **Vol 10 boundary** — During a ReAct request, `ToolRegistry.execute()` is called with the correct tool name and arguments. Assert the tool result appears in the response.
4. **Vol 8 boundary** — The API route handler calls `process_message()` and serializes `ConversationResponse` to `ChatResponse` (C-13 mapping).

**Unit tests (7+ categories):**

1. **IntentParser symbolic tier** — Grammar matching for each verb set (conversation, memory, system, learning). At least one test per `IntentCategory` domain.
2. **IntentParser fallback** — Three-tier cascade: symbolic miss → BERT (if available) → LLM fallback → `IntentParseError` (all fail).
3. **ResponseGenerator deterministic** — Simple intents (greeting, status) produce template responses without LLM calls.
4. **ResponseGenerator ReAct** — Multi-step reasoning with mocked tool calls. Pydantic schema validation at each ReAct phase.
5. **MemoryContextRetriever** — Mock Vol 1 layer queries. Verify `MemoryContext` schema output and token budget enforcement.
6. **PersonalityManager** — Personality loading, system prompt generation, and `frozen=True` enforcement.
7. **Error paths** — Each of the 6 error types in B.7 has at least one unit test verifying the recovery behavior.

**Regression tests (3 tests — one per A.4 failure):**

1. **A.4.1 regression: God-object decomposition** — Assert `engine.py` is ≤ 400 lines and imports from `intent.py`, `response.py`, `personality.py` as separate modules. Structural test, not behavioral.
2. **A.4.2 regression: "Hi Atlas" never fails** — Run the MVA-1 acceptance test 100 times in a loop. Assert 100% pass rate.
3. **A.4.4 regression: No duplicate meta-assessment** — Assert no module matching `meta_assessment*.py` exists in the orchestrator directory. Structural test preventing the v1/v2/v3 recurrence.

### B.9 Configuration

All configuration is defined in a single `OrchestratorConfig` Pydantic `BaseSettings` subclass. Environment variables bind automatically via pydantic-settings. Every field has a default that makes the system work without any env vars set.

**Fields (12):**

1. `REQUEST_TIMEOUT_SECONDS: float = 30.0` — Maximum wall-clock time for `process_message()`.
2. `MAX_CONTEXT_TOKENS: int = 4096` — Maximum tokens for serialized `MemoryContext` injected into prompts.
3. `MAX_REACT_ITERATIONS: int = 5` — Hard cap on ReAct loop iterations.
4. `REACT_ITERATION_TIMEOUT: float = 10.0` — Per-iteration timeout within the ReAct loop.
5. `ML_ENABLED: bool = False` — Whether the BERT classifier tier is active. Default `False` — the system must work without ML (P1). Set `True` only when BERT model is deployed and validated.
6. `BERT_CONFIDENCE_THRESHOLD: float = 0.7` — Minimum BERT confidence to accept an ML classification. Below this, the classification is discarded and LLM fallback is used.
7. `LLM_FALLBACK_MODEL: str = "gpt-4o-mini"` — Model for LLM-based intent classification (cheapest capable model).
8. `RESPONSE_MODEL: str = "gpt-4o"` — Model for response generation. Separate from classification to allow cost optimization.
9. `PERSONALITY_FILE: str = "config/personality.yaml"` — Path to personality definition file. Default loads Jarvis personality.
10. `GOVERNANCE_ENABLED: bool = True` — Whether `AnswerGovernor` is called. When `False`, responses bypass governance (development only). Default `True` because P9 mandates output governance.
11. `LOG_LEVEL: str = "INFO"` — structlog log level.
12. `MAX_LLM_RETRIES: int = 1` — Maximum retries for a failed LLM call (cost control).

**Design invariant:** The system must produce valid `ConversationResponse` output with `ML_ENABLED=False`, `GOVERNANCE_ENABLED=True`, and no LLM provider configured (pure symbolic + deterministic templates). This is the minimum viable configuration.

### B.10 Subsystem Lessons Learned

**Lesson 1: The god-object is the root cause, not a symptom.**
`atlas.py` at 2,800+ lines (the `core/atlas.py` shim re-exports from `core/` but the real file is larger) was the primary integration failure. Every new feature was added as a method on the `Atlas` class: intent parsing, response generation, tool execution, personality management, streaming, error recovery, confirmation flows, proactive suggestions. With 50+ methods and 200+ lines of `__init__` wiring, the class became untestable in isolation. The rebuild decomposes into 5 focused modules (engine, intent, response, personality, memory_context) with the engine at ≤ 400 lines. The critical insight: the god-object pattern made it impossible to test conversation without also initializing ML models, tool registries, and memory backends — so nothing got tested.

**Lesson 2: Intent conflation broke routing.**
The original `IntentType` enum had 9 values for 70+ distinct user intents. `intent_router.py` (1,957 lines) compensated with nested `if/elif` chains, contraction expansion, implicit pattern matching, and "affordance mapping." This was a tax on wrong abstraction: starting with 9 types and expanding to 320 patterns incrementally created routing spaghetti where adding a new intent required modifying 6 functions. The rebuild starts with `IntentCategory` (320 values) as the target taxonomy from day one, with clean routing via dictionary dispatch.

**Lesson 3: Exception swallowing created invisible failures.**
50+ exception handlers use `except Exception: pass` or `except Exception as e: logger.debug(...)`. The `_handle_error_gracefully` method catches all exceptions and returns a generic "I encountered an error" response — correct for the user-facing path — but suppresses diagnostics needed to find root causes. The "Hi Atlas" failure (A.4.2) was insidious: it would sometimes work, sometimes silently fail, with no error in logs because the exception was swallowed at a higher level. The rebuild enforces: every exception logged with `session_id`, `phase`, `elapsed_ms`. No bare `except:`. The crash-guard catches at the top level but always logs the full stack trace.

**Lesson 4: Meta-assessment scope creep as A1 violation.**
Three versions (`meta_assessment.py`, `meta_assessment_v2.py`, `meta_assessment_v3.py`) exist because each was a "quick experiment" never cleaned up. Textbook feature-factory anti-pattern (A1 from Volume 0). None tested. None wired into the main pipeline. ~2,000 lines of dead code collectively. The rebuild kills all three. If meta-assessment is needed, it goes through the DEFER process with a design document.

**Lesson 5: Fragmented prompt construction caused inconsistency.**
Three separate files handled prompts: `prompt_builder.py` (priority-based section builder), `prompt_constants.py` (raw string templates), and `prompts.py` (more raw string templates). The `prompt_builder.py` design — `SectionPriority` enum with `CRITICAL/HIGH/MEDIUM/LOW`, token budgeting, dynamic section selection — was architecturally sound. But the other two files duplicated and contradicted sections, so the actual prompt depended on which file's constants were imported. The rebuild co-locates all prompt construction in `response.py`'s `SystemPromptBuilder`, using the `SectionPriority` pattern as the single source.

**Lesson 6: Ungoverned ReAct LLM calls violated P9.**
ADR-0031 identifies 4 LLM call sites in the ReAct engine that bypass `AnswerGovernor`. The phases (THINK, ACT, OBSERVE, REFLECT) each make independent LLM calls, but only the final ANSWER phase was designed to pass through governance. Intermediate reasoning steps can produce ungrounded claims that influence the final answer without evidence tracking. The rebuild requires: every ReAct phase that produces user-visible text passes through governance. Tool results are stored in `EvidenceStore` for grounding. Non-user-visible reasoning (THINK, REFLECT) is logged but not governed (governance applies to output, not internal reasoning).

### B.11 Discoveries

Findings from the source code that were not documented and are not obvious from existing architecture documents.

**Discovery 1: Disambiguation is more sophisticated than documented.**
`intent_router.py` contains a ~200-line `_disambiguate_intent` method that scores multiple candidate intents against conversation history, active goals (L8), and entity overlap. Not mentioned in any architecture document. The disambiguation logic is valuable — it prevents the "last match wins" problem — but is buried in the router's monolithic structure. The rebuild preserves this as a scoring function within `IntentParser`, exposed as `_score_candidates(candidates: list[UnifiedIntent], context: MemoryContext) -> UnifiedIntent`.

**Discovery 2: EvidenceStore has built-in capacity management.**
`evidence_store.py` implements an `EvidenceStore` with `max_items` (default 100) and automatic eviction of lowest-confidence items when the cap is reached. Designed for ReAct loops that accumulate many tool results. The capacity management logic is correct and the eviction policy (lowest confidence first, then oldest) is reasonable. This must be preserved in the Vol 9 governance rebuild.

**Discovery 3: Recency bias in prompt building is a deliberate trick.**
`prompt_builder.py` (~line 180) has a comment: "Recent episodes get 3x weight in token budget." Intentional design choice: the most recent conversation turns are always included even when the token budget is tight, while older context is truncated. The heuristic works well for conversational coherence but is undocumented. The rebuild preserves this 3x weight and adds it to `OrchestratorConfig` as `RECENCY_WEIGHT_MULTIPLIER: float = 3.0`.

**Discovery 4: A regex-based speculation scrubber exists.**
`response_validator.py` contains a `_scrub_speculation` method using regex patterns to detect and downgrade speculative language ("I think", "probably", "might be", "it seems like") in LLM responses. Predates ADR-0031's formal governance pipeline but implements a lightweight speculation detection. The patterns are worth preserving as a pre-governance filter in ResponseGenerator, before the full `AnswerGovernor` pipeline.

**Discovery 5: Sync/async boundary management is fragile.**
`atlas.py` has a `_ensure_async` wrapper converting synchronous methods to async via `asyncio.to_thread()`. Exists because some Vol 1 memory and Vol 10 tool operations are synchronous while the pipeline is async. The wrapper works but creates subtle bugs when synchronous code accesses shared state. The rebuild defines a clear contract: all Vol 1 and Vol 10 interfaces are `async def`. If the underlying implementation is synchronous, the owning volume wraps it — the orchestrator never calls `to_thread()` on external interfaces.

**Discovery 6: Per-phase model selection is already partially implemented.**
`atlas_llm.py` contains `_select_model_for_phase` choosing different LLM models for different pipeline phases: cheapest for intent classification, mid-tier for ReAct reasoning, most capable for final response generation. Sound cost optimization but hardcodes model names. The rebuild preserves the concept via config: `LLM_FALLBACK_MODEL` (cheapest, classification), `RESPONSE_MODEL` (most capable, generation). ReAct reasoning model matches `RESPONSE_MODEL` by default but can be overridden.

### B.12 Oversight Self-Review

**A.4 items disposition (every item must be mentioned):**

**A.4.1 — "The orchestrator is a god object":** ADDRESSED in B.2 and B.4. The 2,800-line `atlas.py` is decomposed into 5 focused modules: `engine.py` (≤ 400 lines, pipeline orchestration only), `intent.py` (three-tier parsing), `response.py` (generation + ReAct + prompt building), `personality.py` (personality loading + caching), `memory_context.py` (memory retrieval). The engine delegates — it does not handle. B.8 includes a structural regression test (A.4.1 regression) asserting `engine.py` stays ≤ 400 lines.

**A.4.2 — "Hi Atlas fails":** ADDRESSED as the primary acceptance test. MVA-1 Test 1 in B.8 sends "Hi Atlas" and asserts a valid `ConversationResponse` with non-empty `response` and completion within 5 seconds. Regression test runs this 100 times asserting 100% success. The crash-guard pattern in B.7 guarantees the user always gets a response even if internal components fail.

**A.4.3 — "Ungoverned output":** ADDRESSED in B.2, B.4, and B.7. The `OutputGovernor` is an integration point in the pipeline (B.2 data flow, step 4). Vol 2 calls `AnswerGovernor.govern()` (owned by Vol 9). Initial implementation is a pass-through returning `authority_level=ADVISORY`. The DEFER decision in B.4 schedules the full governance pipeline for Tier 4. `GovernanceError` in B.7 ensures governance failure never blocks response delivery. MVA-1 Test 5 validates the integration point exists.

**A.4.4 — "Three meta-assessments":** ADDRESSED in B.4 (KILL) and B.10 (Lesson 4). All three versions killed. B.8 includes a structural regression test asserting no `meta_assessment*.py` exists in the orchestrator directory.

**A.4.5 — "Proactive system disabled":** ADDRESSED in B.4. `proactive_component.py`, `proactive_engine.py`, `proactive_executor.py` are KILLed. Three modules for a permanently-disabled feature violates P7. Revisit as DEFER post-MVA if proactive capabilities are prioritized.

**Oversight questions:**

**Q1: Does the decomposition actually solve the god-object, or just scatter it?**
Each module has a single responsibility: `engine.py` orchestrates, `intent.py` classifies, `response.py` generates, `personality.py` manages personality, `memory_context.py` retrieves context. Each has a single public entry point and communicates via Pydantic schemas. Scatter risk is mitigated by the rule that `ConversationEngine` is the ONLY public entry point — no external module bypasses the engine to call `IntentParser` directly.

**Q2: Is the three-tier intent cascade over-engineered for MVA-1?**
For MVA-1, only the symbolic tier is required. BERT and LLM tiers are behind config flags (`ML_ENABLED`, LLM fallback activates only when symbolic and BERT both fail). The three-tier design is not over-engineering — it is the target architecture with graceful degradation. MVA-1 runs with tier 1 only.

**Q3: Does DEFERring governance (Tier 4) violate P9?**
Strictly, yes — P9 says "output governance, not just action governance." Mitigation: the integration point exists from day one (B.2 step 4, B.3 §3.1 `authority_level` field), and the pass-through governor returns `ADVISORY` instead of silently omitting governance. The user-visible response always includes governance metadata. Full governance activates at Tier 4 without architectural changes.

**Q4: What happens when Vol 1 (Memory) is completely unavailable?**
`MemoryContextError` in B.7 handles this: pipeline continues with empty context. Session management degrades to stateless. The response is less contextual but the user still gets a valid response. Correct degradation — the conversation loop (R1) must work even without memory.

**Q5: Is the ReAct loop's 5-iteration cap sufficient?**
Configurable (`MAX_REACT_ITERATIONS`). 5 chosen based on `react_engine.py` observation: longest successful chains are 3–4 iterations. Each iteration has its own timeout (`REACT_ITERATION_TIMEOUT`). If total exceeds `REQUEST_TIMEOUT_SECONDS`, the pipeline timeout fires first.

**Q6: Are there shared contract violations?**
Verified against `gate-output/shared-contracts.md`:
- C-12 (single endpoint with stream flag): Satisfied — `ConversationRequest.stream` field exists.
- C-13 (ConversationResponse → ChatResponse mapping): Vol 8's responsibility. Vol 2 returns `ConversationResponse`; mapping documented in B.3 §3.1.
- C-17 (field name is `query`): Satisfied — `ConversationRequest.query`, not `message` or `input`.
- Section 1.6 (orchestrator schemas in `contracts/`): Satisfied — B.6 specifies `contracts/orchestrator_schemas.py`.
- Sections 2.1–2.4 (cross-volume interfaces): All documented in B.3 §3.6.

### B.13 Design Quality Scorecard

| Criterion | Points | Score | Justification |
|---|---|---|---|
| **B.1 clarity** | /5 | 5 | Purpose statement defines exact scope, rebuild constraints, and governing principles. Measurable: ≤ 1,500 lines total. |
| **B.2 completeness** | /5 | 5 | All 6 components specified with responsibilities. Data flow diagram. Key architectural decisions stated. |
| **B.3 contract precision** | /5 | 5 | All 5 component contracts have typed method signatures, Pydantic schemas, and cross-volume dependency lists. |
| **B.4 scope triage rigor** | /5 | 4 | 13 REBUILD / 8 DEFER / 56 KILL with rationale. Deduction: DEFER boundary for governance (Tier 4) could be more precise about which features land in which tier. |
| **B.5 technology justification** | /5 | 4 | 6 choices with rationale and 3 rejected alternatives. Deduction: no performance benchmarks for Pydantic v2 vs v1 validation overhead. |
| **B.6 schema coverage** | /5 | 5 | 9 schemas + ReAct phase schemas. All cross-boundary data has Pydantic models. Shared contract field names verified. |
| **B.7 error coverage** | /5 | 5 | 6 typed errors with specific recovery strategies. Crash-guard preserves R1. No silent failures. |
| **B.8 test coverage** | /5 | 5 | 5 acceptance + 4 integration + 7+ unit categories + 3 regression tests. MVA-1 gates everything. A.4 items have regression tests. |
| **B.12 oversight** | /5 | 4 | All 5 A.4 items addressed. 6 oversight questions with honest assessments. Deduction: Q3 (governance DEFER vs P9) acknowledges tension without stronger resolution. |
| **TOTAL** | /45 | **42** | |

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (70+ code files, 30+ docs), context brief, and 5 known failure warnings including god-object orchestrator and unreliable "hi atlas" | Created the orchestrator analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V02-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 source manifest per DISTILLATION_PROTOCOL.md Section 5 | Tagged files as essential vs. nice-to-have for the rebuild analysis |
| v5 | 2026-03-10 | Oz (Vol 2 distillation) | Filled B.1-B.4: Subsystem Purpose, Architecture Overview (6 components + data flow), Interface Contracts (5 component contracts + cross-volume summary), Scope Triage (13 REBUILD, 8 DEFER, 56 KILL) | Completed the design analysis for the conversation engine |
| v6 | 2026-03-11 | Oz (Vol 2 Phase 2 distillation) | Filled B.5-B.13: Technology Choices (6 choices + 3 rejected), Data Model (9 Pydantic schemas + ReAct schemas + shared contract bindings), Error Handling (6 typed errors + crash-guard), Testing Strategy (5 acceptance + 4 integration + 7+ unit + 3 regression), Configuration (12 fields via pydantic-settings), Subsystem Lessons Learned (6 lessons from god-object/intent conflation/exception swallowing/meta-assessment/prompt fragmentation/ungoverned ReAct), Discoveries (6 undocumented findings), Oversight Self-Review (all 5 A.4 items + 6 oversight questions), Design Quality Scorecard (42/45). Status updated to phase-2-complete. | Deep-dived into all 77 source files and completed the full design specification for the conversation engine rebuild |
