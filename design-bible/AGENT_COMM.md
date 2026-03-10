# Agent Communication Hub

| Field | Value |
|---|---|
| **Doc ID** | `DB-X00-003` |
| **Name** | Agent Communication Hub |
| **Purpose** | Persistent coordination file where distillation agents register ownership claims, dependencies, and conflicts across volumes |
| **Owner** | Design Bible / Infrastructure |
| **Status** | `active` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz |
| **Version** | v5 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## Rules

### Ownership Claims
When a distillation agent determines that a component belongs to THEIR volume, they register ownership here. If two agents claim the same component, the conflict must be resolved before either volume is submitted.

Format:
```
CLAIM: [component name]
OWNER: Volume [N]
REASON: [one sentence]
CONTESTED: [yes/no]
```

### Dependency Declarations
When a distillation agent's subsystem needs something from another volume, they declare it here. The owning volume must define the interface; the consuming volume references it.

Format:
```
DEPENDENCY: Volume [consumer] needs [what] from Volume [provider]
STATUS: [pending/acknowledged/resolved]
INTERFACE: [schema name or method signature, once resolved]
```

### Conflict Flags
When two volumes have incompatible design decisions, flag it here for resolution.

Format:
```
CONFLICT: [description]
VOLUMES: [N] vs [M]
PROPOSED RESOLUTION: [suggestion]
STATUS: [open/resolved]
RESOLUTION: [final decision]
```

---

## Pre-Registered Ownership (Known Boundaries)

These ownership decisions are made upfront to prevent predictable conflicts:

### Memory Schemas
- **Owner: Volume 1 (Memory)**
- All Pydantic schemas for data entering/leaving memory layers are defined by Volume 1
- Other volumes CONSUME these schemas, they do not redefine them
- If another volume needs a new field or schema, they declare a DEPENDENCY here

### Intent Validation
- **Owner: Volume 9 (Governance)**
- DecisionValidator and all validation gate logic belongs to Volume 9
- Volume 2 (Orchestrator) CONSUMES validation, it does not own it

### Output Governance
- **Owner: Volume 9 (Governance)**
- GovernedOutput, AnswerGovernor, claim extraction, evidence grounding
- Volume 2 (Orchestrator) integrates governance into the response pipeline but does not own the governance logic

### Knowledge Pipeline
- **Owner: Volume 3 (Learning)** owns the ingestion, extraction, and synthesis pipeline
- **Volume 5 (Intelligence)** owns the amplification layer (analogical reasoning, hypothesis generation, Socratic challenge, growth tracking)
- **Boundary:** Volume 3 produces `RefinedKnowledge`. Volume 5 consumes it.
- Extractors (`src/learning/extractors/`) belong to Volume 3
- `src/intelligence/` components belong to Volume 5

### Tool Registry
- **Owner: Volume 10 (External Tools)** owns the tool infrastructure and individual tools
- Volume 2 (Orchestrator) owns tool INVOCATION (how tools are called during conversation)
- Volume 10 owns tool DEFINITION (what tools exist and what they do)

### Voice Governance Schemas
- **Owner: Volume 9 (Governance)** owns the governance pattern (AuthorityLevel, grounding)
- **Volume 6 (Voice)** owns the voice-specific implementation (TTS, STT, WebRTC)
- ApprovedUtterance is superseded by GovernedOutput in the rebuild; Volume 9 defines the unified schema

### API Endpoints
- **Owner: Volume 8 (API)** owns the server, routing, middleware, and endpoint registration
- Each subsystem volume defines WHAT endpoints their subsystem needs
- Volume 8 defines HOW those endpoints are implemented (FastAPI patterns, error responses, etc.)

---

## Ownership Claims (Agent-Registered)
*[Distillation agents register claims here during their deep dives]*

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
CONTESTED: no (generation ownership TBD - see Conflict Flag below)
```

```
CLAIM: TTS/STT client integration (currently inlined in ChatPanel.tsx)
OWNER: Volume 7 (contested with Volume 6)
REASON: Voice logic is currently embedded in ChatPanel.tsx but belongs to Volume 6. Volume 7 consumes a clean interface after extraction.
CONTESTED: yes (see Conflict Flag below)
```

```
CLAIM: Session management client (console/src/lib/session.ts)
OWNER: Volume 7
REASON: Client-side session persistence and session API consumption is console-owned. Backend session storage is Volume 8.
CONTESTED: no
```

---

## Dependency Declarations (Agent-Registered)
*[Distillation agents declare cross-volume dependencies here]*

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

## Conflict Flags (Agent-Registered)
*[Distillation agents flag conflicts here for resolution]*

```
CONFLICT: TTS/STT voice logic inlined in Console ChatPanel.tsx (Vol 7) but owned by Vol 6
VOLUMES: 7 vs 6
PROPOSED RESOLUTION: Vol 6 owns TTS/STT implementation. Vol 7 extracts inlined Cartesia/OpenAI voice code from ChatPanel.tsx and consumes a clean interface from Vol 6.
STATUS: open
RESOLUTION: [awaiting Vol 6 acknowledgement]
```

```
CONFLICT: Endpoint URL prefix inconsistency - console Vite proxy rewrites /api/* but backend uses /v1/* natively
VOLUMES: 7 vs 8
PROPOSED RESOLUTION: Vol 8 defines the canonical prefix. Console proxy should pass-through /v1/* directly. Eliminate /api prefix in production.
STATUS: open
RESOLUTION: [awaiting Vol 8 acknowledgement]
```

```
CONFLICT: TypeScript type generation ownership - who owns the Pydantic-to-TS codegen pipeline?
VOLUMES: 7 vs 8 vs 9
PROPOSED RESOLUTION: Vol 8 (API and Infrastructure) owns the codegen tool and CI step. Vol 9 provides governance schemas as input. Vol 7 consumes the generated output.
STATUS: open
RESOLUTION: [awaiting integration gate]
```

---

## Integration Gate Output

The integration gate agent produces its output in `design-bible/gate-output/`. See `DISTILLATION_PROTOCOL.md` Section 3 for details.

**Gate output files:**
- `gate-output/conflict-report.md` — Cross-volume conflicts with resolutions
- `gate-output/shared-contracts.md` — Binding interface contracts for Phase 2
- `gate-output/build-order-refined.md` — Refined build order
- `gate-output/mva-refined.md` — Refined MVA criteria
- `gate-output/quality-flags.md` — Per-volume quality assessment
- `gate-output/final-review.md` — Final review after Phase 2 (created at end)

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial creation — defined ownership claim, dependency declaration, and conflict flag protocols; pre-registered 7 known boundary ownership decisions | Created the shared coordination file so agents working on different subsystems don't step on each other |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-X00-003`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added Integration Gate Output section referencing `gate-output/` directory and 6 output files per DISTILLATION_PROTOCOL.md | Added a section pointing to where the integration agent stores its analysis results |
| v5 | 2026-03-10 | Vol-07 Distillation Agent | 4 ownership claims (Console SPA, TS types, TTS/STT client contested with Vol 6, session management), 8 dependency declarations (SSE format, chat schema, sessions, memory, health, WebSocket, type codegen, GovernedOutput from Vol 1/2/8/9), 3 conflict flags (TTS/STT Vol 7 vs 6, endpoint prefix Vol 7 vs 8, codegen ownership Vol 7 vs 8 vs 9) | Console agent registered what it owns, what it needs from other subsystems, and flagged three cross-volume disagreements |
