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

**Framework: FastAPI (keep)**
FastAPI is the correct choice. It provides native async support, automatic OpenAPI docs, Pydantic request/response validation (P8), dependency injection, and SSE/WebSocket support. No departure from Attempt 3's framework choice. The rebuild changes how FastAPI is used, not which framework is used.

**HTTP server: Uvicorn (keep)**
Uvicorn is the standard ASGI server for FastAPI. Single-worker mode for development, multi-worker via `uvicorn --workers N` or Gunicorn for production. No change from Attempt 3.

**Configuration: pydantic-settings (change from YAML)**
Attempt 3 used a mix of `config.yaml`, `dotenv`, and hardcoded defaults scattered across `server.py`. The rebuild uses `pydantic-settings` exclusively — env vars with `ATLAS_` prefix, optional `.env` file, no YAML. This eliminates the 50-flag YAML config problem (A.4 item 5) and gives Pydantic validation on every config value. Per PROJECT_CONVENTIONS.md Section 8.

**Logging: structlog (change from loguru)**
Attempt 3 uses `loguru` throughout. The rebuild switches to `structlog` for structured JSON logging per PROJECT_CONVENTIONS.md Section 7. Structured logs enable machine-parsable observability, which loguru's string-based format does not provide cleanly. The migration is straightforward: replace `logger.info("message")` with `log.info("event_name", key=value)`.

**Database access: aiosqlite (change from raw sqlite3)**
Attempt 3 has known SQLite+asyncio pitfalls (A.4 item 4). The rebuild uses `aiosqlite` for all async SQLite access, or `asyncio.to_thread()` to wrap synchronous drivers. Never call raw `sqlite3.connect()` on the event loop. This is a concurrency model decision, not a database choice — SQLite remains the storage engine per Volume 1.

**CORS: fastapi CORSMiddleware (keep, but restrict)**
Attempt 3 uses `allow_origins=["*"]` — wildcard CORS in all modes. The rebuild defaults `cors_origins` to `["http://localhost:3000"]` (Console dev server). Production deployments must explicitly set `ATLAS_CORS_ORIGINS`. Wildcard is never the default.

**HTTP client: httpx (keep)**
Attempt 3 uses `httpx.AsyncClient` for proxied API calls (ElevenLabs STT, OpenAI Realtime). The rebuild keeps httpx as the async HTTP client for any outbound API calls needed by route handlers.

**TypeScript codegen: datamodel-code-generator or pydantic2ts (new)**
Per shared contract C-11 and PROJECT_CONVENTIONS.md Section 1, Volume 8 owns `contracts/generate_ts_types.py`. The tool reads Pydantic models from `contracts/api_schemas.py` and outputs TypeScript interfaces for Console consumption. The specific codegen library is a build-time dependency, not a runtime one — choose whichever produces the cleanest output at build time.

### B.6 Data Model

Volume 8 owns the HTTP-boundary Pydantic schemas that live in `contracts/api_schemas.py`. These are the schemas that cross the API↔Console boundary. Internal schemas (memory, governance, orchestrator) are owned by their respective volumes.

**Schemas owned by Volume 8:**

**ChatRequest** (location: `contracts/api_schemas.py`)
- `query: str` — `Field(..., min_length=1, max_length=10000)`. The user's input. Field name is `query` everywhere per resolved conflict C-17.
- `session_id: str | None = None` — Optional session for conversation continuity.
- `context: str | None = None` — Optional additional context.
- `stream: bool = False` — If true, response is SSE per resolved conflict C-12. Single endpoint with content negotiation, no separate `/stream` path.
- `model_config = {"frozen": True}`

**ChatResponse** (location: `contracts/api_schemas.py`)
- `answer: str` — The governed response text. Maps from `ConversationResponse.response` (Vol 2) in the route handler per conflict C-13.
- `session_id: str` — The conversation session ID.
- `evidence: list[EvidenceRef] = []` — Evidence sources grounding the response. Maps from `ConversationResponse.evidence_refs`.
- `tool_calls: list[ToolCallSummary] | None = None` — Summary of tools invoked.
- `governed: bool = True` — Whether the response passed output governance (Vol 9).
- `metadata: dict[str, Any] = {}` — Extensible metadata.
- `model_config = {"frozen": True}`

**EvidenceRef** (location: `contracts/api_schemas.py`)
- `source: str` — Evidence source identifier (tool name, memory layer, etc.).
- `content_snippet: str` — Verbatim excerpt from the source.
- `confidence: float` — `Field(ge=0.0, le=1.0)`. Confidence in the evidence.

**ToolCallSummary** (location: `contracts/api_schemas.py`)
- `tool: str` — Tool name.
- `status: Literal["success", "failed", "skipped"]` — Execution outcome.
- `result_summary: str | None = None` — Brief result description.

**ErrorResponse** (location: `contracts/api_schemas.py`)
- `error: str` — ErrorCategory value (critical, operational, learning).
- `detail: str` — Human-readable message with what happened, what was expected, what to do.
- `type: str` — Exception class name.
- `path: str` — Request path.
- `severity: str | None = None` — ErrorSeverity value if available.
- `request_id: str | None = None` — Request correlation ID for tracing.

**HealthResponse** (location: `contracts/api_schemas.py`)
- `status: Literal["healthy", "degraded", "unhealthy"]`
- `service: str = "atlas-api"`
- `version: str`
- `subsystems: dict[str, SubsystemStatus]`
- `uptime_seconds: float`

**SubsystemStatus** (location: `contracts/api_schemas.py`)
- `initialized: bool`
- `healthy: bool`
- `status: Literal["ok", "degraded", "error", "stub", "disabled"]`
- `detail: str | None = None`

**SSE StreamEvent** (location: `contracts/api_schemas.py`)
- `type: Literal["THINKING", "TOOL_CALL", "TOOL_RESULT", "CHUNK", "DONE", "ERROR"]`
- `content: str`
- `metadata: dict[str, Any] = {}`

These schemas serve as the single source of truth for both the Python backend and the Console frontend (via TypeScript codegen).

**Mapping responsibility:** The route handler in `api/routes/chat.py` maps `ConversationResponse` (Vol 2 internal schema) → `ChatResponse` (Vol 8 HTTP schema). Field renames: `response` → `answer`, `evidence_refs` → `evidence`. This mapping is Vol 8's concern.

### B.7 Error Handling

**Error hierarchy** (location: `atlas/shared/errors.py`, owned by Vol 8)

The rebuild error hierarchy follows PROJECT_CONVENTIONS.md Section 6 exactly:

```
AtlasError(Exception)
├── ValidationError          — Pydantic/business rule validation failures
├── MemoryLayerError         — Memory layer operation failures
├── GovernanceViolation      — Constitutional/governance rule violations (blocks execution)
├── IntentParsingError       — Intent extraction failures
├── LLMProviderError         — LLM API call failures (graceful degradation per R6)
├── ToolExecutionError       — Tool invocation failures
├── SandboxError             — Sandbox execution failures
└── ConfigurationError       — Invalid/missing configuration
```

**AtlasError base class design:**
- `category: ErrorCategory` — enum: `CRITICAL`, `OPERATIONAL`, `LEARNING`. Determines HTTP status mapping and routing behavior.
- `severity: ErrorSeverity` — enum: `FATAL`, `HIGH`, `MEDIUM`, `LOW`. Determines monitoring priority.
- `context: dict[str, Any]` — Structured context dict (what happened, what was expected). Never empty.
- `should_route_to_learning: bool` — If true, the error is asynchronously stored in L3 episodic memory via the ExceptionHandlerMiddleware.
- `timestamp: datetime` — When the error occurred.

This design is validated by Attempt 3's `src/errors.py`, which has the same `ErrorCategory`/`ErrorSeverity`/`ATLASException` structure and works well. The rebuild simplifies: drop the 6 specialized subclasses from Attempt 3 (`ConstitutionalViolation`, `DataCorruptionError`, `SafetyBoundaryViolation`, `TargetScopeViolation`, `APIRequestError`, `ArsenalLoadError`) — the 8 classes in PROJECT_CONVENTIONS.md Section 6 are sufficient. Specialized subclasses can be added later as specific failures demand (P2 graduated governance).

**HTTP status mapping** (in `ExceptionHandlerMiddleware`):
- `ErrorCategory.CRITICAL` → 503 Service Unavailable
- `ErrorCategory.OPERATIONAL` → 500 Internal Server Error
- `ErrorCategory.LEARNING` → 500 Internal Server Error
- `ValidationError` specifically → 400 Bad Request (override: validation is a client error)
- Bare `Exception` (not `AtlasError`) → wrapped in `AtlasError` with OPERATIONAL category, 500
- `asyncio.TimeoutError` → 504 Gateway Timeout (handled by `TimeoutMiddleware`)
- 404 returned by route handlers directly (resource not found is route logic, not middleware)

**Error propagation flow:**
1. Exception raised in route handler or subsystem call.
2. `ExceptionHandlerMiddleware` catches it.
3. Middleware maps to structured `ErrorResponse` JSON body.
4. Middleware logs error with `structlog` including full context.
5. If `should_route_to_learning=True`, middleware fires `asyncio.create_task()` to store error in L3 episodic memory (non-blocking — never delays the HTTP response).
6. Response returned to client.

**Forbidden patterns (P5 enforcement):**
- `except: pass` — forbidden. Every handler must log.
- `except Exception: pass` — forbidden. Must at minimum log.
- `raise Exception(...)` — forbidden. Must use `AtlasError` subclass.
- Returning HTTP 200 with `{"error": ...}` — forbidden. Error responses use proper HTTP status codes.

### B.8 Testing Strategy

**Acceptance tests (highest authority, gate everything per P11):**

1. **AT-API-01: Server boots and /health returns 200** — Start the server via `create_app()`, send `GET /health`, verify status code 200 and `status` field is `"healthy"` or `"degraded"` (not `"unhealthy"`). Verify `subsystems` dict is present. Verify response time < 3 seconds. This gates Tier 1.

2. **AT-API-02: Chat endpoint round-trip (MVA-1)** — Send `POST /v1/atlas/chat` with `{"query": "hello"}`, verify response contains `answer` (non-empty string), `session_id` (non-empty string), and `governed` (boolean). Verify response time < 5 seconds. This gates Tier 2.

3. **AT-API-03: Error response structure** — Send `POST /v1/atlas/chat` with `{"query": ""}` (empty string, fails min_length=1 validation). Verify 422 response with Pydantic validation error detail. Send malformed JSON. Verify 400 response. Verify all error responses match `ErrorResponse` schema.

4. **AT-API-04: Streaming chat** — Send `POST /v1/atlas/chat` with `{"query": "hello", "stream": true}` and `Accept: text/event-stream`. Verify response is SSE format. Verify at least one `CHUNK` event and one `DONE` event. Verify each event matches `StreamEvent` schema.

5. **AT-API-05: Health reports honest status** — If a subsystem is disabled (e.g., `enable_voice=False`), verify `/health` reports `status="disabled"` for that subsystem, not `status="ok"`. If a subsystem stub is present, verify `status="stub"`. This tests R5 (honest health reporting).

**Integration tests (real components, no boundary mocks):**

1. **IT-API-01: Middleware stack ordering** — Verify `RequestLoggingMiddleware` → `TimeoutMiddleware` → `ExceptionHandlerMiddleware` ordering by sending a request that triggers each middleware and checking log output order.

2. **IT-API-02: Timeout enforcement** — Send a request to an endpoint that sleeps beyond the configured timeout. Verify 504 response with `ErrorResponse` schema. Verify the request is cancelled (not left running).

3. **IT-API-03: Error routing to memory** — Trigger an error with `should_route_to_learning=True`. Verify the error appears in L3 episodic memory within 5 seconds. Uses a real (test) database, not a mock.

4. **IT-API-04: Configuration loading** — Set `ATLAS_PORT=9999` and `ATLAS_LOG_LEVEL=debug` as env vars. Verify `AtlasConfig` loads these values. Verify unknown env vars are ignored.

5. **IT-API-05: ConversationResponse → ChatResponse mapping** — Create a mock `ConversationResponse` from Vol 2 with known values. Pass through the chat route handler mapping. Verify `ChatResponse` fields are correctly mapped (`response` → `answer`, `evidence_refs` → `evidence`).

**Unit tests (isolated, mocks allowed):**

1. `test_error_hierarchy` — Verify all 8 `AtlasError` subclasses have correct `category`, `severity`, and `should_route_to_learning` defaults.
2. `test_error_response_schema` — Verify `ErrorResponse` schema serializes and deserializes correctly.
3. `test_config_defaults` — Verify `AtlasConfig` defaults: port=8000, host="127.0.0.1", all feature flags=False.
4. `test_config_env_prefix` — Verify env vars with `ATLAS_` prefix are loaded.
5. `test_health_response_schema` — Verify `HealthResponse` and `SubsystemStatus` schemas.
6. `test_chat_request_validation` — Verify `ChatRequest` rejects empty query, accepts valid query, and enforces `max_length=10000`.
7. `test_stream_event_schema` — Verify `StreamEvent` schema with all 6 event types.
8. `test_exception_handler_middleware_maps_atlas_error` — Verify `AtlasError` subclasses are mapped to correct HTTP status codes.
9. `test_exception_handler_middleware_wraps_bare_exception` — Verify bare `Exception` is wrapped in `AtlasError` with OPERATIONAL category.
10. `test_timeout_middleware_per_path_overrides` — Verify `/v1/atlas/chat` gets longer timeout than default.

**Regression tests from A.4 failures:**

1. **REG-01: Server startup time** — Verify server starts in under 3 seconds. Attempt 3's server.py had complex deferred init that made startup unpredictable (A.4 item 3).
2. **REG-02: No stale global singletons** — Verify `create_app()` can be called multiple times (e.g., in tests) without state leaking between instances. Attempt 3 used module-level globals (`_atlas_instance`, `_git_sandbox_instance`, etc.) that caused test isolation problems.
3. **REG-03: CORS not wildcard by default** — Verify `AtlasConfig().cors_origins` does not contain `"*"`. Attempt 3 had `allow_origins=["*"]` hardcoded.

### B.9 Configuration

**Configuration schema** (`atlas/shared/config.py`):

```
class AtlasConfig(BaseSettings):
    # Server
    host: str = "127.0.0.1"              # Bind address
    port: int = 8000                     # Listen port
    log_level: str = "info"              # structlog level
    cors_origins: list[str] = ["http://localhost:3000"]  # CORS allowed origins
    request_timeout: float = 60.0        # Default request timeout (seconds)
    timeout_overrides: dict[str, float] = {}  # Per-path timeout overrides

    # LLM
    openai_api_key: str = ""             # OpenAI API key (empty = disabled)
    anthropic_api_key: str = ""          # Anthropic API key (empty = disabled)
    default_llm_provider: str = "openai" # Default LLM provider

    # Features (off by default, each must have acceptance test when on)
    enable_voice: bool = False
    enable_learning: bool = False
    enable_self_modify: bool = False

    model_config = SettingsConfigDict(
        env_prefix="ATLAS_",
        env_file=".env",
        env_file_encoding="utf-8",
    )
```

**Loading mechanism:** `AtlasConfig()` is instantiated once in `create_app()` and passed to subsystems via dependency injection (not module-level globals). A `get_config()` function returns the current config for convenience but does not create a new instance — it returns the one created by the factory.

**Environment variables:** All prefixed with `ATLAS_`. Examples: `ATLAS_PORT=9000`, `ATLAS_LOG_LEVEL=debug`, `ATLAS_ENABLE_VOICE=true`, `ATLAS_OPENAI_API_KEY=sk-...`. Pydantic-settings handles type coercion (string "true" → bool True).

**`.env.example` template:** Ships with the repo, documents every variable with its default and purpose. Not gitignored. The actual `.env` file is gitignored.

**Feature flags:** Default OFF. Unlike Attempt 3 where ALL flags were FALSE and nothing was ever turned on, the rebuild requires: if a flag is turned ON, the corresponding subsystem must have a passing acceptance test. Feature flags without acceptance tests cannot be set to True in production.

**Timeout overrides:** `timeout_overrides` is a dict mapping path prefixes to timeout seconds. Example: `{"POST /v1/atlas/chat": 120.0, "POST /v1/sandbox/execute": 300.0}`. The `TimeoutMiddleware` checks this dict before falling back to `request_timeout`. In Attempt 3, these were hardcoded in the middleware class — the rebuild makes them configurable.

**What is NOT configurable (hardcoded by design):**
- API version prefix (`/v1/`) — changing would break all clients.
- Error response schema — must be consistent.
- Middleware ordering — `RequestLogging` → `Timeout` → `ExceptionHandler` is fixed.
- Health endpoint path (`/health`) — convention.

### B.10 Subsystem Lessons Learned

1. **server.py as a god object (2600+ lines)**
   Attempt 3's `server.py` mixes: app creation, startup/shutdown lifecycle, route registration, 18 inline route handlers (sandbox, voice, speaker verification, STT proxy, health, database, system resources, config reload, metrics), Pydantic model definitions for those inline routes, global singleton management (`_atlas_instance`, `_git_sandbox_instance`, `_debug_sandbox_manager`, `_db_health_monitor`, `_doc_sync_manager`), background task scheduling (`asyncio.create_task` for 5+ background tasks), static file mounting, and middleware configuration. This is the definition of A1 (Feature Factory). The rebuild separates: factory (`create_app`), lifecycle (lifespan context manager), routes (one file per domain in `api/routes/`), config (`shared/config.py`), errors (`shared/errors.py`). Target: `server.py` under 200 lines.

2. **Massive endpoint duplication**
   Sandbox execution endpoints are defined both inline in `server.py` (lines 1182-1430) AND in `routes/sandbox.py`. The same `SandboxExecuteRequest`, `SandboxFileModel`, `ProposeChangesRequest` Pydantic models are duplicated in both files with identical definitions. The `routes/console.py` file also duplicates a `POST /api/sandbox/execute` handler. Three implementations of the same endpoint with inconsistent behavior. The rebuild: one canonical route per path, one Pydantic model per concept, no duplication.

3. **Voice endpoints mixed into API infrastructure**
   Attempt 3's `server.py` contains 450+ lines of voice endpoints (WebRTC signaling, TTS synthesis, speaker verification, voiceprint CRUD, STT proxy). These are Volume 6 concerns that leaked into server.py because there was no route extraction discipline. The rebuild defers all voice routes to `api/routes/voice.py` and only registers them when `enable_voice=True`.

4. **Global state singletons cause test isolation failures**
   Five module-level global variables (`_atlas_instance`, `_git_sandbox_instance`, `_debug_sandbox_manager`, `_db_health_monitor`, `_doc_sync_manager`) with lazy initialization. Tests that call `create_atlas_instance()` get the singleton from a previous test. The rebuild eliminates module-level singletons: all state lives inside the FastAPI `app.state` attribute, managed by the lifespan context manager. `create_app()` returns a fresh app with fresh state.

5. **81 endpoints with no API surface management**
   Attempt 3 registered routers without discipline: `app.include_router(...)` 17 times in server.py, each importing a router from a route module. No documentation of which endpoints are MVA-critical vs. debug tooling vs. stubs. The rebuild uses explicit route groups with tags, and only registers route modules whose backing subsystem has been initialized and health-checked.

6. **CORS wildcard in all environments**
   `allow_origins=["*"]` with a comment "Configure appropriately for production" that was never acted on. The rebuild defaults to `["http://localhost:3000"]` and requires explicit override for broader access.

7. **Background tasks with no supervision**
   Attempt 3 fires 5+ `asyncio.create_task()` calls during startup with no supervision — if a background task fails, the error is logged but never surfaced to health checks. The rebuild: background tasks are tracked, and `/health` degrades to `"degraded"` if a critical background task has failed.

### B.11 Discoveries

1. **Attempt 3's middleware stack is well-designed and should be preserved in structure**
   The three-middleware pattern (`RequestLogging` → `Timeout` → `ExceptionHandler`) from `src/api/middleware.py` is sound. The `ExceptionHandlerMiddleware` correctly distinguishes `ATLASException` (classified) from bare `Exception` (wrapped), routes learning-category errors to L3 memory, and maps categories to HTTP status codes. The `TimeoutMiddleware` has per-path overrides. The `RequestLoggingMiddleware` correctly skips noisy health/metrics paths. These patterns should be preserved. The rebuild changes: (a) use `structlog` instead of `loguru`, (b) make timeout overrides configurable via `AtlasConfig` instead of hardcoded, (c) remove `SubsystemHealth` circuit breaker from middleware (circuit-breaking belongs at the orchestrator/client level, not HTTP middleware).

2. **Attempt 3's error taxonomy in `src/errors.py` is over-specified but structurally correct**
   The `ATLASException` → `ErrorCategory` → `ErrorSeverity` → `should_route_to_learning` pattern is exactly right. The `to_episode_dict()` method for L3 storage and `route_exception_to_memory()` function demonstrate the correct integration between errors and the memory system. The rebuild simplifies (8 subclasses per conventions vs. 13 in Attempt 3) but preserves the architecture.

3. **Risk: Single-endpoint streaming (C-12 resolution) requires careful SSE content negotiation**
   The conflict resolution mandates a single `POST /v1/atlas/chat` endpoint with a `stream: bool` field in the request body (not a separate `/stream` path). Attempt 3 had both `/v1/atlas/chat` (returns JSON) and `/v1/atlas/chat/stream` (returns SSE). Merging these into one endpoint requires the route handler to check `request.stream` and return either `JSONResponse` or `StreamingResponse`. This is straightforward but must be tested explicitly — the acceptance test AT-API-04 covers this.

4. **Risk: aiosqlite migration may surface hidden synchronous SQLite calls**
   Attempt 3 uses raw `sqlite3.connect()` in some memory layers and `cursor.execute()` directly in route handlers (e.g., `atlas_chat.py` line 356: `atlas.memory.l8.conn.cursor()`). The rebuild's aiosqlite mandate means every such call must go through an async wrapper. Volume 1 (Memory) owns the SQLite access layer, but Volume 8 must ensure no route handler ever touches a SQLite connection directly.

5. **Pattern: Dependency injection via `init_*_routes()` is correct but should use FastAPI's `Depends()`**
   Attempt 3 uses module-level `_get_atlas: Optional[Callable] = None` globals with `init_*_routes()` functions to wire dependencies. This works but makes testing harder (must call init before testing). The rebuild should use FastAPI's native `Depends()` mechanism: define a `get_engine()` dependency that returns the `ConversationEngine`, inject it into route functions. This is standard FastAPI practice and enables clean test overrides via `app.dependency_overrides`.

### B.12 Oversight Self-Review

**Question 1: Does this design address every item in A.4 (Known Failures & Warnings)?**

- **A.4-1 (81 endpoints → how many are needed?):** Addressed in B.4 Scope Triage. 5 REBUILD, 10 DEFER, 25 KILL. The rebuild starts with 2 route files (health, chat) at Tier 1-2, adds routes only as backing subsystems come online. The triage is complete and justified per file.
- **A.4-2 (Error taxonomy):** Addressed in B.7. The 8-class hierarchy from PROJECT_CONVENTIONS.md Section 6 is specified with category/severity/routing behavior. HTTP status mapping defined. Forbidden patterns enumerated.
- **A.4-3 (Startup/initialization order):** Addressed in B.2 and B.10 lesson 7. The rebuild uses a `create_app()` factory with a lifespan context manager. Startup order: load config → boot logging → register middleware → register routes → run smoke self-test. No fire-and-forget background tasks — all supervised. Module-level singletons eliminated.
- **A.4-4 (Concurrency model):** Addressed in B.2 (concurrency model section) and B.5 (aiosqlite choice). Fully async handlers. SQLite access via `aiosqlite` or `asyncio.to_thread()`. Long-running ops use `asyncio.wait_for()` with explicit timeouts. No raw `sqlite3.connect()` on the event loop.
- **A.4-5 (Configuration approach):** Addressed in B.9. `pydantic-settings` with `ATLAS_` prefix, `.env` file, typed+validated. Feature flags default OFF with acceptance test requirement for ON. No YAML config. No 50-flag config files.

**Question 2: Are all shared contracts from `gate-output/shared-contracts.md` respected?**

- **Section 1.3 (API Contract Schemas):** `ChatRequest`, `ChatResponse`, `EvidenceRef`, `ToolCallSummary`, `ErrorResponse`, `HealthResponse` — all specified in B.6 with exact field types matching the contract. `ChatRequest` now includes `stream: bool = False` per C-12 resolution.
- **Section 2.1 (Vol 8 → Vol 2):** `ConversationEngine.process_message()` — consumed by chat route handler. Mapping from `ConversationResponse` → `ChatResponse` specified in B.6.
- **Section 2.14 (Vol 7 → Vol 8):** All Console-consumed endpoints are covered. SSE streaming via single `POST /v1/atlas/chat` with `stream: true` per C-12 resolution.
- **Section 5.1 (Error Hierarchy):** Matches `shared/errors.py` specification exactly.
- **Section 5.2 (Configuration):** Matches `shared/config.py` specification exactly.

**Question 3: Does the design avoid all anti-patterns from Volume 0 Section 5?**

- **A1 (Feature Factory):** Route modules only registered when backing subsystem is initialized. No endpoint added without acceptance test.
- **A2 (Validation Theater):** Health endpoint verifies actual functionality (R5). Feature stubs report `status="stub"`, disabled features report `status="disabled"`.
- **A3 (Simulated Capabilities):** No fake health reports. No stub endpoints that return success.
- **A4 (Exception Swallowing):** Every exception handler logs with context. `except: pass` forbidden. Enforced by middleware design.
- **A5 (Scope Explosion):** Target: 3 files at Tier 1 (server, middleware, health route), 4 at Tier 2 (add chat route). Line budget for server.py: 200 lines.
- **A7 (TODO in Production):** No TODOs. Stub endpoints raise `NotImplementedError` or are not registered.
- **A8 (Tests That Don't Prove Functionality):** Acceptance tests hit the live server. Unit test count is irrelevant. AT-API-02 (MVA-1) sends real HTTP request and verifies real response.

**Question 4: Are there interface mismatches with adjacent volumes?**

- **Vol 2 (Orchestrator):** `ConversationEngine.process_message(message, session_id, device_id) -> ConversationResponse`. Vol 8 maps `ChatRequest.query` → `message`, `ChatRequest.session_id` → `session_id`, hardcodes `device_id="api"`. Return mapped per C-13. No mismatch.
- **Vol 7 (Console):** Console expects `/v1/*` endpoints per C-10 resolution. SSE via single chat endpoint per C-12. TypeScript types generated from Pydantic per C-11. No mismatch.
- **Vol 9 (Governance):** `GovernedOutput` consumed via `ChatResponse.governed` field and `evidence` list. Evidence comes from Vol 9's `AnswerGovernor` via Vol 2. No direct Vol 8 → Vol 9 call needed for basic chat flow. No mismatch.
- **Vol 1 (Memory):** Vol 8 consumes `MemoryManager.get_stats()` and `get_recent_conversations()` for admin/health endpoints. These are documented dependencies in AGENT_COMM.md. No mismatch.

**Question 5: Is anything missing that a coding agent would need to ask about?**

- **WebSocket telemetry protocol:** Deferred to post-MVA (Tier 4+). The event bus recommendation from shared-contracts Section 4 applies. Vol 8 owns the WebSocket transport when built.
- **Session CRUD endpoints:** `GET/POST/DELETE /v1/sessions` requested by Vol 7. Deferred to when Console is built (Tier 6+). Route module `api/routes/sessions.py` will be added then.
- **Memory admin endpoints:** `GET /v1/memory/layers`, `GET /v1/memory/search` requested by Vol 7. Deferred. Route module `api/routes/memory.py` will be added when Vol 1 memory endpoints are built.
- **HTTPS/TLS:** Local-first (R7), no TLS at the application layer. A reverse proxy (nginx, Caddy) handles TLS in production. This is infrastructure, not application concern.

**Question 6: Are the B.4 verdicts still correct after deep dive, or do any need revision?**

All B.4 verdicts stand. No changes. The deep dive confirmed:
- `server.py` REBUILD is correct — the god object must be decomposed.
- `middleware.py` REBUILD is correct — the three-middleware pattern is preserved with config improvements.
- `telemetry_middleware.py` DEFER is correct — observability is post-MVA.
- All 25 KILLed routes are confirmed as development tooling, stubs, or simulated capabilities.
- All 10 DEFERred routes are confirmed as dependent on subsystems built in Tier 3+.

### B.13 Design Quality Scorecard

1. **Volume 0 Compliance** — Does the design honor all relevant Volume 0 principles?
   Score: **5/5**. P1 (ML advises, symbolic decides) — not directly API concern but not violated. P2 (governance enables) — graduated route registration. P3 (nothing ships without integration) — endpoints require backing subsystem acceptance test. P5 (silent failure is fault) — error handling enforces logging. P8 (Pydantic at boundaries) — every endpoint has request/response schemas. P11 (acceptance tests gate) — 5 acceptance tests defined.

2. **Interface Completeness** — Are all consumed/provided interfaces fully specified?
   Score: **5/5**. B.3 specifies 8 interface contracts with exact schemas. B.6 specifies all Pydantic models with field types and constraints. Shared contract compliance verified in B.12.

3. **Anti-Pattern Avoidance** — Does the design avoid all Volume 0 anti-patterns?
   Score: **5/5**. Each of A1-A8 addressed explicitly in B.12 Q3. The design starts minimal (2 route files) and grows only with proven subsystems.

4. **Testability** — Can acceptance tests be written from this spec alone?
   Score: **4/5**. 5 acceptance tests, 5 integration tests, 10 unit tests, 3 regression tests defined with specific inputs and expected outputs. Deduction: WebSocket telemetry testing is deferred (no acceptance test for it yet).

5. **Shared Contract Conformance** — Does the design match approved shared contracts?
   Score: **5/5**. All schemas in shared-contracts.md Section 1.3 are reflected in B.6. All API boundary contracts in Section 2.1 and 2.14 are covered. C-10, C-11, C-12, C-13, C-16, C-17 resolutions incorporated.

6. **Scope Discipline** — Is the rebuild scope minimal and justified?
   Score: **5/5**. 5 REBUILD files out of 40. 25 KILL (62.5% reduction). Clear justification per file. MVA starts with 3 files, grows to 4 at Tier 2.

7. **Specificity** — Could a coding agent implement from this spec without questions?
   Score: **4/5**. Schemas, error hierarchy, middleware stack, config, and mapping logic are fully specified. Deduction: WebSocket protocol for telemetry streaming is deferred, so a coding agent building that later would need additional spec.

8. **Lessons Integration** — Are Attempt 3 failures concretely addressed?
   Score: **5/5**. B.10 lists 7 specific lessons with concrete code references (line numbers, file names). Each lesson maps to a design decision in B.2-B.9. Regression tests REG-01 through REG-03 prevent specific recurrences.

9. **Documentation Quality** — Is the volume clear, structured, and internally consistent?
   Score: **4/5**. All sections filled. Cross-references between sections (B.7 references B.2, B.12 references B.4, etc.). Deduction: some sections are necessarily verbose due to the number of schemas and contracts.

**Total: 42/45** (minimum passing: 30/45) — **PASS**

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (5 server files, 35+ route files, error/config files), context brief, and 5 known failure warnings including 81 endpoints needing triage and SQLite async pitfalls | Created the API/infrastructure analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V08-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
|| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 Source Manifest per DISTILLATION_PROTOCOL.md Section 5 | Labeled which files agents should read in full vs. skim during Phase 1 |
|| v5 | 2026-03-10 | Distillation Agent V8 | Phase 1: Filled B.1 (Subsystem Purpose), B.2 (Architecture Overview with 5 components + data flow + concurrency model), B.3 (8 interface contracts: server factory, health, chat, streaming, errors, middleware, config, route pattern), B.4 (Scope Triage: 5 REBUILD, 10 DEFER, 25 KILL across 40 files) | Wrote the design spec for the rebuilt API server — what endpoints to keep, what to kill, and exactly how they should work |
|| v6 | 2026-03-11 | Distillation Agent V8 | Phase 2: Filled B.5 (Technology Choices — 8 decisions: FastAPI keep, Uvicorn keep, pydantic-settings new, structlog new, aiosqlite new, CORS restricted, httpx keep, TS codegen new), B.6 (Data Model — 8 Pydantic schemas in contracts/api_schemas.py with field-level spec), B.7 (Error Handling — 8-class hierarchy with HTTP status mapping and forbidden patterns), B.8 (Testing Strategy — 5 acceptance, 5 integration, 10 unit, 3 regression tests), B.9 (Configuration — AtlasConfig schema with env prefix and feature flags), B.10 (7 Subsystem Lessons from Attempt 3), B.11 (5 Discoveries including middleware preservation and streaming risk), B.12 (Oversight Self-Review — 6 questions, all A.4 items addressed, all shared contracts verified, all anti-patterns avoided), B.13 (Scorecard 42/45 PASS) | Deep-dived into every source file and wrote the detailed technical spec — what technologies to use, what data flows where, how errors work, and verified the design doesn't repeat past mistakes |
