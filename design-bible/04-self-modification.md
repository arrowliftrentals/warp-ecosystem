# ATLAS Design Bible — Volume 4: Self-Modification & Sandbox

| Field | Value |
|---|---|
| **Doc ID** | `DB-V04-001` |
| **Name** | Volume 4: Self-Modification & Sandbox |
| **Purpose** | Design specification for the self-improvement pipeline — propose, test, validate, and apply code changes with sandbox safety |
| **Owner** | Design Bible / Volume 4 |
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
- **Volume 4: Self-Modification & Sandbox**
- **Purpose:** Enables Atlas to analyze, propose, test, and apply changes to its own codebase — the self-improvement pipeline that is one of the three moat capabilities (Volume 0, Section 3.2).
- **Rebuild phase:** Phase 3 (after memory + learning). Self-modification requires a stable foundation to modify against.

### A.2 Source Manifest

**Code files to read** (paths relative to `atlas/`):

*Core self-modification:*
- `src/self_modify/modifier.py` — main modification API
- `src/self_modify/verification_tracker.py` — proof of actual test execution
- `src/self_modify/meta_cognitive_monitor.py` — detects validation theater
- `src/self_modify/meta_meta_monitor.py` — monitors the monitor
- `src/self_modify/approval_automator.py` — risk-based auto-approval
- `src/self_modify/risk_assessment.py` — change risk scoring
- `src/self_modify/code_analyzer.py` — codebase analysis
- `src/self_modify/auto_fixer.py` — automated bug fixes
- `src/self_modify/self_improving_fixer.py` — learns from fix patterns
- `src/self_modify/mechanical_fixes.py` — deterministic fixes
- `src/self_modify/semantic_fixes.py` — LLM-assisted fixes
- `src/self_modify/fix_templates.py` — fix template library
- `src/self_modify/fix_pattern_extractor.py`
- `src/self_modify/fix_learner.py`

*Validation & enforcement:*
- `src/self_modify/validation_orchestrator.py`
- `src/self_modify/design_validator.py`
- `src/self_modify/api_contract_validator.py`
- `src/self_modify/enforcement_orchestrator.py`
- `src/self_modify/enforcement_state.py`
- `src/self_modify/integrity_guard.py`
- `src/self_modify/import_guard.py`
- `src/self_modify/interpreter_guard.py`
- `src/self_modify/database_guard.py`
- `src/self_modify/dependency_guard.py`
- `src/self_modify/dependency_graph.py`

*Sandbox execution:*
- `src/sandbox/manager.py` — sandbox lifecycle management
- `src/sandbox/executor.py` — code execution in sandbox
- `src/sandbox/docker_executor.py` — Docker-based execution
- `src/sandbox/docker_provider.py` — Docker provisioning
- `src/sandbox/vm_provider.py` — VM-based sandbox
- `src/sandbox/utm_provider.py` — UTM (macOS VM) provider
- `src/sandbox/utm_provider_cli.py`
- `src/sandbox/resource_guard.py` — resource limits
- `src/sandbox/screen_capture.py` — sandbox screen capture

*Other:*
- `src/self_modify/subsystem_architect.py`
- `src/self_modify/integration_planner.py`
- `src/self_modify/template_generator.py`
- `src/self_modify/pattern_extractor.py`
- `src/self_modify/pattern_validator.py`
- `src/self_modify/pattern_sandbox_validator.py`
- `src/self_modify/pattern_version_tracker.py`
- `src/self_modify/pattern_doc_generator.py`
- `src/self_modify/baseline_manager.py`
- `src/self_modify/code_execution_monitor.py`
- `src/self_modify/process_isolation.py`
- `src/self_modify/protocol_loader.py`
- `src/self_modify/remote_attestation.py`
- `src/self_modify/requirements_analyzer.py`
- `src/self_modify/safe_file_ops.py`
- `src/self_modify/secure_key_manager.py`
- `src/self_modify/subprocess_enforcer.py`
- `src/self_modify/trusted_time.py`
- `src/self_modify/trusted_timestamp.py`
- `src/self_modify/verified_agent.py`
- `src/self_modify/monitor_effectiveness.py`
- `src/self_modify/monitor_evolution.py`
- `src/self_modify/fabric_mixin.py`
- `src/self_modify/exceptions.py`

**Documentation to read:**
- `docs/SELF_BUILDING_ATLAS_ROADMAP.md` — 36-month autonomy roadmap
- `docs/architecture/modifier.md`
- `docs/architecture/verification-tracker.md`
- `docs/architecture/verified-orchestrator.md`
- `docs/architecture/self-improving-fix-system.md`
- `docs/architecture/self-modify-tools.md`
- `docs/architecture/sandbox-tools.md`
- `docs/architecture/safety-execution-system.md`
- `docs/architecture/zero-bypass-enforcement.md`
- `docs/development/self-modification-readiness.md`
- `docs/development/safety-system-implementation.md`
- `docs/guides/safety-execution.md`
- `docs/adr/0015-validation-enforcement.md`
- `docs/adr/0024-meta-meta-cognition.md`
- `docs/atlas-evolution-pattern.md` — 5-rule safe evolution

**Test files to read:**
- `tests/self_modify/` (if exists)
- `tests/sandbox/` (if exists)

### A.3 Context Brief

**What worked in Attempt 3:**
- Sandbox execution via Docker with proposal workflow
- Self-modification pipeline: propose → sandbox test → human approval → apply with rollback
- Proposals stored in `.proposals/` directory with metadata
- Verification tracker concept (proof of test execution) was designed and partially implemented
- Git-based rollback mechanism

**What failed or was never wired:**
- 49 files in src/self_modify/ — massive scope explosion
- Meta-cognitive monitor, meta-meta monitor — layers of monitoring that may be over-engineered
- Approval automator existed but unclear if it functioned
- Multiple guard files (import, interpreter, database, dependency) — unclear which are real vs. stubs
- Remote attestation, trusted timestamps — advanced security features likely never integrated
- Feature flags for self-modification likely set to FALSE

**What was simulated/fake:**
- Some "fix" templates returned `False # TODO: implement` (A7 anti-pattern)
- Validation claims may have been made without actual execution evidence

**Relevant Volume 0 principles:**
- P4: Validation must be real (this is the subsystem that ENFORCES this)
- L3: Validation theater is the #1 risk
- A2: Validation theater
- A7: TODO in production code
- Section 3.2: Self-modification is an "extremely unique" moat capability

### A.4 Known Failures & Warnings
1. **49 files is extreme scope explosion**: The self-modify system has more files than most entire projects. Aggressive KILL/DEFER triage is critical.
2. **Validation theater risk**: This subsystem's core job is preventing validation theater. If IT has validation theater, the entire system is compromised. Scrutinize closely.
3. **Meta-meta monitoring**: A monitor that monitors the monitor that monitors the system may be over-engineering. Determine if this is necessary or gold-plating.
4. **Docker dependency**: Sandbox requires Docker Desktop on macOS. Consider if this is acceptable for the rebuild or if alternatives (UTM, process isolation) are needed.
5. **The 36-month roadmap**: The SELF_BUILDING_ATLAS_ROADMAP defines the autonomy phases. The distillation agent must determine what belongs in Phase 3 (rebuild) vs. later phases.

---

## Part B: Design Specification (Agent Fills Out)

### B.1 Subsystem Purpose (Rebuild)
*[To be filled by distillation agent]*

### B.2 Architecture Overview
*[To be filled by distillation agent]*

### B.3 Interface Contracts
*[To be filled by distillation agent]*

### B.4 Scope Triage
*[To be filled by distillation agent — every component in A.2 must get a REBUILD/DEFER/KILL verdict]*

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
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (49 self-modify + 10 sandbox files, 12+ docs), context brief, and 5 known failure warnings including extreme scope explosion and validation theater risk | Created the self-modification system analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V04-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
