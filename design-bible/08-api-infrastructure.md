# ATLAS Design Bible — Volume 8: API & Infrastructure

| Field | Value |
|---|---|
| **Doc ID** | `DB-V08-001` |
| **Name** | Volume 8: API & Infrastructure |
| **Purpose** | Design specification for the server, routing, middleware, error handling, configuration, startup, and concurrency model |
| **Owner** | Design Bible / Volume 8 |
| **Status** | `draft` (scaffold — Part A pre-loaded, Part B awaiting distillation agent) |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / TBD distillation agent (Part B) |
| **Version** | v4 |
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
*[To be filled by distillation agent]*

### B.2 Architecture Overview
*[To be filled by distillation agent]*

### B.3 Interface Contracts
*[To be filled by distillation agent]*

### B.4 Scope Triage
*[To be filled by distillation agent — every route file in A.2 must get a REBUILD/DEFER/KILL verdict]*

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
