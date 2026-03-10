# ATLAS Design Bible — Volume 8: API & Infrastructure

| Field | Value |
|---|---|
| **Doc ID** | `DB-V08-001` |
| **Name** | Volume 8: API & Infrastructure |
| **Purpose** | Design specification for the server, routing, middleware, error handling, configuration, startup, and concurrency model |
| **Owner** | Design Bible / Volume 8 |
| **Status** | `phase-1-complete` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / Distillation Agent V8 (Part B) |
| **Version** | v5 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

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
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (5 server files, 35+ route files, error/config files), context brief, and 5 known failure warnings including 81 endpoints needing triage and SQLite async pitfalls | Created the API/infrastructure analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V08-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 Source Manifest per DISTILLATION_PROTOCOL.md Section 5 | Labeled which files agents should read in full vs. skim during Phase 1 |
| v5 | 2026-03-10 | Distillation Agent V8 | Phase 1: Filled B.1 (Subsystem Purpose), B.2 (Architecture Overview with 5 components + data flow + concurrency model), B.3 (8 interface contracts: server factory, health, chat, streaming, errors, middleware, config, route pattern), B.4 (Scope Triage: 5 REBUILD, 10 DEFER, 25 KILL across 40 files) | Wrote the design spec for the rebuilt API server — what endpoints to keep, what to kill, and exactly how they should work |
