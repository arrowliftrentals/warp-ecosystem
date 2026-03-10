# Agent Communication — Volume 10: External Tools
## Phase 2 Distillation Outputs

---

## Ownership Claims

```
CLAIM: ToolRegistry (tool_registry.py)
OWNER: Volume 10
REASON: Core tool infrastructure — registration, execution, schema generation — belongs to the external tools subsystem.
CONTESTED: no
```

```
CLAIM: ToolDefinition, ToolResult, SecurityClassification schemas
OWNER: Volume 10
REASON: Volume 10 defines what tools are and how results are structured. These schemas live in atlas/tools/schemas.py.
CONTESTED: no
```

```
CLAIM: All parameter schemas (FileReadParams, FileWriteParams, GitStatusParams, MemoryQueryParams, WebSearchParams, etc.)
OWNER: Volume 10
REASON: Tool parameter validation is the tool subsystem's responsibility. 14 parameter schemas defined in B.6.4.
CONTESTED: no
```

```
CLAIM: Tool error hierarchy (ToolNotFoundError, ToolValidationError, ToolTimeoutError, ToolSecurityError, PathSecurityError)
OWNER: Volume 10
REASON: All inherit from ToolExecutionError in shared/errors.py. Volume 10 defines these specific error types for tool execution failures.
CONTESTED: no
```

```
CLAIM: Domain tools (domain_tools.py — 21 handler classes)
OWNER: KILL (LLM-wrapper anti-pattern)
REASON: 15+ domain tool classes are thin LLM-prompt wrappers that add no capability. See B.10.1 and B.11.1. Proposed as anti-pattern A9 in Volume 0.
CONTESTED: no
```

```
CLAIM: ExternalToolSpec, Arsenal, ArsenalRegistry
OWNER: Volume 10 (DEFER to Phase 4)
REASON: Well-designed extensibility patterns owned by Volume 10 but not needed for REBUILD scope. See B.11.2.
CONTESTED: no
```

```
CLAIM: Screen control (accessibility.py, controller.py, app_launcher.py)
OWNER: Volume 10 (DEFER to Phase 5)
REASON: macOS-only commodity capability. ~1100 lines of standard API wrapping. Not portable. See B.10.6.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 10 needs MemoryManager with layer accessors (.l3, .l4, .l9, .l10) from Volume 1
STATUS: pending
INTERFACE: MemoryManager.l3 (EpisodicMemory), .l4 (DeclarativeMemory), .l9 (L9ProceduralMemory), .l10 (L10SemanticMemory) — per shared-contracts.md Section 2.12
```

```
DEPENDENCY: Volume 10 needs DecisionValidator.validate(command, context) -> ValidationResult from Volume 9
STATUS: pending
INTERFACE: DecisionValidator.validate(command: str, context: dict | None) -> ValidationResult — per shared-contracts.md Section 2.13
```

```
DEPENDENCY: Volume 2 (Orchestrator) consumes ToolRegistry.execute(tool_name, arguments, context) -> ToolResult from Volume 10
STATUS: pending
INTERFACE: ToolRegistry.execute(tool_name: str, arguments: dict, context: dict | None) -> ToolResult — per shared-contracts.md Section 2.4
```

```
DEPENDENCY: Volume 2 (Orchestrator) consumes ToolRegistry.get_openai_schema_for_query(query, max_tools) -> list[dict] from Volume 10
STATUS: pending
INTERFACE: ToolRegistry.get_openai_schema_for_query(query: str, max_tools: int = 20) -> list[dict]
```

```
DEPENDENCY: Volume 8 (API) constructs ToolCallSummary from Volume 10's ToolResult
STATUS: pending
INTERFACE: ToolCallSummary constructed from ToolResult fields (success, tool_name, execution_time_ms) — Vol 8 owns ToolCallSummary, Vol 10 provides ToolResult
```

```
DEPENDENCY: Volume 10 needs LLMProvider Protocol from shared/llm.py for STEM backend fallback (Phase 3 — not REBUILD scope)
STATUS: pending
INTERFACE: LLMProvider.complete(messages: list[dict], **kwargs) -> str — needed when STEM computation fails and LLM fallback is required
```

```
DEPENDENCY: Volume 10 needs shared infrastructure (shared/errors.py, shared/config.py, shared/logging.py) from cross-cutting infra
STATUS: pending
INTERFACE: ToolExecutionError from shared/errors.py; AtlasConfig from shared/config.py; structlog from shared/logging.py
```

---

## Conflict Flags

*No cross-volume conflicts identified by Volume 10 Phase 2 distillation.*

---

## Discoveries for Other Volumes

**For Volume 0:**
- B.11.1 proposes new anti-pattern A9: "LLM-Wrapper Tools" — a tool that only calls `llm_client.complete()` adds no capability and should not exist. Volume 0 maintainer should evaluate adding this.

**For Volume 2:**
- ToolResult includes `execution_time_ms` field specifically so Vol 2 can track tool latency in the evidence store.
- Vol 2 is responsible for calling `EvidenceStore.store()` with tool results — Vol 10 does not call EvidenceStore directly.

**For Volume 9:**
- Governance integration is centralized in `ToolRegistry.execute()`, not in individual tool handlers. DecisionValidator is called once per DANGEROUS tool, not per handler.

---

## Modification History

| Version | Date | Modified By | Summary |
|---|---|---|---|
| v1 | 2026-03-10 | Distillation Agent V10 | Initial creation — Phase 2 discoveries: 7 ownership claims, 7 dependency declarations, 0 conflicts, 3 cross-volume notifications |
