# Agent Communication — Volume 8: API & Infrastructure

> **Rules:** Append new claims/dependencies/conflicts using the formats defined in `AGENT_COMM.md`.
> This file is the ONLY place Vol 8 agents register changes. Do NOT edit `AGENT_COMM.md` directly.

---

## Ownership Claims

```
CLAIM: FastAPI app factory, startup/shutdown lifecycle, middleware stack
OWNER: Volume 8
REASON: Server creation, middleware registration, and lifespan management are API infrastructure concerns.
CONTESTED: no
```

```
CLAIM: Error taxonomy (AtlasError hierarchy, ErrorCategory, ErrorSeverity)
OWNER: Volume 8 (shared/errors.py)
REASON: The error hierarchy is cross-cutting infrastructure consumed by every subsystem. Volume 8 defines it; others import it.
CONTESTED: no
```

```
CLAIM: Configuration system (AtlasConfig, pydantic-settings)
OWNER: Volume 8 (shared/config.py)
REASON: Server configuration, feature flags, and env-var loading are infrastructure concerns.
CONTESTED: no
```

```
CLAIM: API request/response Pydantic schemas for chat endpoint (ChatRequest, ChatResponse, EvidenceRef)
OWNER: Volume 8 (contracts/api_schemas.py)
REASON: Cross-boundary schemas shared with Console (Volume 7) live in contracts/. Volume 8 defines the HTTP contract; Volume 2 defines the orchestrator interface.
CONTESTED: no
```

```
CLAIM: ErrorResponse schema (structured error JSON body)
OWNER: Volume 8
REASON: HTTP error formatting is an API-layer concern.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 8 needs Orchestrator.process_command() and Orchestrator.process_command_streaming() from Volume 2
STATUS: pending
INTERFACE: async def process_command(command: str, device_id: str, conversation_id: str | None) -> dict; async generator process_command_streaming(...) -> AsyncIterator[StreamEvent]
```

```
DEPENDENCY: Volume 8 needs MemoryManager.get_stats(), MemoryManager.get_recent_conversations() from Volume 1
STATUS: pending
INTERFACE: get_stats() -> Dict[str, Any]; get_recent_conversations(hours: int, limit: int) -> List[Dict[str, Any]]
```

```
DEPENDENCY: Volume 8 needs GovernedOutput / output governance gate from Volume 9
STATUS: pending
INTERFACE: ChatResponse.governed field + EvidenceRef list depend on Volume 9's governance output schema
```

```
DEPENDENCY: Volume 8 needs structlog configured logging from shared/logging.py (cross-cutting, no single volume owner)
STATUS: pending
INTERFACE: from atlas.shared.logging import log (structlog.BoundLogger)
```

```
DEPENDENCY: Volume 8 (API) needs tool introspection surface from Volume 10
STATUS: pending
INTERFACE: ToolRegistry.list_tools() -> list[str]; SystemTools.get_tool_list(category) -> dict
```

```
DEPENDENCY: Volume 8 needs learning health/stats endpoints from Volume 3
STATUS: pending
INTERFACE: LearningManager.get_stats() -> dict, EffectivenessTracker.get_learning_patterns() -> dict
```

---

## Conflict Acknowledgements

```
CONFLICT: Error taxonomy location
VOLUMES: 8 vs all consumers
RESOLUTION: resolved — shared/errors.py per PROJECT_CONVENTIONS.md Section 6 (conflict-report.md)
```

```
CONFLICT: Chat endpoint request field naming
VOLUMES: 8 vs 2 vs 7
RESOLUTION: resolved — Field name is 'query' everywhere (conflict-report.md C-12)
```

```
CONFLICT: Endpoint URL prefix inconsistency
VOLUMES: 7 vs 8
RESOLUTION: resolved — /v1/* prefix everywhere, kill /api proxy (conflict-report.md C-10)
```

```
CONFLICT: TypeScript type generation ownership
VOLUMES: 7 vs 8 vs 9
RESOLUTION: resolved — TS codegen tool → Vol 8 (conflict-report.md C-11)
```
