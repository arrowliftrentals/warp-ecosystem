# ATLAS Design Bible — Volume 10: External Tools & Capabilities

| Field | Value |
|---|---|
| **Doc ID** | `DB-V10-001` |
| **Name** | Volume 10: External Tools & Capabilities |
| **Purpose** | Design specification for the tool ecosystem — file ops, git, web, STEM computation, security tools, screen control, and tool registry |
| **Owner** | Design Bible / Volume 10 |
| **Status** | `draft` (scaffold — Part A pre-loaded, Part B awaiting distillation agent) |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / TBD distillation agent (Part B) |
| **Version** | v3 |
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
*[To be filled by distillation agent]*

### B.2 Architecture Overview
*[To be filled by distillation agent]*

### B.3 Interface Contracts
*[To be filled by distillation agent]*

### B.4 Scope Triage
*[To be filled by distillation agent — every tool in A.2 must get a REBUILD/DEFER/KILL verdict]*

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
