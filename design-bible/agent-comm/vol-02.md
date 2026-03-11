# Agent Communication — Volume 2: Orchestrator & Conversation Loop

| Field | Value |
|---|---|
| **Volume** | 2 |
| **Phase** | Phase 2 (B.5–B.13) |
| **Date** | 2026-03-11 |

---

## Ownership Claims

```
CLAIM: ConversationEngine (engine.py — single entry point for all conversation processing)
OWNER: Volume 2
REASON: Central pipeline orchestrator: parse intent → retrieve context → generate response → govern output → record interaction.
CONTESTED: no
```

```
CLAIM: IntentParser (intent.py — three-tier intent classification: symbolic → BERT → LLM)
OWNER: Volume 2
REASON: Intent classification is the first stage of the conversation pipeline; symbolic grammar, ML advisory, and LLM fallback are orchestrator concerns.
CONTESTED: no
```

```
CLAIM: ResponseGenerator (response.py — response generation + ReAct engine + prompt building)
OWNER: Volume 2
REASON: Response generation including ReAct multi-step reasoning, prompt construction (SectionPriority system), and template-based deterministic responses.
CONTESTED: no
```

```
CLAIM: PersonalityManager (personality.py — personality loading + caching + system prompt injection)
OWNER: Volume 2
REASON: Personality is injected into the conversation pipeline's system prompts. Immutable at runtime per P10.
CONTESTED: no
```

```
CLAIM: MemoryContextRetriever (memory_context.py — per-request memory context assembly)
OWNER: Volume 2
REASON: Retrieves and assembles context from Vol 1 memory layers (L3-L10) for prompt enrichment. Token budget enforcement is an orchestrator concern.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 2 needs MemoryManager interface (session CRUD + per-layer queries L3-L10) from Volume 1
STATUS: pending
INTERFACE: MemoryManager.start_conversation(session_id), add_message(session_id, role, content), get_conversation(session_id), plus per-layer query methods for L3 episodes, L4 facts, L5 skills, L8 goals, L9 preferences, L10 vector search
```

```
DEPENDENCY: Volume 2 needs DecisionValidator.validate() from Volume 9
STATUS: pending
INTERFACE: DecisionValidator.validate(intent: UnifiedIntent, command: str, context: dict | None) -> ValidationDecision
```

```
DEPENDENCY: Volume 2 needs AnswerGovernor.govern() from Volume 9
STATUS: pending
INTERFACE: AnswerGovernor.govern(content: str, phase: OutputPhase, evidence_store: EvidenceStore | None) -> GovernedOutput
```

```
DEPENDENCY: Volume 2 needs ToolRegistry.execute() and tool schema export from Volume 10
STATUS: pending
INTERFACE: ToolRegistry.execute(tool_name, arguments, context) -> ToolResult; ToolRegistry.get_openai_schema() -> list[dict]
```

```
DEPENDENCY: Volume 2 needs LLMProvider abstraction from shared infrastructure
STATUS: pending
INTERFACE: LLMProvider.generate(messages, model, temperature, tools) -> LLMResponse — model-independent (R6)
```

---

## Cross-Volume Discoveries (Phase 2)

These findings from Vol 2's source code analysis affect other volumes:

### Discovery → Vol 9 (Governance)
**EvidenceStore capacity management:** `evidence_store.py` has built-in `max_items` (default 100) with eviction policy (lowest confidence first, then oldest). Vol 9 must preserve this when rebuilding the governance pipeline. The capacity management is designed for ReAct loops that accumulate many tool results.

### Discovery → Vol 9 (Governance)
**Speculation scrubber patterns:** `response_validator.py` contains regex patterns for detecting speculative language ("I think", "probably", "might be") that predate ADR-0031's formal pipeline. These patterns are a lightweight pre-governance filter. Vol 9 should incorporate or supersede them in the full AnswerGovernor implementation.

### Discovery → Vol 1 (Memory) + Vol 10 (Tools)
**Sync/async boundary contract:** Vol 2's pipeline is fully async. The rebuild defines that all Vol 1 and Vol 10 interfaces consumed by Vol 2 must be `async def`. If underlying implementations are synchronous, the owning volume wraps them — Vol 2 never calls `asyncio.to_thread()` on external interfaces. Vol 1 and Vol 10 must account for this in their interface contracts.

### Discovery → Vol 8 (API)
**ConversationResponse → ChatResponse mapping:** Per shared contract C-13, Vol 8 is responsible for mapping Vol 2's `ConversationResponse` to the HTTP-facing `ChatResponse`. Vol 2 returns the internal schema; Vol 8 serializes.

---

## Shared Contract Verification (Phase 2)

All shared contracts from `gate-output/shared-contracts.md` verified as satisfied:
- **C-12:** `ConversationRequest.stream` field present (single endpoint with stream flag)
- **C-13:** `ConversationResponse` returned by Vol 2; mapping to `ChatResponse` is Vol 8's responsibility
- **C-17:** Field name is `query` (not `message` or `input`) in `ConversationRequest`
- **Section 1.6:** Orchestrator schemas placed in `contracts/orchestrator_schemas.py`
- **Sections 2.1–2.4:** All cross-volume interfaces documented in B.3 §3.6
