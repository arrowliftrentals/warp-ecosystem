# Agent Communication — Volume 2: Orchestrator
## Phase 2 Distillation Outputs

---

## Ownership Claims

```
CLAIM: Orchestrator-domain Pydantic schemas (UnifiedIntent, ExtractedEntity, ConversationRequest, ConversationResponse, MemoryContext, RawResponse, ToolCallRecord, ResponseMetadata, PersonalityTraits)
OWNER: Volume 2
REASON: Per shared-contracts §1.6, orchestrator schemas are defined in orchestrator/schemas.py and owned by Volume 2.
CONTESTED: no
```

```
CLAIM: IntentCategory enum (320 values) and ClassificationSource enum
OWNER: Volume 2 (canonical definition); re-exported from shared/types.py for Vol 3 and Vol 9 consumption
REASON: IntentCategory is the central taxonomy for all user intent classification. Defined in orchestrator/schemas.py. Vol 3 imports for correction records, Vol 9 imports for governance rules.
CONTESTED: no
```

```
CLAIM: IntentParser (symbolic regex-based intent classification)
OWNER: Volume 2
REASON: Deterministic intent parsing using CommandGrammar (~30 compiled regex patterns). Core REBUILD component per B.4.
CONTESTED: no
```

```
CLAIM: ConversationEngine (main conversation loop coordinator)
OWNER: Volume 2
REASON: Orchestrates parse→context→generate→govern pipeline. Replaces Attempt 3's Atlas god object. <300 lines.
CONTESTED: no
```

```
CLAIM: ResponseGenerator (LLM response generation + governance integration)
OWNER: Volume 2
REASON: Calls LLMProvider for generation, passes output through Vol 9 AnswerGovernor. REBUILD component per B.4.
CONTESTED: no
```

```
CLAIM: PromptBuilder (priority-based prompt assembly with token budgeting)
OWNER: Volume 2
REASON: Assembles system prompts with SectionPriority ordering (IDENTITY=1 through EXAMPLES=8). Token budget enforcement prevents context overflow.
CONTESTED: no
```

```
CLAIM: PersonalityTraits configuration and loading
OWNER: Volume 2
REASON: Personality defines tone, verbosity, formality for the orchestrator's response style. Loaded from config/personality.yaml. Note: Attempt 3 uses a dataclass; rebuild converts to Pydantic BaseModel with frozen=True.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 2 (Orchestrator) needs MemoryManager.assemble_context() from Volume 1 (Memory)
STATUS: pending
INTERFACE: async def assemble_context(session_id: str, query: str, max_tokens: int = 4096) -> MemoryContext. Vol 1 owns the implementation; Vol 2 consumes the returned MemoryContext.
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs AnswerGovernor.govern() from Volume 9 (Governance)
STATUS: pending
INTERFACE: async def govern(raw: RawResponse, intent: UnifiedIntent, evidence: EvidenceStore) -> GovernedOutput. Vol 9 owns GovernedOutput schema and governance logic. Vol 2 passes all LLM output through this before delivery.
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs ToolRegistry from Volume 10 (Tools)
STATUS: pending
INTERFACE: ToolRegistry.get_openai_schema_for_query(query: str) -> list[dict] and ToolRegistry.execute(tool_name: str, args: dict) -> ToolResult. Used by the ReAct loop to discover and invoke tools. Schema format: OpenAI function calling JSON.
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs AtlasError base class from shared/errors.py (Volume 8)
STATUS: pending
INTERFACE: class AtlasError(Exception) with category, severity, context fields. Vol 2 defines IntentParsingError, ResponseGenerationError, MemoryContextError, ReActLoopError inheriting from it.
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs AtlasConfig from shared/config.py (Volume 8)
STATUS: pending
INTERFACE: AtlasConfig(BaseSettings) with env_prefix="ATLAS_". Vol 2 reads ATLAS_DEFAULT_MODEL, ATLAS_FALLBACK_MODEL, ATLAS_MAX_REACT_STEPS, ATLAS_INTENT_CONFIDENCE_THRESHOLD, ATLAS_MAX_CONTEXT_TOKENS, ATLAS_RESPONSE_TIMEOUT_SECONDS, ATLAS_ENABLE_BERT, ATLAS_ENABLE_PROACTIVE, ATLAS_PERSONALITY_PATH, ATLAS_LOG_LEVEL.
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs LLMProvider Protocol from shared/llm.py (Volume 8)
STATUS: pending
INTERFACE: Protocol class with async def generate(prompt: str, model: str, **kwargs) -> str. Vol 2 calls this for all LLM interactions (response generation, ReAct reasoning, LLM-fallback classification). R6 model independence.
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs EvidenceStore from Volume 9 (Governance)
STATUS: pending
INTERFACE: EvidenceStore with add_item(item: EvidenceItem) -> str and get_items() -> list[EvidenceItem]. SHA-256 integrity hashing, 256KB/item cap, 2MB/store cap. Per shared-contracts §1.2.
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs structlog configured logging from shared/logging.py (cross-cutting)
STATUS: pending
INTERFACE: from atlas.shared.logging import get_logger -> structlog.BoundLogger
```

---

## Conflict Flags

```
CONFLICT: C-12 (streaming path) — RESOLVED
RESOLUTION: Single endpoint with stream=True/False parameter in ConversationRequest (B.6.3). No separate streaming endpoint.
IMPACT: Vol 8 (API) must handle SSE response when stream=True.
```

```
CONFLICT: C-13 (ConversationResponse vs ChatResponse) — RESOLVED
RESOLUTION: Vol 2 owns ConversationResponse (B.6.4). Vol 8 maps to ChatResponse for HTTP: response→answer, evidence_refs→evidence.
IMPACT: Vol 8 must implement field mapping layer.
```

*No new cross-volume conflicts identified by Volume 2 Phase 2 distillation.*

---

## Discoveries for Other Volumes

**For Volume 0:**
- B.11.1: Speculation scrubbing pattern (30+ regex replacements in answer_governor.py lines 62-108) should be promoted as an implementation note under P9.
- B.11.2: Evidence contracts pattern (15 default contracts mapping intent→required evidence) should be promoted as a design pattern under P9.
- B.11.3: Prompt priority system (SectionPriority with token budget competition) should be documented as a prompt engineering pattern.
- B.11.4: Premature parallel optimization anti-pattern (asyncio.gather race conditions) should be added as anti-pattern A10.

**For Volume 1:**
- Vol 2's ConversationEngine calls `MemoryManager.assemble_context()` synchronously in the critical path. The sequential pipeline (B.11.4) means memory assembly must complete before LLM generation starts.
- Session lifecycle: if ConversationRequest.session_id is None, Vol 2 calls `MemoryManager.start_conversation()` to create a new session. Vol 1 owns session creation and expiry.

**For Volume 3:**
- IntentCategory enum (320 values) is consumed by Vol 3 for correction records. Canonical definition is in `orchestrator/schemas.py`, re-exported from `shared/types.py`.
- OutcomeSignal integration: all orchestrator errors with severity ≥ warning are forwarded to Vol 3 via OutcomeSignal with outcome_type=FAILURE (B.7.2 rule 4).

**For Volume 8:**
- ConversationResponse→ChatResponse field mapping is Vol 8's responsibility (per C-13).
- SSE streaming: Vol 8 must handle `stream=True` in ConversationRequest and produce SSE events (per C-12).
- `shared/errors.py` must define AtlasError before Vol 2 can build its 4 error types. Tier 0 dependency.
- `shared/config.py` must define AtlasConfig with the 10 environment variables listed in B.9.1.
- `shared/llm.py` must define LLMProvider Protocol before Vol 2's ResponseGenerator can make LLM calls.

**For Volume 9:**
- Vol 2's ResponseGenerator passes all RawResponse objects through AnswerGovernor.govern(). Vol 9 must accept UnifiedIntent as context for governance decisions.
- EvidenceStore is consumed by Vol 2's ReAct loop — evidence items are added during tool execution and referenced in ConversationResponse.evidence_refs.
- Evidence contracts (B.11.2) map intent patterns to required evidence. If Vol 9 owns EvidenceContract schema definition, Vol 2 needs the import path.

**For Volume 10:**
- ReAct loop uses ToolRegistry.get_openai_schema_for_query() to get tool schemas in OpenAI function calling format. Vol 10 must provide this interface.
- ToolCallRecord (B.6.7) is Vol 2's record of tool execution. Vol 10's ToolResult must be convertible to ToolCallRecord fields.

---

## Phase 2 Corrections to Phase 1

**PersonalityTraits type correction:** Phase 1 B.3 references PersonalityTraits without specifying its type. Attempt 3's `personality_loader.py` and `personality_models.py` use a `dataclass` (not Pydantic BaseModel). The rebuild converts to `BaseModel` with `frozen=True` for Pydantic validation enforcement (P8). Documented in B.6.9.

**ReAct max_iterations correction:** Attempt 3's `react_engine.py` defaults `max_iterations` to 15. The rebuild sets `ATLAS_MAX_REACT_STEPS` default to 5 per P7 (smaller and working). Documented in B.9.1.

---

## Modification History

| Version | Date | Modified By | Summary |
|---|---|---|---|
| v1 | 2026-03-11 | Phase 2 Distillation Agent | Initial creation — 7 ownership claims, 8 dependency declarations, 2 resolved conflict flags, cross-volume discoveries for Vols 0/1/3/8/9/10, 2 Phase 1 corrections |
