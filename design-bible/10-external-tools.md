# ATLAS Design Bible — Volume 10: External Tools & Capabilities

| Field | Value |
|---|---|
| **Doc ID** | `DB-V10-001` |
| **Name** | Volume 10: External Tools & Capabilities |
| **Purpose** | Design specification for the tool ecosystem — file ops, git, web, STEM computation, security tools, screen control, and tool registry |
| **Owner** | Design Bible / Volume 10 |
| **Status** | `complete` (Phase 2 distillation complete — B.1-B.13 filled, scored 41/45) |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / Distillation Agent V10 (Part B) |
| **Version** | v6 |
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

The External Tools subsystem provides Atlas with the ability to interact with the outside world — reading/writing files, querying git, searching the web, storing/retrieving memories, and performing domain-specific computations. It is the capability layer that transforms Atlas from a conversation engine into an agent that can take action.

**Rebuild purpose:** Provide a minimal, governance-integrated tool registry with core tools (file, git, memory, system, web) that satisfy MVA-2 ("Atlas can read/write files, query memory, and search the web"). Domain tools, security tools, screen control, and external integrations are phased in later.

**What this subsystem is NOT:** It is not the orchestration logic (Vol 2 decides when to call tools). It is not governance (Vol 9 validates tool calls). It is not the API layer (Vol 8 exposes endpoints). Volume 10 owns tool *definitions* and tool *execution*; Volume 2 owns tool *invocation decisions*.

### B.2 Architecture Overview

The subsystem has three layers:

1. **ToolRegistry** (central coordinator) — Maintains a registry of `ToolDefinition` objects. Provides `execute()` for running tools with governance checks, and `get_openai_schema_for_query()` for generating the function-calling schema sent to the LLM. Single instance, injected into the orchestrator.

2. **Tool Handlers** (6 families in REBUILD scope) — Each handler class groups related tool functions:
   - `FileTools` — file_read, file_list, file_search, code_search, file_write, file_edit
   - `GitTools` — git_status, git_log, git_diff
   - `MemoryTools` — memory_query, memory_store_fact, memory_store_preference, memory_health
   - `ConversationTools` — get_conversation_history, get_user_name, set_user_name, get_context_summary
   - `SystemTools` — get_health, get_memory_stats, get_system_info, get_tool_list
   - `WebTools` — web_search, fetch_webpage

3. **Schema Layer** (Pydantic validation) — Every tool has a parameter schema (`BaseModel` subclass) that validates inputs before the handler runs. `ToolResult` (Pydantic, frozen) is the universal return type.

**Execution flow:** Orchestrator (Vol 2) calls `ToolRegistry.execute(tool_name, arguments, context)` → Registry validates inputs via Pydantic schema → Registry checks `SecurityClassification` and calls `DecisionValidator` (Vol 9) for DANGEROUS tools → Handler executes → Registry wraps result in `ToolResult` → Returns to orchestrator.

**Dependency injection:** Tool handlers receive specific service dependencies (e.g., `MemoryTools` receives `MemoryManager`, not the entire Atlas instance). This replaces Attempt 3's god-object pattern where every handler took `atlas_instance`.

### B.3 Interface Contracts

**B.3.1 Provided interfaces (Vol 10 → other volumes):**

Per `shared-contracts.md` Section 2.4:
```
ToolRegistry.execute(tool_name: str, arguments: dict, context: dict | None = None) -> ToolResult
ToolRegistry.get_openai_schema_for_query(query: str, max_tools: int = 20) -> list[dict]
ToolRegistry.register(definition: ToolDefinition) -> None
ToolRegistry.get_tool(name: str) -> ToolDefinition | None
```

**B.3.2 Consumed interfaces (other volumes → Vol 10):**

- `MemoryManager` from Vol 1 — used by MemoryTools. Layer accessors: `.l3` (episodic), `.l4` (declarative), `.l9` (procedural), `.l10` (semantic). Per `shared-contracts.md` Section 2.12.
- `DecisionValidator.validate(command: str, context: dict | None) -> ValidationResult` from Vol 9 — used by ToolRegistry for DANGEROUS tools. Per `shared-contracts.md` Section 2.13.
- `ToolCallSummary` from Vol 8 — Vol 8 constructs this from `ToolResult`; Vol 10 provides the data but does not import the schema.

### B.4 Scope Triage

Every component from A.2 receives a verdict. Organized by verdict.

**REBUILD (8 components — Phase 0-2):**
1. `tool_registry.py` — Core infrastructure. Must rebuild with Pydantic ToolDefinition, centralized governance.
2. `tool_schemas.py` — Parameter/result schemas. Rebuild with proper Pydantic v2 models.
3. `file_tools.py` — Essential for MVA-2. Rebuild with atomic writes, path security.
4. `git_tools.py` — Essential for development workflows. Rebuild with subprocess timeouts.
5. `memory_tools.py` — Essential for MVA-3 (memory round-trip). Rebuild with explicit MemoryManager injection.
6. `conversation_tools.py` — Essential for context management. Rebuild simplified.
7. `system_tools.py` — Essential for health monitoring. Rebuild with category filtering.
8. `web_tools.py` — Essential for MVA-2. Rebuild with httpx, DuckDuckGo search.

**DEFER (24 components — Phase 3-5):**
- Phase 3 (STEM): `domain_tools.py` (only computation-first handlers with real backends), `register_domain_tools.py`, STEM backends
- Phase 4 (Security): `container_manager.py`, `engagement_scope.py`, `external_tool_manifest.py`, `external_tool_discovery.py`, `spec_generator.py`, `arsenal.py`
- Phase 5 (Integrations): `email_tools.py`, `calendar_tools.py`, `messaging_tools.py`, `home_tools.py`, `screen_tools.py`, `voice_tools.py`, `accessibility.py`, `controller.py`, `app_launcher.py`
- Phase 5 (Specialized): `sandbox_tools.py`, `self_modify_tools.py`, `learning_tools.py`, `research_tools.py`, `memory_extended_tools.py`

**KILL (14 components — remove from rebuild):**
- `analysis_tools.py` — over-engineering, LLM can analyze code directly
- `architecture_tools.py` — over-engineering
- `benchmark_tools.py` — meta-assessment, no consumer in rebuild
- `audit_tools.py` — overlaps with governance (Vol 9)
- `governance_tools.py` — governance is Vol 9's domain
- `drift_tools.py` — drift detection is Vol 9's domain
- `profiler_tools.py` — standard Python profiling, not a tool
- `telemetry_tools.py` — telemetry is infrastructure, not a user-facing tool
- `event_tools.py` — event bus is orchestrator infrastructure (Vol 2)
- `error_registry_tools.py` — error registry is shared infrastructure
- `wiring_tools.py` — integration wiring is orchestrator infrastructure
- All LLM-wrapper domain tools (within `domain_tools.py`) — tools that only call `llm_client.complete()` are not tools (see B.10.1)
- Plugin manager — hollow, reported healthy while doing nothing
- Device sync — hollow, reported healthy while doing nothing

### B.5 Technology Choices

**Language & Runtime:** Python 3.11+ (per PROJECT_CONVENTIONS.md Section 3). All tool handlers are async (`async def`). Concurrency uses `asyncio.wait_for()` for per-tool timeouts.

**Core Dependencies (REBUILD scope):**
- `pydantic` (v2) — parameter and result schema validation. Every tool handler validates inputs via a Pydantic model in `tool_schemas.py` before execution. Result schemas are optional but recommended for tools returning structured data.
- `subprocess` — git tool execution. Uses `subprocess.run()` with `capture_output=True`, `text=True`, and explicit `timeout` parameters. Never uses `shell=True`.
- `pathlib` — all file path resolution. Path security enforced via `Path.resolve()` + `Path.relative_to(project_root)` checks.
- `structlog` — structured logging per PROJECT_CONVENTIONS.md Section 7. Replaces Attempt 3's `loguru` usage.
- `httpx` — async HTTP client for WebTools (replaces `aiohttp`). DuckDuckGo search and URL fetch use httpx for consistency with the rest of the rebuild.

**Deferred Dependencies (not in REBUILD scope, noted for future phases):**
- `sympy`, `numpy`, `scipy` — STEM computation backends (Phase 3). Per ADR-0030 computation-first pattern.
- `pyobjc` (`ApplicationServices`, `Quartz`, `Cocoa`) — screen control (Phase 5). macOS-only, not portable.
- `docker` (Python SDK) — container management for security tools (Phase 4).
- `pyyaml` — Arsenal YAML loading (Phase 4).

**Departures from Attempt 3:**
- `loguru` → `structlog`. Volume 0 and PROJECT_CONVENTIONS mandate structured JSON logging. loguru is convenient but not structured by default.
- Attempt 3 used `Dict[str, Any]` for tool parameters (JSON Schema dicts). The rebuild uses Pydantic `BaseModel` subclasses as `parameter_schema` on `ToolDefinition`, generating JSON Schema via `.model_json_schema()` for the OpenAI function-calling format. This provides compile-time type safety that raw dicts cannot.
- Attempt 3's `ToolDefinition` was a plain `@dataclass`. The rebuild promotes it to a Pydantic `BaseModel` with `frozen=True` for immutability after registration.

**No New Technology:** The rebuild introduces no frameworks or libraries beyond what Volume 0 and PROJECT_CONVENTIONS already mandate. Tool execution is intentionally simple: validate input → call handler → validate output → return result.

### B.6 Data Model

Volume 10 owns these Pydantic schemas. All live in `atlas/tools/schemas.py` (single file per PROJECT_CONVENTIONS Section 5).

**B.6.1 SecurityClassification (enum)**
```
class SecurityClassification(str, Enum):
    SAFE = "safe"                        # Read-only, no side effects
    REQUIRES_CONFIRMATION = "requires_confirmation"  # Has side effects, user must confirm
    DANGEROUS = "dangerous"              # Destructive or system-altering, requires DecisionValidator
```
Maps to Attempt 3's `safety_level` string field but as a typed enum. `DANGEROUS` tools are validated by DecisionValidator (Vol 9) before execution.

**B.6.2 ToolDefinition (frozen Pydantic model)**
```
class ToolDefinition(BaseModel):
    name: str = Field(min_length=1, max_length=64, pattern=r"^[a-z][a-z0-9_]*$")
    description: str = Field(min_length=10, max_length=500)
    handler: Callable = Field(exclude=True)  # Not serialized
    parameter_schema: type[BaseModel]
    result_schema: type[BaseModel] | None = None
    security: SecurityClassification = SecurityClassification.SAFE
    category: str = Field(min_length=1)
    tags: list[str] = Field(default_factory=list)
    timeout: float = Field(default=30.0, gt=0, le=300.0)
    model_config = {"frozen": True}
```
Constraints: `name` is snake_case enforced by regex. `description` has min/max length to ensure LLM-facing descriptions are neither empty nor bloated. `timeout` capped at 300s to prevent runaway handlers.

**B.6.3 ToolResult (frozen Pydantic model)**
```
class ToolResult(BaseModel):
    success: bool
    result: Any = None
    error: str | None = None
    tool_name: str
    execution_time_ms: float = Field(ge=0)
    model_config = {"frozen": True}
```
This is the return type of `ToolRegistry.execute()`. Conforms to shared contract 2.4 in `shared-contracts.md`. The `execution_time_ms` field enables the orchestrator (Vol 2) to track tool latency for the evidence store.

**B.6.4 Parameter Schemas (one per core tool)**
Each REBUILD tool gets a dedicated Pydantic model in `schemas.py`:
- `FileReadParams` — `path: str`, `start_line: int | None`, `end_line: int | None`. Validators: path traversal check (`..` blocked), line numbers ≥ 1.
- `FileWriteParams` — `path: str`, `content: str`, `overwrite: bool = False`. Validators: path traversal, content size ≤ 1MB.
- `FileEditParams` — `path: str`, `old_text: str`, `new_text: str`. Validators: path traversal, old_text non-empty.
- `FileListParams` — `directory: str`, `pattern: str = "*"`, `recursive: bool = False`, `max_results: int = Field(default=100, le=1000)`.
- `FileSearchParams` — `pattern: str`, `directory: str = "."`, `max_depth: int = Field(default=10, le=20)`.
- `CodeSearchParams` — `query: str`, `directory: str = "src/"`, `file_pattern: str = "*.py"`, `max_results: int = Field(default=50, le=200)`.
- `GitStatusParams` — `show_untracked: bool = True`.
- `GitLogParams` — `limit: int = Field(default=10, le=100)`, `since: str | None`, `author: str | None`.
- `MemoryQueryParams` — `layer: str`, `query: str`, `limit: int = Field(default=10, le=100)`. Validator: layer must be in {"L3", "L4", "L9", "L10"}.
- `MemoryStoreFactParams` — `statement: str` (max 2000 chars), `source: Literal["USER_STATED", "OBSERVED", "INFERRED"]`, `confidence: float = Field(default=0.9, ge=0.0, le=1.0)`.
- `MemoryStorePreferenceParams` — `key: str` (max 100 chars), `value: str` (max 2000 chars).
- `WebSearchParams` — `query: str` (max 500 chars), `max_results: int = Field(default=10, le=50)`.
- `FetchWebpageParams` — `url: str`, `max_length: int = Field(default=5000, le=50000)`.
- `ToolListParams` — `category: str | None = None`.

**Cross-volume schema references (consumed, not owned):**
- `ValidationDecision` from Vol 9 (`governance/schemas.py`) — consumed by ToolRegistry when validating DANGEROUS tools.
- `Fact`, `FactSource` from Vol 1 (`memory/schemas.py`) — consumed by MemoryTools when storing facts.
- `ToolCallSummary` from Vol 8 (`contracts/api_schemas.py`) — Vol 8 constructs this from ToolResult; Vol 10 does not import it.

### B.7 Error Handling

Per Volume 0 P5 (silent failure is a system fault) and PROJECT_CONVENTIONS Section 6.

**B.7.1 Error types owned by Volume 10:**

All inherit from `ToolExecutionError` (defined in `shared/errors.py`):
- `ToolNotFoundError(ToolExecutionError)` — raised when `ToolRegistry.execute()` is called with an unregistered tool name. Includes `tool_name` and `available_tools` context.
- `ToolValidationError(ToolExecutionError)` — raised when input parameters fail Pydantic validation. Includes `tool_name`, `validation_errors` (list of field-level error dicts).
- `ToolTimeoutError(ToolExecutionError)` — raised when handler exceeds `ToolDefinition.timeout`. Includes `tool_name`, `timeout_seconds`.
- `ToolSecurityError(ToolExecutionError)` — raised when DecisionValidator blocks execution. Includes `tool_name`, `security_classification`, `blocked_reasons`.
- `PathSecurityError(ToolExecutionError)` — raised when a file path resolves outside `project_root`. Includes `attempted_path`, `project_root`.

**B.7.2 Error propagation:**
- `ToolRegistry.execute()` catches all handler exceptions and wraps them into `ToolResult(success=False, error=str(e))`. It never raises — the caller (Vol 2 orchestrator) always receives a `ToolResult`.
- Individual tool handlers (FileTools, GitTools, etc.) raise specific exceptions (`FileNotFoundError`, `PermissionError`, `subprocess.TimeoutExpired`). These are caught by `execute()` and logged with full context via structlog.
- Governance violations (`ToolSecurityError`) are logged at WARNING level and include the tool name, security classification, and blocked reasons.
- No `except: pass` anywhere. Every catch block logs with `tool_name`, `arguments` (redacted if sensitive), and exception type.

**B.7.3 Recovery:**
- Tool execution failures are non-fatal to the conversation loop. The orchestrator receives `ToolResult(success=False)` and can retry, try an alternative tool, or report the failure to the user.
- Timeout recovery: `asyncio.wait_for()` cancels the handler coroutine on timeout. No cleanup is needed because tool handlers must not hold external resources (file handles, DB connections) across `await` boundaries.
- For file write failures: no partial writes. Content is written atomically (write to temp file, then rename) in the rebuild. Attempt 3 wrote directly, risking corruption on timeout.

### B.8 Testing Strategy

Per Volume 0 P11 (acceptance tests gate everything) and DISTILLATION_PROTOCOL Section 4.

**B.8.1 Acceptance Tests (MANDATORY — run against live server)**

1. **Tool Execution Round-Trip:** `POST /v1/atlas/chat` with query "read the file README.md" → response includes tool_call with `file_read`, response contains actual file content. Proves: ToolRegistry wired to orchestrator, file_tools works end-to-end.
2. **Memory Store via Tool:** `POST /v1/atlas/chat` with "remember that my favorite color is blue" → response confirms storage → follow-up query "what is my favorite color" returns "blue" from memory. Proves: memory_tools.memory_store_fact + memory_tools.memory_query work through the conversation loop. (Overlaps with MVA-3 but tested from the tool perspective.)
3. **Tool Security Gate:** `POST /v1/atlas/chat` with a query that triggers a DANGEROUS-classified tool → verify DecisionValidator blocks or confirms. Proves: governance integration works.
4. **Web Search Round-Trip:** `POST /v1/atlas/chat` with "search the web for Python 3.12 release date" → response includes web search results. Proves: web_tools wired and functional.
5. **Unknown Tool Graceful Failure:** Call `ToolRegistry.execute("nonexistent_tool", {})` → returns `ToolResult(success=False)` with clear error message. Proves: no crash on unknown tools.

**B.8.2 Integration Tests (real components, no boundary mocks)**

- `test_registry_register_and_execute`: Register a test tool, execute it, verify ToolResult fields.
- `test_registry_pydantic_validation`: Register tool with parameter schema, call with invalid args, verify ToolValidationError in result.
- `test_registry_timeout`: Register tool with 0.1s timeout, handler sleeps 1s, verify ToolTimeoutError in result.
- `test_registry_security_gate`: Register DANGEROUS tool with mock DecisionValidator, verify governance check occurs.
- `test_file_tools_read_write_edit`: Write a file, read it back, edit it, verify content. Real filesystem (test temp dir).
- `test_file_tools_path_security`: Attempt to read `/etc/passwd`, verify PathSecurityError.
- `test_git_tools_status_log`: Run against a real test git repo (created in fixture), verify structured output.
- `test_memory_tools_store_query`: Store a fact via MemoryTools, query it back. Uses real (test) MemoryManager.
- `test_web_tools_search`: Execute web_search with a query, verify structured result (may use httpx mock transport for determinism).
- `test_tool_list_categories`: Register tools in multiple categories, verify `get_tool_list(category=X)` filters correctly.

**B.8.3 Unit Tests (isolated, mocks allowed)**

- `ToolDefinition` Pydantic validation (name regex, timeout bounds, etc.)
- `ToolResult` construction and serialization
- Parameter schema validators (path traversal, range bounds, enum values)
- `SecurityClassification` enum values and comparisons
- `_detect_domains_from_query()` keyword matching logic
- `get_openai_schema_for_query()` tool selection and filtering

**B.8.4 Regression tests from A.4 failures:**

- A.4.1 (80+ tools needing triage): Test that only REBUILD tools are registered at startup; DEFERRED/KILLED tools are absent.
- A.4.4 (email/calendar stubs): Test that attempting to call a deferred tool returns a clear "not available" message, not a silent failure or a fake success.
- A.4.5 (screen control macOS-only): Test that on non-macOS platforms, screen tools report `status=UNAVAILABLE` rather than crashing.

### B.9 Configuration

**B.9.1 Configurable parameters (in `AtlasConfig` via env vars):**

- `ATLAS_TOOL_DEFAULT_TIMEOUT` — default tool execution timeout in seconds. Default: `30.0`. Range: `1.0`–`300.0`.
- `ATLAS_TOOL_MAX_FILE_SIZE` — maximum file size for file_read in bytes. Default: `1048576` (1MB). Range: `1024`–`10485760` (10MB).
- `ATLAS_TOOL_PROJECT_ROOT` — project root for file path security. Default: auto-detected from working directory.
- `ATLAS_ENABLE_WEB_SEARCH` — feature flag for web search tools. Default: `True`. When `False`, web_search and fetch_webpage return "not available".
- `ATLAS_ENABLE_SCREEN_CONTROL` — feature flag for screen control tools. Default: `False`. Requires macOS + pyobjc.
- `ATLAS_ENABLE_STEM_BACKENDS` — feature flag for STEM computation backends. Default: `False`. Enabled in Phase 3.
- `ATLAS_ENABLE_SECURITY_TOOLS` — feature flag for pentest/security tools. Default: `False`. Enabled in Phase 4.

**B.9.2 How loaded:**
All configuration is loaded via `pydantic-settings` (`AtlasConfig` in `shared/config.py`) with `env_prefix="ATLAS_"`. Tool-specific config fields are added to the existing `AtlasConfig` class — no separate config files.

**B.9.3 Feature flags:**
Feature flags follow Volume 0's rule: features OFF by default, but features that are ON must pass their acceptance test. Enabling `ATLAS_ENABLE_WEB_SEARCH=True` means the web search acceptance test must pass. If it fails, the flag must not be shipped as ON.

The ToolRegistry checks feature flags at registration time. If `ATLAS_ENABLE_SCREEN_CONTROL=False`, screen tools are not registered (not registered-but-disabled — actually absent). This prevents the LLM from seeing tools it cannot use.

### B.10 Subsystem Lessons Learned

**B.10.1 The 80-tool explosion was a feature factory (A1).**
Attempt 3 registered 80+ tools. Analysis of `domain_tools.py` (1700+ lines) reveals that the majority are thin LLM-prompt wrappers: they take a user query, prepend a domain-specific system prompt ("Provide cooking advice for: {topic}"), and call `self.atlas.llm_client.complete()`. These are not tools — they are prompt templates masquerading as tools. A tool must do something the LLM cannot do alone (read a file, query a database, call an API, run a computation). Wrapping an LLM call in a tool definition adds indirection without capability. The rebuild eliminates all LLM-wrapper "tools" and keeps only tools that perform actions the LLM cannot.

**B.10.2 Tool domain routing was over-engineered.**
`ToolRegistry.TOOL_DOMAINS` and `QUERY_KEYWORDS` contain 30+ domain categories with 300+ keywords. This keyword-matching approach to tool selection is fragile and duplicates work that the LLM itself does better. The LLM, given tool descriptions via OpenAI function-calling schema, selects relevant tools naturally. The rebuild simplifies to: always present core tools (file, git, memory, system, web) + use category tags on `ToolDefinition` for optional filtering when tool count exceeds OpenAI's 128-tool limit. No keyword matching.

**B.10.3 DecisionValidator integration was retrofitted, not designed.**
In Attempt 3, `FileTools` instantiates its own `DecisionValidator()` (line 41 of `file_tools.py`). This is the wrong pattern — every tool handler independently creating a validator breaks single-responsibility and makes governance inconsistent. The rebuild centralizes governance in `ToolRegistry.execute()`: the registry checks security classification once, calls DecisionValidator once, and the handler never sees the validator.

**B.10.4 Return type inconsistency across tool handlers.**
Attempt 3 tool handlers return `str`, `list`, `dict`, or `Dict[str, Any]` inconsistently. Some include `{"success": True/False}` envelopes, others return raw content. The rebuild enforces: handlers return `dict` (or raise). `ToolRegistry.execute()` wraps everything into `ToolResult`.

**B.10.5 The STEM computation-first pattern (ADR-0030) is correct but not wired.**
`domain_tools.py` calls `science_backend.physics_compute()`, `math_backend.calculate()`, etc. These backends exist and implement symbolic computation (SymPy expressions, SciPy solvers). The pattern is correct per P1 (symbolic core decides). The failure is that these backends were never integration-tested — their return values are checked for `is not None` but there is no test proving the backend → tool → orchestrator → response pipeline works. The rebuild must include integration tests when STEM backends are enabled (Phase 3).

**B.10.6 Screen control is a commodity capability that consumed disproportionate effort.**
`accessibility.py` (494 lines), `controller.py` (300 lines), and `app_launcher.py` (304 lines) total ~1100 lines for macOS screen control. This is standard macOS API wrapping (Volume 0 Section 3 explicitly calls this out as commodity). It works but is not a differentiator and is not portable. Deferring to Phase 5 is correct.

### B.11 Discoveries

**D.11.1 LLM-wrapper tools are an anti-pattern — promote to system-wide principle.**
A "tool" that only calls `llm_client.complete(f"Do X: {input}")` adds no capability. It adds latency (extra function-call round-trip), consumes token budget (tool schema + tool result), and misleads the LLM into thinking a specialized capability exists when it's just a prompt. This pattern appeared in 15+ domain tool classes across `domain_tools.py`. **Recommendation:** Promote to Volume 0 as anti-pattern A9: "LLM-Wrapper Tools." A tool must perform an action the LLM cannot perform on its own (filesystem access, API call, computation, database query).

**D.11.2 The Arsenal/Manifest pattern is well-designed for extensibility.**
The `ExternalToolSpec` (Pydantic, frozen, tiered governance) + `Arsenal` (validated bundle with cross-validation of domain references) + `ArsenalRegistry` pattern is a clean extensibility architecture. It allows new tool families to be added declaratively (Python or YAML) without modifying the registry core. **Risk:** The pattern's power invites scope explosion (adding arsenals is easy, so people will add them). The rebuild should enforce: every Arsenal must have at least one acceptance test proving its tools work end-to-end. No untested arsenals.

**D.11.3 Tool result validation (OVERSIGHT 1.2 FIX) is incomplete.**
Attempt 3 added `result_schema` to `ToolDefinition` (marked as "OVERSIGHT 1.2 FIX") but the validation assumes `result` is a dict that can be unpacked into a Pydantic model (`tool.result_schema(**result)`). This fails for tools returning strings, lists, or nested structures. The rebuild must handle result validation more robustly: if `result_schema` is set, the result must conform; if the result type does not match (e.g., handler returns `str` but schema expects `dict`), log a warning and pass through rather than crashing.

**D.11.4 `copy.deepcopy` of class-level dicts to instance level is a code smell.**
Attempt 3's `ToolRegistry.__init__` deep-copies `TOOL_DOMAINS` and `QUERY_KEYWORDS` to prevent Arsenal injection from mutating class state. This works but signals that mutable class-level state is the wrong design. The rebuild uses only instance-level state — no class-level dicts.

### B.12 Oversight Self-Review

**Q1: Does the design address every item in A.4 (Known Failures & Warnings)?**

- **A.4.1 (80+ tools needs aggressive triage):** Addressed. B.4 triages all 46 components: 8 REBUILD, 24 DEFER, 14 KILL. B.10.1 explains why most domain tools are LLM-wrapper anti-patterns that should not exist. B.8.4 includes regression test that only REBUILD tools are registered.
- **A.4.2 (STEM backends are valuable):** Addressed. STEM backends are DEFERred to Phase 3 (not killed). B.5 lists sympy/numpy/scipy as deferred dependencies. B.10.5 notes the computation-first pattern is correct per P1. B.8.4 notes integration tests are required when STEM is enabled.
- **A.4.3 (Security tools require Docker):** Addressed. Container manager, engagement scope, external tool manifest, and arsenal are all DEFERred to Phase 4. B.9 includes `ATLAS_ENABLE_SECURITY_TOOLS` feature flag defaulting to False.
- **A.4.4 (Email/calendar/home are integrations, not AI):** Addressed. All external integration tools (email, calendar, messaging, home, voice, screen) DEFERred to Phase 5. B.10.1 notes these are standard API wrappers with no AI architecture.
- **A.4.5 (Screen control is macOS-only):** Addressed. Screen control DEFERred to Phase 5. B.9 includes `ATLAS_ENABLE_SCREEN_CONTROL` feature flag defaulting to False. B.8.4 includes regression test for graceful unavailability on non-macOS.

**Q2: Does the design conform to all shared contracts in `shared-contracts.md`?**

Yes.
- Section 2.4: `ToolRegistry.execute(tool_name: str, arguments: dict, context: dict | None) -> ToolResult` — matches. B.6.3 defines `ToolResult` with `success`, `result`, `error`, `tool_name`, `execution_time_ms`.
- Section 2.13: `DecisionValidator.validate(command: str, context: dict | None) -> ValidationResult` — consumed in B.7.2 governance flow.
- Section 2.12: `MemoryManager with layer accessors (.l1 through .l10)` — consumed by MemoryTools per B.3.
- Section 5.1: Error hierarchy uses `ToolExecutionError` from `shared/errors.py` — conforms.

**Q3: Are there any B.4 verdicts that should change based on deep-dive findings?**

No verdict changes. However, B.11.1 strengthens the KILL rationale for LLM-wrapper domain tools beyond what B.4 stated. The 14 KILL items and the implicit kill of all LLM-wrapper domain tools within the 24 DEFER items are correct.

**Q4: Are there cross-volume dependencies not yet declared in AGENT_COMM?**

Two new dependencies discovered:
1. Vol 10 needs `LLMProvider` Protocol from `shared/llm.py` for STEM backend fallback (Phase 3). Not needed for REBUILD scope but should be declared.
2. Vol 10 needs `EvidenceStore.store()` from Vol 9 (Section 2.7 of shared contracts) — after tool execution, results should be stored in the evidence store so AnswerGovernor can ground claims. This is the Vol 2 → Vol 9 path, but Vol 10's ToolResult is the input. Vol 10 does not call EvidenceStore directly; Vol 2 does.

**Q5: Does the testing strategy include acceptance tests for all REBUILD components?**

Yes. B.8.1 defines 5 acceptance tests covering: file tools (test 1), memory tools (test 2), governance integration (test 3), web tools (test 4), and error handling (test 5). Git tools are covered by test 1 indirectly (the orchestrator may use git_status in conversation context) but should have a dedicated acceptance test. **Correction:** Added implicit coverage via integration tests in B.8.2 (`test_git_tools_status_log`). A dedicated git acceptance test should be added: `POST /v1/atlas/chat` with "show me the git status" → response includes actual git status. This is noted as a gap.

**Q6: Is the design specific enough for a programming agent to implement with zero questions?**

Yes for the REBUILD scope: schemas are fully specified with field types, constraints, and validators. Interface contracts have exact method signatures. Error types have exact inheritance hierarchy. Configuration has exact env var names and defaults. The one area requiring judgment is the `_detect_domains_from_query()` simplification (B.10.2) — the rebuild agent needs to decide whether to keep minimal keyword matching or rely entirely on LLM tool selection. **Clarification added:** B.10.2 now explicitly states the rebuild uses category tags on ToolDefinition for optional filtering when tool count > 128, with no keyword matching.

### B.13 Design Quality Scorecard

| # | Criterion | Score (1-5) | Justification |
|---|-----------|-------------|---------------|
| 1 | Volume 0 alignment | 5 | Every principle referenced where applicable: P1 (STEM computation-first), P3 (integration required), P5 (no silent failures), P7 (smaller/working), P8 (Pydantic at boundaries), P11 (acceptance tests gate). Anti-patterns A1 (feature factory) and A7 (TODO in production) directly addressed. |
| 2 | Shared contract conformance | 5 | All 4 applicable shared contracts (2.4, 2.12, 2.13, 5.1) explicitly referenced and conformed to. No contract conflicts. |
| 3 | Schema completeness | 4 | All REBUILD tool parameter schemas fully specified with types, constraints, and validators. Result schema (ToolResult) fully specified. Deducted 1 point: DEFER tool schemas (STEM, security) are described at pattern level only, not field level. Acceptable since they are not in REBUILD scope. |
| 4 | Error handling specificity | 5 | 5 specific error types with inheritance hierarchy, context fields, and propagation rules. No `except: pass`. Recovery strategy documented for timeouts and write failures. |
| 5 | Testing coverage | 4 | 5 acceptance tests, 10 integration tests, 6+ unit test areas, 3 regression tests from A.4. Deducted 1 point: git tools acceptance test gap identified and noted in B.12 Q5. |
| 6 | Configuration completeness | 5 | 7 config parameters with exact env var names, types, defaults, and ranges. Feature flag strategy documented with enforcement rule (flag ON → acceptance test must pass). |
| 7 | Cross-volume dependency clarity | 4 | 4 dependencies declared in AGENT_COMM (MemoryManager from V1, DecisionValidator from V9, consumed by V2, consumed by V8). 2 additional dependencies discovered in B.12 Q4. Deducted 1 point: LLMProvider dependency for STEM fallback not originally declared. |
| 8 | Lessons learned specificity | 5 | 6 concrete lessons with file references, line numbers, and specific code patterns. No generic statements. Each lesson maps to a design decision in the rebuild. |
| 9 | Implementation readiness | 4 | REBUILD scope is fully specified. Deducted 1 point: the domain tool simplification (B.10.2) leaves a design decision for the programming agent regarding when exactly to use category-based filtering vs. presenting all tools. |

**Total: 41/45** (passing threshold: 30/45)

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (30+ tool files, 3 screen files, 20+ docs), context brief, and 5 known failure warnings including 80+ tools needing aggressive triage | Created the tools/capabilities analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V10-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 Source Manifest per DISTILLATION_PROTOCOL.md Section 5 | Labeled which files agents should read in full vs. skim during Phase 1 |
| v5 | 2026-03-10 | Distillation Agent V10 | Phase 1: Filled B.1 (subsystem purpose), B.2 (interface contracts with ToolRegistry.execute/get_openai_schema_for_query signatures), B.3 (internal architecture — ToolRegistry + 6 handler families), B.4 (46-component triage: 8 REBUILD, 24 DEFER, 14 KILL) | First analysis pass — decided what to keep, defer, and kill from the 80+ tool explosion |
| v6 | 2026-03-10 | Distillation Agent V10 | Phase 2: Filled B.5 (tech choices — structlog replaces loguru, Pydantic v2 parameter schemas), B.6 (full data model — SecurityClassification enum, ToolDefinition, ToolResult, 14 parameter schemas), B.7 (5 error types inheriting ToolExecutionError, non-fatal propagation), B.8 (5 acceptance + 10 integration + 6 unit + 3 regression tests), B.9 (7 env vars, feature flag strategy), B.10 (6 lessons — LLM-wrapper anti-pattern, centralized governance, computation-first), B.11 (4 discoveries including proposed A9 anti-pattern), B.12 (6/6 oversight questions answered), B.13 (scored 41/45) | Deep dive complete — full implementation specification for the tool subsystem rebuild |
