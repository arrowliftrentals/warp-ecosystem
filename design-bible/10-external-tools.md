# ATLAS Design Bible — Volume 10: External Tools & Capabilities

| Field | Value |
|---|---|
| **Doc ID** | `DB-V10-001` |
| **Name** | Volume 10: External Tools & Capabilities |
| **Purpose** | Design specification for the tool ecosystem — file ops, git, web, STEM computation, security tools, screen control, and tool registry |
| **Owner** | Design Bible / Volume 10 |
| **Status** | `draft` (Phase 1 distillation — B.1-B.4 filled) |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / Distillation Agent V10 (Part B) |
| **Version** | v5 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## Part A: Context (Pre-loaded)

### A.1 Subsystem Identity
- **Volume 10: External Tools & Capabilities**
- **Purpose:** The tool ecosystem — file operations, git, web, email, calendar, screen control, STEM computation, security tools, and all other capabilities Atlas exposes through its tool registry.
- **Rebuild phase:** Phase 2-6 (tools are added incrementally as subsystems come online). Core tools (file, git, memory) come with Phase 0-1. Domain tools come later.

### A.2 Source Manifest

**Code files to read** (paths relative to `atlas/`):

*Tool infrastructure:*
- `src/orchestrator/tool_registry.py` — central tool registration and lookup
- `src/orchestrator/tool_schemas.py` — tool input/output schemas

*Core tools (high priority):*
- `src/orchestrator/tools/file_tools.py` — file read/write/search
- `src/orchestrator/tools/git_tools.py` — git operations
- `src/orchestrator/tools/memory_tools.py` — memory CRUD
- `src/orchestrator/tools/memory_extended_tools.py` — advanced memory ops
- `src/orchestrator/tools/conversation_tools.py` — conversation management
- `src/orchestrator/tools/system_tools.py` — system operations
- `src/orchestrator/tools/web_tools.py` — web search/fetch

*Domain tools (STEM):*
- `src/orchestrator/tools/domain_tools.py` — STEM domain tools (21 handlers)
- `src/orchestrator/tools/register_domain_tools.py` — domain tool registration

*STEM computation backends:*
- `src/orchestrator/tools/backends/` (if exists — ADR-0030 computation-first backends)

*Security/pentest tools:*
- `src/orchestrator/tools/container_manager.py` — Docker container management
- `src/orchestrator/tools/engagement_scope.py` — pentest scope enforcement
- `src/orchestrator/tools/external_tool_manifest.py` — tiered governance
- `src/orchestrator/tools/external_tool_discovery.py` — tool auto-discovery
- `src/orchestrator/tools/spec_generator.py` — tool spec generation
- `src/orchestrator/tools/arsenal.py` — Kali tool arsenal

*Specialized tools:*
- `src/orchestrator/tools/sandbox_tools.py` — sandbox execution
- `src/orchestrator/tools/self_modify_tools.py` — self-modification tools
- `src/orchestrator/tools/learning_tools.py` — learning system tools
- `src/orchestrator/tools/research_tools.py` — research/paper tools
- `src/orchestrator/tools/analysis_tools.py` — code/system analysis
- `src/orchestrator/tools/architecture_tools.py` — architecture inspection
- `src/orchestrator/tools/benchmark_tools.py` — benchmarking
- `src/orchestrator/tools/audit_tools.py` — auditing
- `src/orchestrator/tools/governance_tools.py` — governance tools
- `src/orchestrator/tools/drift_tools.py` — drift detection
- `src/orchestrator/tools/profiler_tools.py` — profiling
- `src/orchestrator/tools/telemetry_tools.py` — telemetry
- `src/orchestrator/tools/event_tools.py` — event bus tools
- `src/orchestrator/tools/error_registry_tools.py` — error registry
- `src/orchestrator/tools/wiring_tools.py` — integration wiring

*External integrations:*
- `src/orchestrator/tools/email_tools.py` — email
- `src/orchestrator/tools/calendar_tools.py` — calendar
- `src/orchestrator/tools/messaging_tools.py` — messaging
- `src/orchestrator/tools/home_tools.py` — home automation
- `src/orchestrator/tools/screen_tools.py` — screen control
- `src/orchestrator/tools/voice_tools.py` — voice tools

*Screen control:*
- `src/screen/accessibility.py` — macOS Accessibility API
- `src/screen/controller.py` — screen control orchestration
- `src/screen/app_launcher.py` — application launching

**Documentation to read:**
- `docs/architecture/tool-registry.md`
- `docs/architecture/tool-schemas.md`
- `docs/architecture/file-tools.md`
- `docs/architecture/git-tools.md`
- `docs/architecture/web-tools.md`
- `docs/architecture/email-tools.md`
- `docs/architecture/calendar-tools.md`
- `docs/architecture/home-tools.md`
- `docs/architecture/screen-tools.md`
- `docs/architecture/domain-tools.md`
- `docs/architecture/domains.md`
- `docs/architecture/mathematics.md`
- `docs/architecture/science.md`
- `docs/architecture/engineering.md`
- `docs/architecture/data-science.md`
- `docs/architecture/container-manager.md`
- `docs/architecture/engagement-scope.md`
- `docs/architecture/external-tool-manifest.md`
- `docs/architecture/external-tool-discovery.md`
- `docs/architecture/spec-generator.md`
- `docs/architecture/ui-automation.md`
- `docs/architecture/additive-manufacturing.md`
- `docs/adr/0028-kali-container-tiered-governance.md`
- `docs/adr/0029-arsenal-template-system.md`
- `docs/adr/0030-stem-backend-wiring.md`

**Test files to read:**
- `tests/tools/` (if exists)
- `tests/screen/` (if exists)

**CORE/PERIPHERAL Classification** (per `DISTILLATION_PROTOCOL.md` Section 5):
- **CORE** (10 files): `tool_registry.py`, `tool_schemas.py`, `file_tools.py`, `git_tools.py`, `memory_tools.py`, `conversation_tools.py`, `system_tools.py`, `web_tools.py`, `accessibility.py`, `controller.py`
- **PERIPHERAL** (32 files): All domain tools (2), security/pentest tools (6), specialized tools (15), external integrations (6), `app_launcher.py`, `memory_extended_tools.py`, `register_domain_tools.py`

### A.3 Context Brief

**What worked in Attempt 3:**
- Tool registry with 80+ tools registered
- File tools, git tools, memory tools functional
- STEM domain tools with 21 handlers (computation-first via ADR-0030)
- Kali container with tiered governance (ADR-0028) — PASSIVE/ACTIVE/INTRUSIVE tiers
- Screen control via macOS Accessibility API
- Tool spec generator for auto-discovering external CLI tools

**What failed or was never wired:**
- 80+ tools registered but unclear which were actually integrated end-to-end
- Email, calendar, messaging, home automation tools — likely stubs or minimal implementations
- Plugin manager and device sync — initialized, report healthy, completely hollow
- Screen control — standard macOS APIs, commodity (Volume 0 Section 3)
- Many specialized tools (drift, profiler, wiring) may be over-engineering

**What was simulated/fake:**
- Plugin manager and device sync reported healthy while being completely hollow

**Relevant Volume 0 principles:**
- P1: ML advises, symbolic core decides (STEM backends compute first, LLM fallback)
- P3: Nothing ships without integration (80+ tools, how many actually work?)
- P7: Smaller and working beats larger and broken
- A1: Feature factory (80+ tools, many potentially unused)
- Section 3: Tool ecosystem is commodity — not the moat

### A.4 Known Failures & Warnings
1. **80+ tools needs aggressive triage**: Most of these are not moat capabilities. Core tools (file, git, memory, web) are essential. Everything else needs a REBUILD/DEFER/KILL verdict.
2. **STEM backends are valuable**: ADR-0030's computation-first pattern (sympy, numpy, scipy before LLM) is a correct application of P1. The user is a mechanical engineer PhD — engineering tools have high personal value.
3. **Security tools require Docker**: Kali container (ADR-0028) is impressive but requires Docker Desktop. Determine if this is a Phase 3+ capability or earlier.
4. **Email/calendar/home are integrations, not AI**: These are standard API integrations. They don't require AI architecture — just API wrappers. May be quick to rebuild but low priority for the moat.
5. **Screen control is macOS-only**: `src/screen/` uses macOS Accessibility API. Not portable. Determine if this is essential or deferrable.

---

## Part B: Design Specification (Agent Fills Out)

### B.1 Subsystem Purpose (Rebuild)

Volume 10 provides the **capability surface** through which Atlas interacts with external systems — files, git repositories, the web, STEM computation, security infrastructure, and system operations. The design intent is a **typed tool registry** where every capability is a first-class object with Pydantic-validated input/output schemas, explicit security classifications, and discoverable OpenAI-compatible function-calling signatures. Volume 10 owns tool **definition** (what tools exist and what they do). Volume 2 owns tool **invocation** (how tools are called during conversation). The rebuild must preserve this boundary while aggressively triaging the 80+ registered tools down to the set that actually delivers value.

The subsystem embodies P1 (ML advises, symbolic core decides) through the STEM computation backends: mathematical, scientific, and engineering problems are solved symbolically first (SymPy, NumPy, SciPy) with LLM fallback only when computation fails. This computation-first pattern (ADR-0030) is the correct expression of the neuro-symbolic principle for tool-layer work.

### B.2 Architecture Overview

**Layer structure (bottom → top):**

```
Layer 4: Tool Handlers (FileTools, GitTools, MemoryTools, etc.)
   │  Each class groups related operations as methods
   │  Each method = one tool (e.g. FileTools.read_file)
   ▼
Layer 3: ToolRegistry
   │  Central registration, lookup, schema export
   │  Converts handler methods → ToolDefinition objects
   │  Provides get_openai_schema_for_query() for dynamic tool selection
   ▼
Layer 2: ToolDefinition + tool_schemas.py
   │  Pydantic parameter/result schemas per tool
   │  Security classification: SAFE / REQUIRES_CONFIRMATION / DANGEROUS
   │  Category tags for filtered discovery
   ▼
Layer 1: External Systems
   │  Filesystem, git repos, web APIs, Docker containers, macOS Accessibility
```

**Key components:**

1. **ToolRegistry** (`tool_registry.py`): Singleton managing ~80 tool definitions. Methods: `register()`, `get_tool()`, `list_tools()`, `execute()`, `get_openai_schema_for_query()`. Uses MemoryManager for context-aware tool selection (semantic search over tool descriptions). Provides category-based and query-based filtering for dynamic tool presentation to the LLM.

2. **ToolDefinition** dataclass: name, description, handler callable, parameter schema (Pydantic), result schema, security classification enum, category tags, and whether confirmation is required.

3. **Core tool handler classes** (6 classes, ~40 tools total):
   - **FileTools**: read, write, search, list, create, delete, move files. Path validation via `_validate_path()` with allowed/blocked directory enforcement.
   - **GitTools**: status, log, diff, commit, push, pull, branch, merge. Wraps subprocess calls to git CLI. Safety: commit/push require confirmation.
   - **MemoryTools**: store/retrieve/search across L1-L10 memory layers. Delegates to MemoryManager (Volume 1). CRUD for facts, episodes, skills, beliefs.
   - **ConversationTools**: list, search, summarize, export conversations. Direct MemoryManager.l1 access for conversation history.
   - **SystemTools**: tool listing, help, system info, diagnostics. `get_tool_list()` provides introspection surface. Health checks aggregate subsystem status.
   - **WebTools**: web search (DuckDuckGo), URL fetch, content extraction. Rate limiting and content sanitization.

4. **STEM computation backends** (`backends/`): mathematics.py, science.py, engineering.py, data_science.py, additive_manufacturing.py. Each implements a computation-first pattern per ADR-0030: parse problem → attempt symbolic/numerical solution → return structured result → LLM fallback only on failure. 21 domain tool handlers in `domain_tools.py` dispatch to these backends.

5. **Security/pentest stack**: container_manager.py (Docker lifecycle), engagement_scope.py (target validation), external_tool_manifest.py (tiered tool governance per ADR-0028: PASSIVE/ACTIVE/INTRUSIVE), external_tool_discovery.py (CLI tool auto-discovery via `--help` parsing), spec_generator.py (OpenAPI spec generation from discovered tools), arsenal.py (Kali tool templates per ADR-0029).

6. **Screen control**: accessibility.py (macOS Accessibility API wrappers), controller.py (screen interaction orchestration: click, type, read, screenshot), app_launcher.py (application open/close/focus). macOS-only, uses pyobjc.

**Data flow for tool execution:**
```
Orchestrator (V2) → ToolRegistry.execute(name, args, context)
  → ToolDefinition lookup
  → Pydantic parameter validation
  → Security classification check → if DANGEROUS: DecisionValidator.validate() (V9)
  → Handler method invocation
  → Result wrapping in ToolResult
  → Return to orchestrator
```

### B.3 Interface Contracts

**3.1 ToolRegistry (central contract — consumed by Volume 2, Volume 8)**

```python
class ToolRegistry:
    def register(self, tool: ToolDefinition) -> None: ...
    def get_tool(self, name: str) -> ToolDefinition | None: ...
    def list_tools(self, category: str | None = None) -> list[str]: ...
    async def execute(self, tool_name: str, arguments: dict, context: dict | None = None) -> ToolResult: ...
    def get_openai_schema_for_query(self, query: str, max_tools: int = 20) -> list[dict]: ...
    def get_all_schemas(self) -> list[dict]: ...
```

**Inputs:** tool_name (str), arguments (dict validated against ToolDefinition.parameter_schema), context (optional dict with conversation_id, user preferences).
**Outputs:** ToolResult with `.success` (bool), `.result` (Any), `.error` (str | None), `.execution_time` (float).
**Dependencies consumed:** MemoryManager (V1) for semantic tool selection; DecisionValidator (V9) for DANGEROUS tool pre-flight.
**Dependencies served:** Volume 2 calls `execute()` and `get_openai_schema_for_query()`. Volume 8 calls `list_tools()` via API endpoints.

**3.2 ToolDefinition (schema contract)**

```python
@dataclass
class ToolDefinition:
    name: str
    description: str
    handler: Callable
    parameter_schema: type[BaseModel]  # Pydantic model
    result_schema: type[BaseModel] | None
    security: SecurityClassification  # SAFE | REQUIRES_CONFIRMATION | DANGEROUS
    category: str
    tags: list[str]
    requires_confirmation: bool
```

**3.3 Core tool handler contracts**

All handler methods follow the pattern:
```python
async def handler_method(self, **validated_params) -> dict | str | list:
    # Returns structured result or raises ToolExecutionError
```

- **FileTools**: Consumes filesystem. Path validation enforced via `_validate_path(path) -> Path`. Raises `ToolExecutionError` on blocked paths.
- **GitTools**: Consumes git CLI via subprocess. Returns structured dicts with stdout/stderr/return_code.
- **MemoryTools**: Consumes MemoryManager (V1). All layer access through `self.memory_manager.l{N}` accessors.
- **ConversationTools**: Consumes MemoryManager.l1 (working memory / conversation store).
- **SystemTools**: Consumes ToolRegistry (self-reference for tool introspection). Consumes MemoryManager for stats.
- **WebTools**: Consumes external HTTP (DuckDuckGo, URL fetch). Rate-limited. Returns sanitized content.

**3.4 STEM backend contracts (per ADR-0030)**

Each backend exposes:
```python
async def solve(self, problem: str, context: dict | None = None) -> ComputationResult:
    # Attempts symbolic/numerical solution first
    # Returns ComputationResult with .success, .result, .method ("symbolic"|"numerical"|"llm_fallback"), .steps
```

Domain tool handlers in `domain_tools.py` dispatch to the appropriate backend based on the `domain` parameter.

**3.5 Security tool contracts (per ADR-0028)**

- **ContainerManager**: `start_container()`, `stop_container()`, `execute_in_container(command)` — all require `EngagementScope` validation before execution.
- **EngagementScope**: `validate_target(target) -> bool` — checks target against authorized scope. Blocks out-of-scope operations.
- **ExternalToolManifest**: `get_tool_tier(tool_name) -> Tier` — returns PASSIVE/ACTIVE/INTRUSIVE classification. Higher tiers require escalating confirmation.

### B.4 Scope Triage

**REBUILD** (8 components — essential for Phase 0-2):

| Component | Verdict | Justification |
|---|---|---|
| `tool_registry.py` | REBUILD | Central infrastructure. Every tool depends on it. Phase 0 requirement. |
| `tool_schemas.py` | REBUILD | Pydantic parameter/result schemas. Required for typed tool execution. |
| `file_tools.py` | REBUILD | Core capability. File operations needed from Phase 0. |
| `git_tools.py` | REBUILD | Core capability. Version control integration needed from Phase 0. |
| `memory_tools.py` | REBUILD | Core capability. Memory CRUD needed as soon as memory layer (V1) exists. |
| `conversation_tools.py` | REBUILD | Core capability. Conversation management needed from Phase 1. |
| `system_tools.py` | REBUILD | Tool introspection and diagnostics. Needed for system health from Phase 1. |
| `web_tools.py` | REBUILD | Core capability. Web search and URL fetch needed from Phase 1. |

**DEFER** (24 components — valuable but not MVA-blocking):

| Component | Verdict | Justification |
|---|---|---|
| `domain_tools.py` | DEFER (Phase 3) | STEM tool dispatch layer. Valuable but depends on backends. |
| `register_domain_tools.py` | DEFER (Phase 3) | Registration wiring for domain tools. Follows domain_tools. |
| `backends/mathematics.py` | DEFER (Phase 3) | SymPy computation-first. High value per ADR-0030 but not MVA. |
| `backends/science.py` | DEFER (Phase 3) | SciPy science computation. Same phase as mathematics. |
| `backends/engineering.py` | DEFER (Phase 3) | NumPy/SciPy engineering computation. User is ME PhD — high personal value. |
| `backends/data_science.py` | DEFER (Phase 3) | Data analysis backends. Follows other STEM tools. |
| `backends/additive_manufacturing.py` | DEFER (Phase 4) | Specialized 3D printing/AM computation. Niche, later phase. |
| `container_manager.py` | DEFER (Phase 4) | Docker container lifecycle. Requires Docker Desktop. Security tool dependency. |
| `engagement_scope.py` | DEFER (Phase 4) | Pentest scope enforcement. Requires container_manager first. |
| `external_tool_manifest.py` | DEFER (Phase 4) | Tiered governance per ADR-0028. Depends on container infrastructure. |
| `external_tool_discovery.py` | DEFER (Phase 4) | CLI tool auto-discovery. Nice-to-have for extensibility. |
| `spec_generator.py` | DEFER (Phase 4) | OpenAPI spec generation from discovered tools. |
| `arsenal.py` | DEFER (Phase 4) | Kali tool templates per ADR-0029. Requires full security stack. |
| `memory_extended_tools.py` | DEFER (Phase 2) | Advanced memory operations. After core memory_tools works. |
| `email_tools.py` | DEFER (Phase 5) | Email API integration. Standard wrapper, not AI architecture. |
| `calendar_tools.py` | DEFER (Phase 5) | Calendar API integration. Standard wrapper. |
| `messaging_tools.py` | DEFER (Phase 5) | Messaging API integration. Standard wrapper. |
| `home_tools.py` | DEFER (Phase 5) | Home automation API integration. Standard wrapper. |
| `voice_tools.py` | DEFER (Phase 5) | Voice tool wrappers. Volume 6 owns voice; these are thin tool-layer adapters. |
| `screen_tools.py` | DEFER (Phase 5) | Screen control tool wrappers for screen/ subsystem. |
| `accessibility.py` | DEFER (Phase 5) | macOS Accessibility API. Platform-specific, not portable. |
| `controller.py` | DEFER (Phase 5) | Screen control orchestration. Depends on accessibility.py. |
| `app_launcher.py` | DEFER (Phase 5) | Application launching. Depends on screen control stack. |
| `sandbox_tools.py` | DEFER (Phase 2) | Sandbox execution tools. Volume 4 owns sandbox; these are thin wrappers. |

**KILL** (10 components — over-engineering, no clear consumer, or duplicated):

| Component | Verdict | Justification |
|---|---|---|
| `self_modify_tools.py` | KILL | Volume 4 owns self-modification. Tool-layer wrapper is unnecessary indirection. V4 SelfModifier is the interface. |
| `learning_tools.py` | KILL | Volume 3 owns learning pipeline. Tool wrappers for learning have no consumer in the tool-calling flow. |
| `research_tools.py` | KILL | Paper/research tools. Over-engineering. Web search covers the use case. |
| `analysis_tools.py` | KILL | Code/system analysis tools. Duplicates what system_tools + file_tools provide. |
| `architecture_tools.py` | KILL | Architecture inspection tools. Meta-tooling with no real consumer. |
| `benchmark_tools.py` | KILL | Benchmarking tools. Meta-assessment. Killed per Volume 0 anti-pattern A1. |
| `audit_tools.py` | KILL | Audit tools. Governance inspection belongs in Volume 9, not tool layer. |
| `drift_tools.py` | KILL | Drift detection tools. Monitoring concern, not a tool capability. |
| `profiler_tools.py` | KILL | Profiling tools. Developer tooling, not a user-facing capability. |
| `telemetry_tools.py` | KILL | Telemetry tools. Monitoring concern. Volume 7/8 owns telemetry endpoints. |
| `error_registry_tools.py` | KILL | Error registry tools. Infrastructure concern, not a tool capability. |
| `wiring_tools.py` | KILL | Integration wiring tools. Build-time concern, not runtime tool. |
| `governance_tools.py` | KILL | Governance tools. Volume 9 owns governance. Tool-layer wrappers are unnecessary indirection. |
| `event_tools.py` | KILL | Event bus tools. Infrastructure concern, not a user-facing tool capability. |

**Triage totals: 8 REBUILD, 24 DEFER, 14 KILL across 46 components.**

**Rebuild order within Volume 10:**
1. `tool_schemas.py` → `tool_registry.py` (infrastructure first)
2. `file_tools.py` → `git_tools.py` (filesystem tools, no memory dependency)
3. `memory_tools.py` → `conversation_tools.py` (requires V1 MemoryManager)
4. `system_tools.py` → `web_tools.py` (requires registry self-reference and HTTP)

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
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (30+ tool files, 3 screen files, 20+ docs), context brief, and 5 known failure warnings including 80+ tools needing aggressive triage | Created the tools/capabilities analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V10-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
|| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 Source Manifest per DISTILLATION_PROTOCOL.md Section 5 | Labeled which files agents should read in full vs. skim during Phase 1 |
|| v5 | 2026-03-10 | Distillation Agent V10 | Phase 1: Filled B.1 (subsystem purpose), B.2 (architecture overview with 6-component layer diagram), B.3 (interface contracts for ToolRegistry, ToolDefinition, core handlers, STEM backends, security tools), B.4 (scope triage: 8 REBUILD, 24 DEFER, 14 KILL across 46 components with per-component justifications) | Agent analyzed all 42 tool files and wrote the design specification for what the tool system should look like in the rebuild |
