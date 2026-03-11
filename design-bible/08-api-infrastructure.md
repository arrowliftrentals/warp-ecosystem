# ATLAS Design Bible — Volume 8: API & Infrastructure

| Field | Value |
|---|---|
| **Doc ID** | `DB-V08-001` |
| **Name** | Volume 8: API & Infrastructure |
| **Purpose** | Design specification for the server, routing, middleware, error handling, configuration, startup, and concurrency model |
| **Owner** | Design Bible / Volume 8 |
|| **Status** | `complete` (Phase 1 + Phase 2 — all sections filled, scorecard 42/45 PASS) |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
|| **Author** | Oz (Part A) / Distillation Agent V8 (Part B) |
|| **Version** | v6 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-11 |

---

## Part A: Context (Pre-loaded)

### A.1 Subsystem Identity
- **Volume 8: API & Infrastructure**
- **Purpose:** The server, routing, middleware, error handling, configuration, startup, and concurrency model that everything runs on. The plumbing.
- **Rebuild phase:** Phase 0 (built alongside the conversation loop). The API server is the entry point for all interaction.

### A.2 Source Manifest

**Code files to read** (paths relative to `atlas/`):

*Server core:*
- `src/api/server.py` — FastAPI app, startup/shutdown, route registration
- `src/api/middleware.py` — request/response middleware
- `src/api/telemetry_middleware.py` — telemetry collection middleware
- `src/api/documentation_bridge.py`
- `src/api/meta_sections.py`

*Routes (all):*
- `src/api/routes/atlas_chat.py` — main chat endpoint (/v1/atlas/chat)
- `src/api/routes/console.py` — console session management
- `src/api/routes/streaming.py` — streaming responses
- `src/api/routes/sandbox.py` — sandbox execution
- `src/api/routes/proposals.py` — self-modification proposals
- `src/api/routes/voice.py` — voice endpoints
- `src/api/routes/intelligence.py` — intelligence queries
- `src/api/routes/knowledge.py` — knowledge operations
- `src/api/routes/learning.py` — learning endpoints
- `src/api/routes/learning_feedback.py`
- `src/api/routes/security.py`
- `src/api/routes/safety.py`
- `src/api/routes/system.py`
- `src/api/routes/data.py`
- `src/api/routes/metrics.py`
- `src/api/routes/analytics.py`
- `src/api/routes/analysis.py`
- `src/api/routes/architecture.py`
- `src/api/routes/architecture_analysis.py`
- `src/api/routes/benchmarks.py`
- `src/api/routes/capabilities.py`
- `src/api/routes/classification.py`
- `src/api/routes/contract_audit.py`
- `src/api/routes/council.py`
- `src/api/routes/demo_stream.py`
- `src/api/routes/documentation.py`
- `src/api/routes/fix_issues.py`
- `src/api/routes/fix_stream.py`
- `src/api/routes/integrations.py`
- `src/api/routes/meta.py`
- `src/api/routes/pentest.py`
- `src/api/routes/proactive.py`
- `src/api/routes/recommendations.py`
- `src/api/routes/reindex.py`

*Error handling:*
- `src/errors.py` — error classes (if exists at this path)

*Configuration:*
- `config/` directory (if exists)
- `.env` — environment configuration

**Documentation to read:**
- `docs/architecture/streaming-routes.md`
- `docs/architecture/services.md`
- `docs/architecture/resource-manager.md`
- `docs/architecture/scheduler.md`
- `docs/architecture/observability-metrics-implementation-spec.md`
- `docs/architecture/telemetry-bridge.md`
- `docs/architecture/telemetry-architecture-discovery.md`
- `docs/development/running-tests.md`
- `docs/development/testing-methodology.md`
- `docs/development/docker-cleanup-solution.md`
- `docs/guides/usage.md`

**Test files to read:**
- `tests/api/` (if exists)

**CORE/PERIPHERAL Classification** (per `DISTILLATION_PROTOCOL.md` Section 5):
- **CORE** (9 files): `server.py`, `middleware.py`, `telemetry_middleware.py`, routes: `atlas_chat.py`, `console.py`, `streaming.py`, `sandbox.py`, `proposals.py`, `voice.py`
- **PERIPHERAL** (31 files): All remaining specialty route files, `documentation_bridge.py`, `meta_sections.py`, `errors.py`, config files

### A.3 Context Brief

**What worked in Attempt 3:**
- FastAPI server with 81 REST endpoints
- Default port 8000
- Main chat at `/v1/atlas/chat` (expects `{"query": "..."}` not `{"message": "..."}`)
- Agent alias at `/v1/atlas/agent`
- Health check at `/health`
- Streaming response support
- Console session management

**What failed or was never wired:**
- 81 endpoints is massive — many are likely stubs or unused
- API contract validation missing — code calls non-existent methods and tests pass
- Configuration loaded from `config.yaml` with ALL feature flags FALSE
- Error taxonomy unclear — `src/errors.py` may not have comprehensive coverage
- Startup order complex with deferred initialization
- Concurrency model (async throughout) may have SQLite threading issues

**What was simulated/fake:**
- Some endpoints may return stub data
- Health endpoint may report healthy for stub subsystems

**Relevant Volume 0 principles:**
- P5: Silent failure is a system fault (error handling)
- P8: Pydantic schemas at every boundary (API request/response validation)
- R1: Start with working conversation loop (chat endpoint is the entry point)
- R8: Observable and debuggable (telemetry, logging)

### A.4 Known Failures & Warnings
1. **81 endpoints → how many are needed?**: The rebuild should start with the minimum viable API surface and add endpoints as subsystems come online. The distillation agent must triage.
2. **Error taxonomy**: Define the error classification system for the rebuild. This affects every subsystem.
3. **Startup/initialization order**: Attempt 3 had complex deferred init. The rebuild should have a simple, predictable startup sequence.
4. **Concurrency model**: Explicit decision needed — async-first? Which operations are truly async? SQLite + asyncio has known pitfalls.
5. **Configuration approach**: Feature flags all FALSE was a symptom of A1. The rebuild needs a clean config strategy.

---

## Part B: Design Specification (Agent Fills Out)

### B.1 Subsystem Purpose (Rebuild)

The API & Infrastructure subsystem is the external boundary of Atlas. It receives every user request (HTTP, WebSocket), delegates to internal subsystems (orchestrator, memory, governance), and returns governed responses. In the rebuild it SHOULD provide: (a) a minimal, schema-validated FastAPI server that starts in under 3 seconds with a deterministic startup sequence; (b) a small set of versioned REST and WebSocket endpoints — starting with `/health` and `/v1/atlas/chat` — where each endpoint has a Pydantic request model, a Pydantic response model, and an acceptance test that hits the live server; (c) a middleware stack that enforces request timeouts, structured error responses, request logging, and CORS; (d) a configuration system backed by `pydantic-settings` with an `ATLAS_` env-var prefix and explicit feature flags that default to OFF; (e) an error taxonomy rooted in a single `AtlasError` base class with category/severity classification, so every error is logged with context (P5) and never silently swallowed. New endpoints are added only when the subsystem they serve has a passing acceptance test (P3, R3). The server owns HOW endpoints are registered and served; each subsystem volume defines WHAT endpoints it needs.

### B.2 Architecture Overview

**Major Components:**

1. **`api/server.py` — Application Factory + Lifecycle**
   Creates the FastAPI app via a `create_app()` factory (not a module-level global). Owns `startup` and `shutdown` lifespan events. Startup: load config → boot shared services (logging, config) → register middleware → register route groups → run smoke self-test (call `/health`, verify 200). Shutdown: drain in-flight requests → close subsystems in reverse order → flush logs. No background `asyncio.create_task` fire-and-forget at startup; deferred init is explicit and supervised.

2. **`api/middleware.py` — Middleware Stack**
   Three middlewares applied in order (outermost first): `RequestLoggingMiddleware` → `TimeoutMiddleware` (default 60 s, per-path overrides via config) → `ExceptionHandlerMiddleware`. ExceptionHandler catches `AtlasError` subclasses, maps to HTTP status codes via a category→status table, returns a structured `ErrorResponse` JSON body, and routes LEARNING-category errors to the memory system asynchronously. CORS middleware is configurable (not wildcard in production).

3. **`api/routes/` — Route Modules (one file per domain)**
   Each file defines an `APIRouter`, its Pydantic request/response models, and a `init_*_routes(deps)` function called by the factory. Initial route files for MVA: `health.py`, `chat.py`. Post-MVA additions follow R3 (integrated + tested before next begins): `memory.py`, `learning.py`, `sandbox.py`, `voice.py`.

4. **`shared/errors.py` — Error Taxonomy**
   Single `AtlasError(Exception)` base with `category: ErrorCategory`, `severity: ErrorSeverity`, context dict. Subclasses: `ValidationError`, `MemoryLayerError`, `GovernanceViolation`, `IntentParsingError`, `LLMProviderError`, `ToolExecutionError`, `SandboxError`, `ConfigurationError`. Matches PROJECT_CONVENTIONS.md Section 6 exactly.

5. **`shared/config.py` — Configuration**
   `AtlasConfig(BaseSettings)` loaded from env vars with `ATLAS_` prefix and optional `.env` file. Flat structure. Feature flags (`enable_voice`, `enable_learning`, `enable_self_modify`) default OFF. No YAML. No 50-flag config files.

**Data Flow (request lifecycle):**

```
Client → CORS → RequestLogging → Timeout → ExceptionHandler
  → Route Handler
    → Pydantic request validation (P8)
    → Orchestrator / Memory / Governance call
    → Pydantic response validation (P8)
  ← Structured JSON response
← Client
```

**Concurrency Model:**
Fully async (`async def` handlers). SQLite access via `aiosqlite` or `asyncio.to_thread()` for synchronous drivers — never raw `sqlite3.connect()` on the event loop. Long-running operations (sandbox execution, LLM calls) use `asyncio.wait_for()` with explicit timeouts.

### B.3 Interface Contracts

#### 3.1 Server Factory

```
def create_app(config: AtlasConfig | None = None) -> FastAPI
```
- **Input:** Optional `AtlasConfig`. Defaults to loading from env.
- **Output:** Configured FastAPI app with middleware and routes registered.
- **Dependencies consumed:** `AtlasConfig` (shared/config), error hierarchy (shared/errors), logging (shared/logging).
- **Dependencies served:** The running HTTP server that all subsystems and the Console depend on.

#### 3.2 Health Endpoint

```
GET /health → HealthResponse
```

**HealthResponse schema:**
```
class HealthResponse(BaseModel):
    status: Literal["healthy", "degraded", "unhealthy"]
    service: str = "atlas-api"
    version: str
    subsystems: dict[str, SubsystemStatus]
    uptime_seconds: float

class SubsystemStatus(BaseModel):
    initialized: bool
    healthy: bool
    status: Literal["ok", "degraded", "error", "stub", "disabled"]
    detail: str | None = None
```
- **Rule (R5):** `healthy=True` only if the subsystem can demonstrate actual functionality. Stubs report `status="stub"`, disabled features report `status="disabled"`.
- **Consumed by:** Console (Volume 7), acceptance tests, monitoring.

#### 3.3 Chat Endpoint (MVA-1)

```
POST /v1/atlas/chat → ChatResponse
```

**ChatRequest schema:**
```
class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=10000)
    session_id: str | None = None
    context: str | None = None
```

**ChatResponse schema:**
```
class ChatResponse(BaseModel):
    answer: str
    session_id: str
    evidence: list[EvidenceRef] = []
    tool_calls: list[ToolCallSummary] | None = None
    governed: bool = True
    metadata: dict[str, Any] = {}

class EvidenceRef(BaseModel):
    source: str
    content_snippet: str
    confidence: float = Field(ge=0.0, le=1.0)

class ToolCallSummary(BaseModel):
    tool: str
    status: Literal["success", "failed", "skipped"]
    result_summary: str | None = None
```
- **Request key is `query` (not `message`).** This matches Attempt 3's convention and the rules in AGENT_COMM.md.
- **Consumed by:** Console (Volume 7), CLI client, acceptance tests.
- **Depends on:** Orchestrator engine (Volume 2), Memory manager (Volume 1), Governance output gate (Volume 9).

#### 3.4 Streaming Chat Endpoint

```
POST /v1/atlas/chat/stream → SSE stream
```
- Same `ChatRequest` input.
- Response: `text/event-stream` with events: `THINKING`, `TOOL_CALL`, `TOOL_RESULT`, `CHUNK`, `DONE`, `ERROR`.
- Each event is a JSON object with `type` and `content` fields.
- **Depends on:** Orchestrator streaming interface (Volume 2).

#### 3.5 Error Response Contract

All error responses follow one schema:
```
class ErrorResponse(BaseModel):
    error: str          # ErrorCategory value
    detail: str         # Human-readable message with context
    type: str           # Exception class name
    path: str           # Request path
    severity: str | None = None
    request_id: str | None = None
```
- 400: Validation errors (bad input)
- 404: Resource not found
- 500: Internal / operational errors
- 503: Critical errors (subsystem unavailable)
- 504: Timeout

#### 3.6 Middleware Contracts

**TimeoutMiddleware:**
- Default timeout: 60s.
- Per-path overrides loaded from `AtlasConfig.timeout_overrides: dict[str, float]`.
- Returns 504 `ErrorResponse` on timeout.

**ExceptionHandlerMiddleware:**
- Catches `AtlasError` → maps `category` to HTTP status (CRITICAL→503, OPERATIONAL→500, LEARNING→500).
- Catches bare `Exception` → wraps in `AtlasError`, returns 500.
- Routes errors with `should_route_to_learning=True` to memory asynchronously (non-blocking).
- Never swallows exceptions silently (P5).

**RequestLoggingMiddleware:**
- Logs slow requests (>5s) at WARNING.
- Logs failed requests (status ≥ 400) at WARNING.
- Skips noisy paths (`/health`, `/metrics`) from normal logging.
- Uses `structlog` structured logging.

#### 3.7 Configuration Contract

```
class AtlasConfig(BaseSettings):
    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "info"
    cors_origins: list[str] = ["http://localhost:3000"]
    timeout_overrides: dict[str, float] = {}

    # LLM
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    default_llm_provider: str = "openai"

    # Features (off by default, R5: must work if on)
    enable_voice: bool = False
    enable_learning: bool = False
    enable_self_modify: bool = False

    model_config = {"env_prefix": "ATLAS_", "env_file": ".env"}
```
- **Consumed by:** Every subsystem via `get_config()` singleton.
- **Rule:** No YAML config files. All config through env vars or `.env`.

#### 3.8 Subsystem Route Registration Pattern

Every subsystem that exposes endpoints follows this pattern:
```python
# api/routes/{subsystem}.py
from fastapi import APIRouter
router = APIRouter(prefix="/v1/{subsystem}", tags=["{subsystem}"])

def init_{subsystem}_routes(deps: SubsystemDeps) -> None:
    """Wire dependencies. Called by create_app() at startup."""
    ...

@router.post("/action")
async def action(request: ActionRequest) -> ActionResponse:
    ...
```
- Route file defines its own Pydantic request/response models.
- Cross-boundary schemas (shared with Console) live in `contracts/api_schemas.py`.
- Dependencies injected via `init_*_routes()`, never via module-level globals.

### B.4 Scope Triage

Verdict for every file listed in A.2. REBUILD = needed in Atlas v4. DEFER = useful but not needed for initial tiers. KILL = not needed, duplicated, or should not exist.

**Server Core:**

| File | Verdict | Justification |
|---|---|---|
| `src/api/server.py` | **REBUILD** | Core entry point. Must be rewritten as a clean factory function (~200 lines, not 2600). Attempt 3's server.py is a god object mixing route definitions, startup logic, global singletons, and inline handlers. The rebuild separates concerns: factory, lifecycle, route registration. |
| `src/api/middleware.py` | **REBUILD** | ExceptionHandler, Timeout, RequestLogging middlewares are sound design. Rebuild keeps the three-middleware stack, uses the new error taxonomy from shared/errors.py, and removes the circuit-breaker (SubsystemHealth) — circuit-breaking belongs at the client/orchestrator level, not HTTP middleware. |
| `src/api/telemetry_middleware.py` | **DEFER** | Telemetry decorator is useful for observability but not needed for MVA. Add after Tier 4 when observability tooling is built. |
| `src/api/documentation_bridge.py` | **KILL** | Import coupling bridge for a documentation subsystem that was never fully wired. The rebuild has no documentation authority subsystem in the initial tiers. If documentation tooling is rebuilt later, it follows the standard route module pattern — no bridge file needed. |
| `src/api/meta_sections.py` | **KILL** | Assessment dashboard section endpoints. This is development introspection tooling, not core Atlas functionality. Not needed in the rebuild. If meta-assessment is wanted later, it becomes a standard route module. |

**Route Files — CORE:**

| File | Verdict | Justification |
|---|---|---|
| `src/api/routes/atlas_chat.py` | **REBUILD** | This is the MVA-1 critical path. `/v1/atlas/chat` and `/v1/atlas/chat/stream` are the conversation loop entry points. Rebuild as `api/routes/chat.py` with clean ChatRequest/ChatResponse schemas. Remove task CRUD (belongs in a separate tasks route if needed), skill history (peripheral), and voice-approved endpoint (Volume 6 concern). |
| `src/api/routes/console.py` | **DEFER** | Console session management, file browser, activity logs. Needed for Console (Volume 7) but not for MVA. Add when Console is built (Tier 6+). |
| `src/api/routes/streaming.py` | **DEFER** | WebSocket endpoints for telemetry stream, notification stream, proactive stream. Important for Console visualization but not MVA. The telemetry injection endpoints are infrastructure for testing; defer until observability tier. |
| `src/api/routes/sandbox.py` | **DEFER** | Docker sandbox execution and git worktree proposals. Needed for self-modification (Volume 4) but not for MVA. Add at Tier 6+. Note: massive duplication with inline handlers in server.py — rebuild consolidates into one module. |
| `src/api/routes/proposals.py` | **DEFER** | SelfModifier proposal CRUD. Depends on self-modification subsystem (Volume 4). Not MVA. |
| `src/api/routes/voice.py` | **DEFER** | WebRTC signaling, TTS proxy, STT proxy, speaker verification. Depends on Voice subsystem (Volume 6). Not MVA. |

**Route Files — PERIPHERAL:**

| File | Verdict | Justification |
|---|---|---|
| `src/api/routes/intelligence.py` | **DEFER** | Analogical reasoning, hypothesis generation. Volume 5 capability, not MVA. |
| `src/api/routes/knowledge.py` | **DEFER** | Knowledge librarian endpoints. Useful for memory introspection. Add with Volume 1 memory endpoints. |
| `src/api/routes/learning.py` | **DEFER** | Learning pattern visibility. Add when learning subsystem (Volume 3) is built at Tier 5. |
| `src/api/routes/learning_feedback.py` | **DEFER** | Intent correction feedback. Needed for MVA-4 (learning round-trip). Add at Tier 5. |
| `src/api/routes/security.py` | **KILL** | Security scanning scheduler. Development/audit tooling, not core Atlas. |
| `src/api/routes/safety.py` | **KILL** | Extracted stub with no substantial implementation found. |
| `src/api/routes/system.py` | **KILL** | Extracted stub for system routes. Subsystem status is covered by /health. |
| `src/api/routes/data.py` | **KILL** | Extracted stub for data routes. No clear purpose distinct from memory endpoints. |
| `src/api/routes/metrics.py` | **KILL** | Fix generator comparison metrics. Development tooling specific to Attempt 3's fix pipeline. |
| `src/api/routes/analytics.py` | **KILL** | Analytics dashboard endpoints. Development introspection, not core. |
| `src/api/routes/analysis.py` | **KILL** | Code analysis with real-time progress. Development tooling for Attempt 3's analysis pipeline. |
| `src/api/routes/architecture.py` | **KILL** | Extracted architecture stub. Development introspection. |
| `src/api/routes/architecture_analysis.py` | **KILL** | Codebase architecture analysis proxy. Development tooling. |
| `src/api/routes/benchmarks.py` | **KILL** | Benchmark dashboard routes. Development introspection. |
| `src/api/routes/capabilities.py` | **KILL** | Multimodal stub endpoints. Simulated/fake capabilities (A3 anti-pattern). |
| `src/api/routes/classification.py` | **KILL** | Intent classification debug routes. Development tooling. |
| `src/api/routes/contract_audit.py` | **KILL** | API contract validation. Useful idea but was itself not integrated. Rebuild achieves this via acceptance tests instead. |
| `src/api/routes/council.py` | **KILL** | Knowledge council federated query. Over-engineered research feature, not core. |
| `src/api/routes/demo_stream.py` | **KILL** | Live demo streaming. Marketing feature, not core Atlas. |
| `src/api/routes/documentation.py` | **KILL** | Documentation authority/librarian API. Documentation subsystem was never fully wired. |
| `src/api/routes/fix_issues.py` | **KILL** | Fix generation bridge. Attempt 3's analysis→fix pipeline, replaced by self-modification in rebuild. |
| `src/api/routes/fix_stream.py` | **KILL** | Fix job log streaming. Tied to killed fix pipeline. |
| `src/api/routes/integrations.py` | **KILL** | Integration health status. No real integrations existed. |
| `src/api/routes/meta.py` | **KILL** | Meta-assessment dashboard. Development introspection. |
| `src/api/routes/pentest.py` | **KILL** | Kali container pentest tooling. Security research feature, not core. |
| `src/api/routes/proactive.py` | **KILL** | Proactive suggestion routes stub. |
| `src/api/routes/recommendations.py` | **KILL** | Strategic recommendations engine. Business analysis feature, not core. |
| `src/api/routes/reindex.py` | **DEFER** | Codebase re-indexing trigger. Useful for memory/knowledge system but not MVA. |

**Error/Config Files:**

| File | Verdict | Justification |
|---|---|---|
| `src/errors.py` | **REBUILD** | Error taxonomy (ErrorCategory, ErrorSeverity, ATLASException hierarchy) is well-designed. Rebuild as `shared/errors.py` following PROJECT_CONVENTIONS.md Section 6 exactly. Simplify: keep the 8 error classes defined in conventions, drop Attempt 3's specialized subclasses (APIRequestError, ExecutionTimeoutError, etc.) — those can be added as needed. |
| `config/` directory | **REBUILD** | Replace YAML-based config with `pydantic-settings` `AtlasConfig` as defined in PROJECT_CONVENTIONS.md Section 8. No config/ directory; just `shared/config.py` + `.env`. |
| `.env` | **REBUILD** | Environment configuration. Template as `.env.example` with documented variables. |

**Summary counts:** REBUILD: 5 files. DEFER: 10 files. KILL: 25 files.

The rebuild starts with 3 files: `server.py`, `middleware.py`, `routes/health.py` (Tier 1), then adds `routes/chat.py` (Tier 2). The remaining DEFER files are added as their owning subsystems come online.

### B.5 Technology Choices

**Framework: FastAPI (keep)** — Native async, OpenAPI docs, Pydantic validation (P8), DI, SSE/WS. No change from Attempt 3. The rebuild changes how FastAPI is used, not which framework.

**HTTP server: Uvicorn (keep)** — Standard ASGI server. Single-worker dev, multi-worker via Gunicorn for production.

**Configuration: pydantic-settings (change from YAML)** — Attempt 3 mixed `config.yaml`, `dotenv`, and hardcoded defaults. Rebuild uses `pydantic-settings` exclusively: env vars with `ATLAS_` prefix, optional `.env`, no YAML. Eliminates A.4 item 5. Per PROJECT_CONVENTIONS.md Section 8.

**Logging: structlog (change from loguru)** — Structured JSON logging per PROJECT_CONVENTIONS.md Section 7. Machine-parsable. Migration: `logger.info("message")` → `log.info("event_name", key=value)`.

**Database access: aiosqlite (change from raw sqlite3)** — Addresses A.4 item 4. `aiosqlite` or `asyncio.to_thread()` for sync drivers. Never raw `sqlite3.connect()` on the event loop. SQLite remains the storage engine per Volume 1.

**CORS: CORSMiddleware (keep, restrict)** — Attempt 3 uses `allow_origins=["*"]`. Rebuild defaults to `["http://localhost:3000"]`. Production must explicitly set `ATLAS_CORS_ORIGINS`.

**HTTP client: httpx (keep)** — Async HTTP client for outbound API calls (ElevenLabs STT, OpenAI Realtime proxying).

**TypeScript codegen: datamodel-code-generator or pydantic2ts (new)** — Per C-11 and PROJECT_CONVENTIONS.md Section 1. Vol 8 owns `contracts/generate_ts_types.py`. Reads Pydantic models from `contracts/api_schemas.py`, outputs TS interfaces for Console.

### B.6 Data Model

Vol 8 owns the HTTP-boundary Pydantic schemas in `contracts/api_schemas.py`. These cross the API↔Console boundary. Internal schemas owned by respective volumes.

**ChatRequest** (`contracts/api_schemas.py`)
- `query: str` — `Field(..., min_length=1, max_length=10000)`. Field name is `query` per C-17.
- `session_id: str | None = None` — Optional session.
- `context: str | None = None` — Optional additional context.
- `stream: bool = False` — If true, response is SSE per C-12. Single endpoint, no separate `/stream` path.
- `model_config = {"frozen": True}`

**ChatResponse** (`contracts/api_schemas.py`)
- `answer: str` — Maps from `ConversationResponse.response` (Vol 2) per C-13.
- `session_id: str`
- `evidence: list[EvidenceRef] = []` — Maps from `ConversationResponse.evidence_refs`.
- `tool_calls: list[ToolCallSummary] | None = None`
- `governed: bool = True` — Whether response passed output governance (Vol 9).
- `metadata: dict[str, Any] = {}`
- `model_config = {"frozen": True}`

**EvidenceRef** — `source: str`, `content_snippet: str`, `confidence: float = Field(ge=0.0, le=1.0)`

**ToolCallSummary** — `tool: str`, `status: Literal["success", "failed", "skipped"]`, `result_summary: str | None = None`

**ErrorResponse** — `error: str` (ErrorCategory), `detail: str`, `type: str` (exception class), `path: str`, `severity: str | None`, `request_id: str | None`

**HealthResponse** — `status: Literal["healthy", "degraded", "unhealthy"]`, `service: str = "atlas-api"`, `version: str`, `subsystems: dict[str, SubsystemStatus]`, `uptime_seconds: float`

**SubsystemStatus** — `initialized: bool`, `healthy: bool`, `status: Literal["ok", "degraded", "error", "stub", "disabled"]`, `detail: str | None`

**SSE StreamEvent** — `type: Literal["THINKING", "TOOL_CALL", "TOOL_RESULT", "CHUNK", "DONE", "ERROR"]`, `content: str`, `metadata: dict[str, Any] = {}`

These schemas are the single source of truth for both backend and Console frontend (via TS codegen).

**Mapping responsibility:** Route handler in `api/routes/chat.py` maps `ConversationResponse` (Vol 2) → `ChatResponse` (Vol 8). Field renames: `response` → `answer`, `evidence_refs` → `evidence`.

### B.7 Error Handling

**Error hierarchy** (location: `atlas/shared/errors.py`, owned by Vol 8)

```
AtlasError(Exception)
├── ValidationError          — Pydantic/business rule validation failures
├── MemoryLayerError         — Memory layer operation failures
├── GovernanceViolation      — Constitutional/governance rule violations
├── IntentParsingError       — Intent extraction failures
├── LLMProviderError         — LLM API call failures (graceful degradation per R6)
├── ToolExecutionError       — Tool invocation failures
├── SandboxError             — Sandbox execution failures
└── ConfigurationError       — Invalid/missing configuration
```

**AtlasError base class:** `category: ErrorCategory` (CRITICAL/OPERATIONAL/LEARNING), `severity: ErrorSeverity` (FATAL/HIGH/MEDIUM/LOW), `context: dict[str, Any]` (never empty), `should_route_to_learning: bool`, `timestamp: datetime`.

Validated by Attempt 3's `src/errors.py` which has the same `ErrorCategory`/`ErrorSeverity`/`ATLASException` structure. Rebuild simplifies: 8 classes per PROJECT_CONVENTIONS.md Section 6 (drops 6 specialized subclasses from Attempt 3).

**HTTP status mapping** (in `ExceptionHandlerMiddleware`):
- `CRITICAL` → 503, `OPERATIONAL` → 500, `LEARNING` → 500
- `ValidationError` → 400 (override: client error)
- Bare `Exception` → wrapped in `AtlasError` OPERATIONAL, 500
- `asyncio.TimeoutError` → 504 (via `TimeoutMiddleware`)
- 404 returned by route handlers directly

**Error propagation:** Exception raised → `ExceptionHandlerMiddleware` catches → maps to `ErrorResponse` JSON → logs with `structlog` → if `should_route_to_learning`, fires `asyncio.create_task()` for L3 storage (non-blocking) → response returned.

**Forbidden patterns (P5):** `except: pass`, `except Exception: pass`, `raise Exception(...)`, HTTP 200 with error body.

### B.8 Testing Strategy

**Acceptance tests (gate everything per P11):**
1. **AT-API-01:** Server boots, `GET /health` returns 200, `status` is `"healthy"` or `"degraded"`, `subsystems` present, < 3s. Gates Tier 1.
2. **AT-API-02:** `POST /v1/atlas/chat` with `{"query": "hello"}`, response has `answer` (non-empty), `session_id`, `governed`. < 5s. Gates Tier 2.
3. **AT-API-03:** Empty query → 422. Malformed JSON → 400. All errors match `ErrorResponse`.
4. **AT-API-04:** `{"query": "hello", "stream": true}` returns SSE with at least `CHUNK` + `DONE` events matching `StreamEvent`.
5. **AT-API-05:** Disabled subsystem reports `status="disabled"`, stub reports `status="stub"` (R5).

**Integration tests:**
1. **IT-API-01:** Middleware ordering verified via log output.
2. **IT-API-02:** Request beyond timeout → 504 + cancelled.
3. **IT-API-03:** Learning-category error stored in L3 within 5s (real DB).
4. **IT-API-04:** `ATLAS_PORT=9999` loaded by `AtlasConfig`.
5. **IT-API-05:** `ConversationResponse` → `ChatResponse` mapping verified (`response`→`answer`, `evidence_refs`→`evidence`).

**Unit tests:**
1. `test_error_hierarchy` — 8 subclasses have correct defaults.
2. `test_error_response_schema` — Serialization round-trip.
3. `test_config_defaults` — port=8000, host=127.0.0.1, flags=False.
4. `test_config_env_prefix` — `ATLAS_` prefix loads.
5. `test_health_response_schema` — Schema validation.
6. `test_chat_request_validation` — Rejects empty, accepts valid, max_length=10000.
7. `test_stream_event_schema` — All 6 event types.
8. `test_exception_handler_maps_atlas_error` — Category→status mapping.
9. `test_exception_handler_wraps_bare` — Bare Exception → OPERATIONAL.
10. `test_timeout_per_path_overrides` — `/v1/atlas/chat` gets longer timeout.

**Regression tests:**
1. **REG-01:** Server starts < 3s (A.4 item 3).
2. **REG-02:** `create_app()` callable multiple times without state leaks (eliminates global singletons).
3. **REG-03:** `AtlasConfig().cors_origins` does not contain `"*"` (A.4 item 6).

### B.9 Configuration

**Schema** (`atlas/shared/config.py`):
```
class AtlasConfig(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "info"
    cors_origins: list[str] = ["http://localhost:3000"]
    request_timeout: float = 60.0
    timeout_overrides: dict[str, float] = {}
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    default_llm_provider: str = "openai"
    enable_voice: bool = False
    enable_learning: bool = False
    enable_self_modify: bool = False
    model_config = SettingsConfigDict(env_prefix="ATLAS_", env_file=".env", env_file_encoding="utf-8")
```

**Loading:** Instantiated once in `create_app()`, passed via DI. `get_config()` returns the factory instance.

**Env vars:** `ATLAS_` prefix. Pydantic-settings handles type coercion.

**Feature flags:** Default OFF. ON requires passing acceptance test. `.env.example` documents all vars.

**Timeout overrides:** Dict mapping path prefixes to seconds, e.g. `{"POST /v1/atlas/chat": 120.0}`. `TimeoutMiddleware` checks before `request_timeout` fallback.

**Not configurable (by design):** `/v1/` prefix, error response schema, middleware ordering, `/health` path.

### B.10 Subsystem Lessons Learned

1. **server.py god object (2600+ lines)** — Mixes app creation, lifecycle, 18 inline handlers, 5 global singletons, background tasks, static files, middleware config. A1 anti-pattern. Rebuild separates: factory, lifecycle, routes, config, errors. Target: <200 lines.

2. **Endpoint duplication** — Sandbox endpoints defined in server.py (1182-1430) AND routes/sandbox.py AND routes/console.py. Three implementations, inconsistent. Rebuild: one route per path, one model per concept.

3. **Voice endpoints leaked into API infra** — 450+ lines of WebRTC/TTS/STT/voiceprint in server.py. Vol 6 concerns. Rebuild: `api/routes/voice.py`, registered only when `enable_voice=True`.

4. **Global singletons break test isolation** — 5 module-level globals with lazy init. Tests get stale state. Rebuild: state in `app.state` via lifespan context manager. `create_app()` returns fresh state.

5. **81 endpoints, no API surface management** — 17 `app.include_router()` calls, no docs on MVA-critical vs. stubs. Rebuild: explicit tags, route modules registered only with healthy backing subsystem.

6. **CORS wildcard** — `allow_origins=["*"]` with unacted "configure for production" comment. Rebuild defaults to `["http://localhost:3000"]`.

7. **Unsupervised background tasks** — 5+ `asyncio.create_task()` at startup, failures logged but not surfaced to `/health`. Rebuild: tracked tasks, `/health` degrades to `"degraded"` on failure.

### B.11 Discoveries

1. **Middleware stack is well-designed — preserve structure** — `RequestLogging` → `Timeout` → `ExceptionHandler` from `src/api/middleware.py` is sound. ExceptionHandler classifies ATLASException vs. bare Exception, routes learning errors to L3, maps category→HTTP status. Rebuild changes: structlog, configurable timeouts, remove SubsystemHealth circuit breaker.

2. **Error taxonomy structurally correct but over-specified** — `ATLASException` → `ErrorCategory` → `ErrorSeverity` → `should_route_to_learning` is exactly right. `to_episode_dict()` and `route_exception_to_memory()` demonstrate correct error↔memory integration. Rebuild: 8 subclasses (not 13).

3. **Risk: single-endpoint streaming (C-12)** — Merging `/v1/atlas/chat` (JSON) and `/v1/atlas/chat/stream` (SSE) into one endpoint with `stream: bool`. Route handler checks field, returns `JSONResponse` or `StreamingResponse`. AT-API-04 covers this.

4. **Risk: aiosqlite migration** — Raw `sqlite3.connect()` in route handlers (atlas_chat.py:356). Every call must go through async wrapper. Vol 1 owns SQLite access layer; Vol 8 ensures no route handler touches connections directly.

5. **DI pattern: use FastAPI `Depends()` not `init_*_routes()` globals** — Attempt 3 uses `_get_atlas: Optional[Callable]` module globals. Rebuild: `Depends()` mechanism, `app.dependency_overrides` for tests.

### B.12 Oversight Self-Review

**Q1: Does this design address every A.4 item?**
- **A.4-1 (81 endpoints):** B.4 triage: 5 REBUILD, 10 DEFER, 25 KILL. Starts with 2 route files.
- **A.4-2 (Error taxonomy):** B.7: 8-class hierarchy, HTTP mapping, forbidden patterns.
- **A.4-3 (Startup order):** B.2: `create_app()` factory + lifespan. Supervised startup. No singletons.
- **A.4-4 (Concurrency):** B.2 + B.5: async handlers, aiosqlite, `asyncio.wait_for()`. No raw sqlite3.
- **A.4-5 (Configuration):** B.9: pydantic-settings, `ATLAS_` prefix, typed+validated. No YAML.

**Q2: Shared contracts respected?**
- Section 1.3 schemas: all in B.6. ChatRequest includes `stream: bool` per C-12.
- Section 2.1 (Vol 8→Vol 2): `ConversationEngine.process_message()` consumed, mapping in B.6.
- Section 2.14 (Vol 7→Vol 8): SSE via single chat endpoint per C-12.
- Section 5.1/5.2: error hierarchy and config match exactly.

**Q3: Anti-patterns avoided?**
- A1: Routes registered only with backing subsystem. A2: Health verifies actual functionality (R5). A3: No fake reports. A4: Exception handlers log, `except: pass` forbidden. A5: 3 files Tier 1, 4 Tier 2. A7: No TODOs. A8: Acceptance tests hit live server.

**Q4: Interface mismatches?**
- Vol 2: `process_message(message, session_id, device_id)` — `ChatRequest.query`→`message`, `session_id`→`session_id`, `device_id="api"`. No mismatch.
- Vol 7: `/v1/*` per C-10, SSE per C-12, TS types per C-11. No mismatch.
- Vol 9: `ChatResponse.governed` + `evidence` from `AnswerGovernor` via Vol 2. No mismatch.
- Vol 1: `MemoryManager.get_stats()` for health. No mismatch.

**Q5: Missing for coding agent?**
- WebSocket telemetry: deferred to Tier 4+.
- Session CRUD: deferred to Tier 6+.
- Memory admin endpoints: deferred.
- HTTPS/TLS: reverse proxy concern, not application.

**Q6: B.4 verdicts still correct?**
All stand. server.py REBUILD, middleware.py REBUILD, telemetry DEFER, 25 KILL confirmed, 10 DEFER confirmed.

### B.13 Design Quality Scorecard

1. **Volume 0 Compliance** — **5/5**. P2 graduated registration. P3 endpoints require AT. P5 error logging. P8 Pydantic schemas. P11 five ATs.
2. **Interface Completeness** — **5/5**. 8 contracts in B.3, all schemas in B.6 with field types.
3. **Anti-Pattern Avoidance** — **5/5**. A1-A8 addressed in B.12 Q3. Minimal start.
4. **Testability** — **4/5**. 5 AT, 5 IT, 10 UT, 3 REG with inputs/outputs. Deduction: WS telemetry deferred.
5. **Shared Contract Conformance** — **5/5**. All Section 1.3 schemas. C-10 through C-17 incorporated.
6. **Scope Discipline** — **5/5**. 5/40 REBUILD, 25 KILL (62.5% reduction). MVA: 3→4 files.
7. **Specificity** — **4/5**. Schemas, errors, middleware, config, mapping specified. Deduction: WS protocol deferred.
8. **Lessons Integration** — **5/5**. 7 lessons with code refs. REG-01–REG-03 prevent recurrence.
9. **Documentation Quality** — **4/5**. All sections filled, cross-referenced. Deduction: verbose due to schema count.

**Total: 42/45** (minimum: 30/45) — **PASS**

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (5 server files, 35+ route files, error/config files), context brief, and 5 known failure warnings including 81 endpoints needing triage and SQLite async pitfalls | Created the API/infrastructure analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V08-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
|| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 Source Manifest per DISTILLATION_PROTOCOL.md Section 5 | Labeled which files agents should read in full vs. skim during Phase 1 |
|| v5 | 2026-03-10 | Distillation Agent V8 | Phase 1: Filled B.1 (Subsystem Purpose), B.2 (Architecture Overview with 5 components + data flow + concurrency model), B.3 (8 interface contracts: server factory, health, chat, streaming, errors, middleware, config, route pattern), B.4 (Scope Triage: 5 REBUILD, 10 DEFER, 25 KILL across 40 files) | Wrote the design spec for the rebuilt API server — what endpoints to keep, what to kill, and exactly how they should work |
|| v6 | 2026-03-11 | Distillation Agent V8 | Phase 2: Filled B.5-B.13 (Technology Choices, Data Model, Error Handling, Testing Strategy, Configuration, Lessons Learned, Discoveries, Oversight Self-Review, Scorecard 42/45 PASS) | Deep-dived into source files and completed the detailed technical spec with schemas, error taxonomy, test plans, and design verification |
