# Agent Communication — Volume 7: Console

> **Rules:** Append new claims/dependencies/conflicts using the formats defined in `AGENT_COMM.md`.
> This file is the ONLY place Vol 7 agents register changes. Do NOT edit `AGENT_COMM.md` directly.

---

## Ownership Claims

```
CLAIM: Console SPA (React frontend application)
OWNER: Volume 7
REASON: The browser-hosted console is the sole UI surface for Atlas interaction and observability.
CONTESTED: no
```

```
CLAIM: Console TypeScript type definitions (console/src/lib/types.ts)
OWNER: Volume 7
REASON: Console-side TS types are owned by Volume 7; auto-generated from Pydantic schemas (Volume 8/9 source of truth) under R9.
CONTESTED: no
```

```
CLAIM: TTS/STT client integration (currently inlined in ChatPanel.tsx)
OWNER: Volume 7 (UI layer); Volume 6 (implementation)
REASON: Voice logic is currently embedded in ChatPanel.tsx. Vol 6 owns TTS/STT implementation; Vol 7 consumes a clean interface after extraction.
CONTESTED: no (resolved — Vol 6 owns implementation, Vol 7 owns UI consumption)
```

```
CLAIM: Session management client (console/src/lib/session.ts)
OWNER: Volume 7
REASON: Client-side session persistence and session API consumption is console-owned. Backend session storage is Volume 8.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 7 (Console) needs the ChatRequest/ChatResponse/ErrorResponse schemas from Volume 8 contracts/api_schemas.py for TypeScript type generation
STATUS: pending
INTERFACE: Pydantic models in contracts/api_schemas.py → generated TypeScript types via scripts/generate_contracts.sh
```

```
DEPENDENCY: Volume 7 needs SSE streaming event format specification from Volume 8
STATUS: pending
INTERFACE: SSE event schema: { type: text|thinking|tool_call|tool_result|error|done } (see DB-V07-001 B.3.1)
```

```
DEPENDENCY: Volume 7 needs chat response schema (ChatMessage, ThinkingStep, ToolCall) from Volume 2
STATUS: pending
INTERFACE: ChatMessage, ThinkingStep, ToolCall interfaces (see DB-V07-001 B.3.4)
```

```
DEPENDENCY: Volume 7 needs session CRUD API endpoints from Volume 8
STATUS: pending
INTERFACE: GET/POST/DELETE /v1/sessions (see DB-V07-001 B.3.1)
```

```
DEPENDENCY: Volume 7 needs memory layer read API from Volume 1 (schemas) and Volume 8 (endpoints)
STATUS: pending
INTERFACE: GET /v1/memory/layers, /v1/memory/layers/:name, /v1/memory/search (see DB-V07-001 B.3.1)
```

```
DEPENDENCY: Volume 7 needs health endpoint format from Volume 8
STATUS: pending
INTERFACE: 10 health endpoints returning { status: string } minimum (see DB-V07-001 B.3.1)
```

```
DEPENDENCY: Volume 7 needs WebSocket telemetry protocol from Volume 8
STATUS: pending
INTERFACE: ws://host/ws/telemetry with { type: metrics, data: TelemetryPayload } (see DB-V07-001 B.3.2)
```

```
DEPENDENCY: Volume 7 needs Pydantic-to-TypeScript type generation pipeline from Volume 8 (R9 enablement)
STATUS: pending
INTERFACE: Build-time codegen producing shared/types/ from Pydantic schemas (see DB-V07-001 B.3.5)
```

```
DEPENDENCY: Volume 7 needs GovernedOutput type from Volume 9
STATUS: pending
INTERFACE: GovernedOutput schema replacing raw response text (see DB-V07-001 B.3.7)
```

---

## Conflict Acknowledgements

```
CONFLICT: TTS/STT voice logic inlined in Console ChatPanel.tsx
VOLUMES: 7 vs 6
RESOLUTION: resolved — Vol 6 owns TTS/STT implementation. Vol 7 extracts inlined voice code and consumes a clean interface (conflict-report.md C-09)
```

```
CONFLICT: Endpoint URL prefix inconsistency
VOLUMES: 7 vs 8
RESOLUTION: resolved — /v1/* prefix everywhere, kill /api proxy (conflict-report.md C-10)
```

```
CONFLICT: TypeScript type generation ownership
VOLUMES: 7 vs 8 vs 9
RESOLUTION: resolved — TS codegen tool → Vol 8. Vol 9 provides governance schemas as input. Vol 7 consumes output (conflict-report.md C-11)
```

```
CONFLICT: Chat endpoint request field naming
VOLUMES: 8 vs 2 vs 7
RESOLUTION: resolved — Field name is 'query' everywhere (conflict-report.md C-12)
```
