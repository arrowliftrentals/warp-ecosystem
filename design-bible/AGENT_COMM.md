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

```
CLAIM: ToolRegistry (registration, lookup, schema export, execution orchestration)
OWNER: Volume 10
REASON: Central tool infrastructure per pre-registered boundary — Volume 10 owns DEFINITION, Volume 2 owns INVOCATION.
CONTESTED: no
```

```
CLAIM: ToolDefinition dataclass and tool_schemas.py Pydantic parameter/result schemas
OWNER: Volume 10
REASON: Boundary validation schemas for tool inputs and outputs live with tool definitions.
CONTESTED: no
```

```
CLAIM: Core tool handlers (FileTools, GitTools, MemoryTools, ConversationTools, SystemTools, WebTools)
OWNER: Volume 10
REASON: Tool implementation classes and their handler methods. Volume 10 owns what each tool does.
CONTESTED: no
```

```
CLAIM: STEM computational backends (backends/mathematics.py, science.py, engineering.py, data_science.py, additive_manufacturing.py)
OWNER: Volume 10
REASON: ADR-0030 computation-first backends are tool-layer implementation with no orchestrator dependency.
CONTESTED: no
```

```
CLAIM: Security/pentest tool stack (container_manager, engagement_scope, external_tool_manifest, external_tool_discovery, spec_generator, arsenal)
OWNER: Volume 10
REASON: External tool governance and discovery infrastructure per ADR-0028/0029.
CONTESTED: no
```

```
CLAIM: Screen control subsystem (accessibility.py, controller.py, app_launcher.py)
OWNER: Volume 10
REASON: macOS UI automation is an external capability surface, not orchestrator logic.
CONTESTED: no
```

```
CLAIM: External integration tools (email_tools, calendar_tools, messaging_tools, home_tools, voice_tools, screen_tools)
OWNER: Volume 10
REASON: Integration wrappers exposing external service APIs as tool handlers.
CONTESTED: no
```

---

## Dependency Declarations (Agent-Registered)

```
DEPENDENCY: Volume 10 needs MemoryManager interface (L1-L10 access) from Volume 1
STATUS: pending
INTERFACE: MemoryManager with layer accessors (.l1 through .l10), search methods, get_stats(), get_consolidation_health(), get_safeguards_status()
```

```
DEPENDENCY: Volume 10 needs DecisionValidator.validate(command, context) from Volume 9
STATUS: pending
INTERFACE: DecisionValidator.validate(command: str, context: dict | None) -> ValidationResult with is_safe(), blocked_reasons, requires_confirmation
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs ToolRegistry.execute() and ToolRegistry.get_openai_schema_for_query() from Volume 10
STATUS: pending
INTERFACE: ToolRegistry.execute(tool_name, arguments, context) -> ToolResult; ToolRegistry.get_openai_schema_for_query(query, max_tools) -> list[dict]
```

```
DEPENDENCY: Volume 8 (API) needs tool introspection surface from Volume 10
STATUS: pending
INTERFACE: ToolRegistry.list_tools() -> list[str]; SystemTools.get_tool_list(category) -> dict
```

---

## Conflict Flags (Agent-Registered)
*No new conflicts flagged by Volume 10 distillation. All ownership boundaries align with pre-registered decisions.*

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
|| v4 | 2026-03-10 | Oz | Added Integration Gate Output section referencing `gate-output/` directory and 6 output files per DISTILLATION_PROTOCOL.md | Added a section pointing to where the integration agent stores its analysis results |
|| v5 | 2026-03-10 | Distillation Agent V10 | Phase 1: Registered 7 ownership claims (ToolRegistry, tool schemas, core handlers, STEM backends, security/pentest stack, screen control, external integrations), 4 dependency declarations (MemoryManager from V1, DecisionValidator from V9, ToolRegistry execution to V2, tool introspection to V8). No new conflicts. | Volume 10 agent claimed all tool definitions, registries, and capability implementations; documented cross-volume interface needs |
