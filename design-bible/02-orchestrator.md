# ATLAS Design Bible — Volume 2: Orchestrator & Conversation Loop

| Field | Value |
|---|---|
| **Doc ID** | `DB-V02-001` |
| **Name** | Volume 2: Orchestrator & Conversation Loop |
| **Purpose** | Design specification for the central conversation engine — intent parsing, routing, response generation, and personality |
| **Owner** | Design Bible / Volume 2 |
| **Status** | `draft` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / Distillation Agent V2 (Part B) |
| **Version** | v5 |
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
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 source manifest per DISTILLATION_PROTOCOL.md Section 5 | Tagged files as essential vs. nice-to-have for the rebuild analysis |
| v5 | 2026-03-10 | Oz (Vol 2 distillation) | Filled B.1-B.4: Subsystem Purpose, Architecture Overview (6 components + data flow), Interface Contracts (5 component contracts + cross-volume summary), Scope Triage (13 REBUILD, 8 DEFER, 56 KILL) | Completed the design analysis for the conversation engine |
