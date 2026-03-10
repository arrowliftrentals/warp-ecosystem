# Agent Communication — Volume 10: External Tools & Capabilities

> **Rules:** Append new claims/dependencies/conflicts using the formats defined in `AGENT_COMM.md`.
> This file is the ONLY place Vol 10 agents register changes. Do NOT edit `AGENT_COMM.md` directly.

---

## Ownership Claims

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

## Dependency Declarations

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

---

## Conflict Acknowledgements

No conflicts involving Volume 10.
