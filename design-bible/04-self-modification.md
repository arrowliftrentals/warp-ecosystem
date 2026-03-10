# ATLAS Design Bible — Volume 4: Self-Modification & Sandbox

| Field | Value |
|---|---|
| **Doc ID** | `DB-V04-001` |
| **Name** | Volume 4: Self-Modification & Sandbox |
| **Purpose** | Design specification for the self-improvement pipeline — propose, test, validate, and apply code changes with sandbox safety |
| **Owner** | Design Bible / Volume 4 |
| **Status** | `draft` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / Distillation Agent V4 (Part B) |
| **Version** | v5 |
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

**CORE/PERIPHERAL Classification** (per `DISTILLATION_PROTOCOL.md` Section 5):
- **CORE** (14 files): `modifier.py`, `verification_tracker.py`, `meta_cognitive_monitor.py`, `risk_assessment.py`, `code_analyzer.py`, `approval_automator.py`, `validation_orchestrator.py`, `design_validator.py`, `api_contract_validator.py`, `integrity_guard.py`, `exceptions.py`, sandbox: `manager.py`, `executor.py`, `docker_executor.py`
- **PERIPHERAL** (44 files): All fix-related (6), guard files except integrity_guard (4), all pattern files (5), sandbox variants (`vm_provider.py`, `utm_provider*.py`, `screen_capture.py`, `resource_guard.py`), `meta_meta_monitor.py`, enforcement files, and all remaining

### A.3 Context Brief

**What worked in Attempt 3:**
- Sandbox execution via Docker
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

The self-modification subsystem enables Atlas to propose, sandbox-test, verify, and apply changes to its own codebase with cryptographic proof that validation actually occurred. It is the enforcement arm of Principle P4 ("validation must be real") — the subsystem that makes validation theater structurally impossible. The rebuild must provide a minimal, end-to-end pipeline: a `SelfModifier` accepts a proposed code change, clones the codebase into a Docker sandbox, applies the change, runs the full test suite, signs the execution output via `VerificationTracker` (HMAC-SHA256), scores the risk via `RiskAssessor`, and either auto-approves (low risk, all gates passed) or escalates to the human. A `MetaCognitiveMonitor` audits every proposal for validation theater patterns (claims without execution evidence, stale evidence, generic claims). The sandbox layer provides isolated Docker-based code execution with snapshot-and-rollback safety. The entire pipeline must work end-to-end in under 10 minutes for a typical change, and every claim must be backed by cryptographic evidence stored in L4 declarative memory. This is one of Atlas's three moat capabilities (Volume 0, Section 3.2) and must be built to survive, not to impress.

### B.2 Architecture Overview

The rebuild has five major components organized into two domains: the **proposal pipeline** (propose, test, approve) and the **sandbox layer** (isolate, execute, rollback).

```
┌─────────────────── PROPOSAL PIPELINE ───────────────────┐
│                                                          │
│  CodeChange ──► SelfModifier.propose_improvement()       │
│                    │                                     │
│                    ├─► clone_to_sandbox()                │
│                    ├─► apply_changes()                   │
│                    ├─► run_validation()                  │
│                    │     └─► ValidationOrchestrator      │
│                    │           (syntax→imports→API→      │
│                    │            patterns→intent)          │
│                    ├─► VerificationTracker               │
│                    │     (HMAC-sign test output,         │
│                    │      store claim in L4)             │
│                    ├─► MetaCognitiveMonitor              │
│                    │     (audit for theater patterns)    │
│                    ├─► RiskAssessor                      │
│                    │     (7 gates → risk score)          │
│                    └─► ApprovalAutomator                 │
│                          (auto-approve LOW / escalate)   │
│                              │                           │
│                    ┌─────────┴─────────┐                 │
│                    ▼                   ▼                  │
│              apply_to_prod()    reject + log             │
│              (git branch+commit)                         │
└──────────────────────────────────────────────────────────┘

┌─────────────────── SANDBOX LAYER ───────────────────────┐
│                                                          │
│  SandboxManager                                          │
│    ├─ DockerProvider  (create/start/stop/snapshot)       │
│    ├─ SandboxExecutor (SSH-based command execution)      │
│    │     └─ Signs output via VerificationTracker         │
│    └─ ResourceGuard   (disk usage ceiling enforcement)   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Data flow:** A caller constructs one or more `CodeChange` objects (file path, original content, modified content, rationale). `SelfModifier.propose_improvement()` orchestrates the full lifecycle. The sandbox clone uses rsync with incremental sync for speed. Validation runs pytest inside the container, parses verbose output to extract per-test PASSED/FAILED status. The `VerificationTracker` signs the raw command output (HMAC-SHA256 with a nonce) and stores the signed claim as an immutable `Fact` in L4 declarative memory. `MetaCognitiveMonitor` runs 7 heuristic checks against the proposal (claims without execution evidence, generic claims, timestamp gaps, missing pytest markers, success-only testing, critical file changes, bypass attempts). `RiskAssessor` evaluates 7 gates (test pass rate, critical files, scope, verification quality, execution evidence, dependencies, rollback feasibility) and produces a risk level (LOW/MEDIUM/HIGH/CRITICAL). `ApprovalAutomator` auto-approves only when risk is LOW and all gates pass; everything else escalates to the human. Approved proposals are applied via git branch + commit in the appropriate repository.

**Key dependencies consumed:**
- Volume 1 (Memory): MemoryManager, L4 declarative memory for storing validation claims, L7 world state for execution proofs
- Volume 9 (Governance): DecisionValidator for intent safety checks in ValidationOrchestrator
- Volume 8 (API): Dashboard SSE broadcast for sandbox execution events

**Key dependencies served:**
- Volume 2 (Orchestrator): `SelfModifier` is invoked from orchestrator tool calls
- Volume 3 (Learning): Proposal outcomes feed the learning pipeline

### B.3 Interface Contracts

#### 3.1 SelfModifier (Core Pipeline)

**Location (rebuild):** `src/atlas/self_modify/modifier.py`

**Input schemas:**
```
class CodeChange(BaseModel):
    file_path: Path
    original_content: str
    modified_content: str
    diff: str
    rationale: str
    model_config = {"frozen": True}
```

**Output schemas:**
```
class ProposalStatus(str, Enum):
    PENDING = "pending"
    APPLIED = "applied"
    REJECTED = "rejected"
    ROLLED_BACK = "rolled_back"

class ImprovementProposal(BaseModel):
    id: str  # timestamp-based
    title: str
    description: str
    changes: list[CodeChange]
    created_at: datetime
    validation_passed: bool
    tests_passed: int
    tests_failed: int
    estimated_risk: RiskLevel
    status: ProposalStatus = ProposalStatus.PENDING
    applied_at: datetime | None = None
    rejected_at: datetime | None = None
    rejection_reason: str | None = None
    impact_analysis: dict[str, Any] | None = None
    model_config = {"frozen": False}  # status is mutable
```

**Public methods:**
- `async propose_improvement(title: str, description: str, changes: list[CodeChange], progress_callback: Callable | None = None) -> ImprovementProposal` — Full lifecycle: clone → apply → validate → create proposal.
- `async apply_proposal_to_production(proposal: ImprovementProposal) -> bool` — Apply approved proposal via git branch + commit.

**Dependencies consumed:**
- `SandboxManager` (sandbox layer)
- `VerificationTracker` (validation proof)
- `MemoryManager` (via VerificationTracker for L4 storage)

**Dependencies served:**
- Orchestrator tool system (Volume 2) calls `propose_improvement()`

---

#### 3.2 VerificationTracker (Cryptographic Proof)

**Location (rebuild):** `src/atlas/self_modify/verification.py`

**Input schemas (from Volume 1 memory schemas):**
```
class CommandEvidence(BaseModel):
    command: str
    exit_code: int
    stdout: str
    stderr: str
    timestamp: datetime
    duration_seconds: float
    executed_in: str  # sandbox ID or "local"
    signature: str  # HMAC-SHA256 hex
    nonce: str  # replay prevention
    proposal_id: str | None = None
    model_config = {"frozen": True}

class ValidationClaimType(str, Enum):
    TESTS_PASSED = "tests_passed"
    LINTING_CLEAN = "linting_clean"
    TYPE_CHECK_CLEAN = "type_check_clean"

class ValidationClaim(BaseModel):
    claim_id: str
    claim_type: ValidationClaimType
    claim_statement: str
    evidence: CommandEvidence
    verified: bool = False
    verified_at: datetime | None = None
    fact_id: str | None = None  # L4 fact ID
```

**Public methods:**
- `sign_command_output(command, exit_code, stdout, stderr, timestamp, duration_seconds, executed_in, nonce, proposal_id) -> str` — Returns HMAC-SHA256 hex signature.
- `verify_signature(evidence: CommandEvidence, enforce_freshness: bool = True) -> bool` — Constant-time HMAC comparison. Raises `ValidationTheaterError` if evidence is stale (>1 hour).
- `claim_validation(claim_type: ValidationClaimType, statement: str, evidence: CommandEvidence) -> ValidationClaim` — Verify signature, store in L4 as immutable fact.
- `has_verified_claims(proposal_id: str, required_types: list[ValidationClaimType] | None = None) -> bool` — Check if proposal has all required verified claims.
- `sign_local_command(command, exit_code, stdout, stderr, duration_seconds, proposal_id) -> CommandEvidence` — Sign evidence from non-sandbox execution.

**Dependencies consumed:**
- `MemoryManager.l4` (Volume 1) — stores validated claims as facts
- Secure key storage (macOS Keychain or machine-ID derived)

**Dependencies served:**
- `SandboxExecutor` signs every command output
- `SelfModifier` checks `has_verified_claims()` before accepting proposals

---

#### 3.3 MetaCognitiveMonitor (Theater Detection)

**Location (rebuild):** `src/atlas/self_modify/monitor.py`

**Public methods:**
- `analyze_proposal(proposal: dict[str, Any], execution_logs: list[dict] | None = None) -> list[ValidationTheaterIssue]` — Run 7 heuristic checks. Returns empty list if clean.
- `should_auto_reject(issues: list[ValidationTheaterIssue]) -> bool` — Returns True if any issue has severity "critical".

**Output schema:**
```
class ValidationTheaterIssue(BaseModel):
    severity: Literal["critical", "warning", "info"]
    pattern: str  # e.g. "claimed_validation_without_execution"
    evidence: str
    recommendation: str
    proposal_id: str | None = None
    detected_at: datetime
```

**Dependencies consumed:**
- `VerificationTracker` — to cross-check claims
- `MemoryManager` — to store detected patterns for learning

---

#### 3.4 RiskAssessor (Risk Scoring)

**Location (rebuild):** `src/atlas/self_modify/risk.py`

**Output schemas:**
```
class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RiskFactor(BaseModel):
    name: str
    level: RiskLevel
    score: float  # 0.0 (safe) to 1.0 (dangerous)
    reason: str
    blocking: bool = False

class RiskAssessment(BaseModel):
    proposal_id: str
    overall_level: RiskLevel
    overall_score: float
    risk_factors: list[RiskFactor]
    gates_passed: dict[str, bool]
    all_gates_passed: bool
    blocking_reasons: list[str]
    auto_approve_eligible: bool
```

**Public methods:**
- `assess_proposal(proposal: dict, verification_issues: list[ValidationTheaterIssue], execution_logs: list[dict] | None) -> RiskAssessment`

**7 gates:** test_pass_rate, critical_files, change_scope, verification_quality, execution_evidence, dependencies, rollback_feasibility.

**Dependencies consumed:** None (stateless evaluator).

---

#### 3.5 ApprovalAutomator

**Location (rebuild):** `src/atlas/self_modify/approval.py`

**Output schema:**
```
class ApprovalResult(BaseModel):
    approved: bool
    auto: bool  # True if auto-approved
    reason: str
    proposal_id: str
    risk_assessment: RiskAssessment | None = None
    timestamp: datetime
```

**Public methods:**
- `evaluate_proposal(proposal: dict, execution_logs: list[dict] | None) -> ApprovalResult`

**Dependencies consumed:**
- `RiskAssessor`
- `MetaCognitiveMonitor`
- `MemoryManager` (audit trail in L4)

---

#### 3.6 ValidationOrchestrator (Multi-Stage Validation)

**Location (rebuild):** `src/atlas/self_modify/validation.py`

**Output schemas:**
```
class ValidationStage(str, Enum):
    SYNTAX = "syntax"
    IMPORTS = "imports"
    API_CONTRACTS = "api_contracts"
    PATTERNS = "patterns"
    INTENT = "intent"

class StageResult(BaseModel):
    stage: ValidationStage
    passed: bool
    severity: Literal["error", "warning", "info"]
    issues: list[str]
    duration_ms: float

class OrchestratorResult(BaseModel):
    is_valid: bool
    stages: list[StageResult]
    blocking_errors: list[str]
    warnings: list[str]
    total_duration_ms: float
```

**Public methods:**
- `validate(content: str, file_path: Path | None, context: dict | None) -> OrchestratorResult` — Runs syntax → imports → API contracts (→ patterns → intent if configured). Fail-fast on blocking errors.

**Dependencies consumed:**
- `APIContractValidator` (internal)
- `DecisionValidator` (Volume 9, optional)

---

#### 3.7 APIContractValidator

**Location (rebuild):** `src/atlas/self_modify/api_contracts.py`

**Output schema:**
```
class APIViolation(BaseModel):
    file_path: str
    line: int
    violation_type: str  # "missing_method", "wrong_signature"
    expected: str | None
    actual: str | None
    message: str

class APIValidationResult(BaseModel):
    is_valid: bool
    violations: list[APIViolation]
    methods_checked: int
```

**Public methods:**
- `validate(code: str, file_path: Path | None) -> APIValidationResult` — AST-based detection of method calls against known API definitions.
- `add_known_api(component: str, methods: list[str]) -> None` — Register new API surface.

**Dependencies consumed:** None (AST analysis only, known APIs are hardcoded + extensible).

---

#### 3.8 SandboxManager

**Location (rebuild):** `src/atlas/self_modify/sandbox/manager.py`

**Public methods:**
- `async create_sandbox(name, os_type, memory_mb, cpu_count, disk_size_gb) -> str` — Create and baseline-snapshot a sandbox.
- `async start_sandbox(vm_id, headless=True) -> None`
- `async create_snapshot(vm_id, name, description) -> str` — With ResourceGuard pre-check.
- `async restore_snapshot(vm_id, snapshot_id) -> None`
- `async execute_command(command, timeout, cwd) -> ExecutionResult`
- `async execute_code(code, language, timeout, cwd) -> ExecutionResult`
- `async with_snapshot_protection(vm_id, operation_name, operation_func, auto_rollback_on_error) -> Any` — Snapshot before operation, rollback on failure.
- `close() -> None`

**Dependencies consumed:**
- `DockerProvider` (Docker SDK)
- `SandboxExecutor` (SSH-based execution)
- `ResourceGuard` (disk usage enforcement)

---

#### 3.9 SandboxExecutor

**Location (rebuild):** `src/atlas/self_modify/sandbox/executor.py`

**Output schema:**
```
class ExecutionResult(BaseModel):
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    execution_time: float
    error: str | None = None
    signature: str | None = None  # HMAC if VerificationTracker wired
    timestamp: str | None = None
```

**Public methods:**
- `async execute_command(command, cwd, timeout, env) -> ExecutionResult` — SSH execution with timeout and optional HMAC signing.
- `async execute_python(code, cwd, timeout) -> ExecutionResult`
- `async upload_file(local_path, remote_path) -> bool`
- `async upload_file_content(content, remote_path) -> bool`
- `async test_connection() -> bool`

**Dependencies consumed:**
- SSH/SCP (system tools)
- `VerificationTracker` (optional, for signing)

---

#### 3.10 IntegrityGuard

**Location (rebuild):** `src/atlas/self_modify/integrity.py`

**Public methods:**
- `seal_integrity() -> None` — Compute SHA-256 hashes of critical files at startup. Must be called once.
- `verify_integrity() -> None` — Recompute and compare. Raises `IntegrityViolation` if tampered.
- `get_status() -> dict[str, Any]`

**Dependencies consumed:**
- `BaselineManager` (persistent hash storage)
- Git (to distinguish committed changes from tampering)

### B.4 Scope Triage

Every file from A.2 receives a REBUILD, DEFER, or KILL verdict.

#### REBUILD (14 components — the minimal viable pipeline)

**`src/self_modify/modifier.py`** → REBUILD
Core pipeline orchestrator. Must be rebuilt as Pydantic-schema-based `SelfModifier`. Dataclass-based `CodeChange`/`ImprovementProposal` must become Pydantic `BaseModel`. Remove CognitiveFabric/CodebaseAwareness coupling (Volume 5 concern). Remove pattern library coupling. Keep: clone → apply → validate → propose → apply-to-production lifecycle.

**`src/self_modify/verification_tracker.py`** → REBUILD
Essential for P4 enforcement. HMAC-SHA256 signing, claim storage in L4, freshness checks, validation theater detection — all survive. Remove dependency on `database_guard` and `integrity_guard` inline calls (those become optional startup hooks, not per-operation checks). Schemas (`CommandEvidence`, `ValidationClaim`, `ValidationClaimType`) move to Volume 1 memory schemas or `contracts/api_schemas.py`.

**`src/self_modify/meta_cognitive_monitor.py`** → REBUILD
7 theater-detection heuristics are valuable and proven. Rebuild as stateless analyzer operating on proposal dicts. Remove MemoryManager coupling for pattern storage (defer that to learning). Keep: `analyze_proposal()`, `should_auto_reject()`.

**`src/self_modify/risk_assessment.py`** → REBUILD
Clean, stateless, evidence-based risk scoring with 7 gates. Already well-designed. Convert dataclasses to Pydantic models. Keep all 7 gates and the conservative auto-approve logic.

**`src/self_modify/approval_automator.py`** → REBUILD
Orchestrates MetaCognitiveMonitor + RiskAssessor into a single approval decision. Keep the escalation logic. Remove global singleton pattern; pass as constructor dependency.

**`src/self_modify/validation_orchestrator.py`** → REBUILD
5-stage validation chain is well-designed (syntax → imports → API contracts → patterns → intent). Already uses Pydantic schemas. Keep fail-fast behavior. Remove PatternValidator integration (DEFER). Keep DecisionValidator as optional.

**`src/self_modify/api_contract_validator.py`** → REBUILD
AST-based detection of invalid method calls. Caught real bugs (e.g., `memory.l7.get_state()` which doesn't exist). Already uses Pydantic schemas. Keep the extensible `KNOWN_APIS` registry. Add auto-discovery from runtime introspection.

**`src/self_modify/code_analyzer.py`** → REBUILD
The lightweight `CodeAnalyzer` (single-file AST analysis) is useful for tool calls. The heavy `SelfCodeAnalyzer` (full-project pylint/mypy in sandbox) can be simplified. Rebuild `CodeAnalyzer` only; defer `SelfCodeAnalyzer` to post-MVA.

**`src/self_modify/integrity_guard.py`** → REBUILD
SHA-256 file hashing and tamper detection for critical validation code. Essential safety boundary. Simplify: remove `BaselineManager` dependency (use a simpler persistent hash file). Keep: `seal_integrity()`, `verify_integrity()`, git-committed-change detection.

**`src/self_modify/exceptions.py`** → REBUILD
Narrow scope. Replace with proper error hierarchy under `atlas.shared.errors.SandboxError` per PROJECT_CONVENTIONS. Define: `ValidationTheaterError(SandboxError)`, `IntegrityViolation(SandboxError)`, `SandboxExecutionError(SandboxError)`.

**`src/sandbox/manager.py`** → REBUILD
High-level sandbox orchestration: create/start/stop/snapshot/rollback. Provider-agnostic via `VMProviderBase`. Keep snapshot protection wrapper. Remove UTM/Parallels providers (KILL). Docker-only for rebuild.

**`src/sandbox/executor.py`** → REBUILD
SSH-based remote execution with timeout, output capture, and HMAC signing integration. Clean, functional. Keep as-is with minor cleanup (remove dashboard SSE broadcast — that's Volume 8's concern).

**`src/sandbox/docker_executor.py`** → REBUILD
Direct Docker exec API execution (no SSH overhead). Useful alternative to SSH executor. Keep for local development sandboxing.

**`src/sandbox/docker_provider.py`** → REBUILD
Docker container lifecycle (create, start, stop, snapshot via `docker commit`). The only provider that works. Keep.

#### DEFER (12 components — valuable but post-MVA)

**`src/self_modify/design_validator.py`** → DEFER
Validates subsystem designs against requirements. Useful for Phase 2.3+ (autonomous subsystem development). Not needed for basic self-modification pipeline.

**`src/self_modify/dependency_graph.py`** → DEFER
AST-based dependency graph for impact prediction. Phase 2.1 of the autonomy roadmap. Valuable for predicting which tests to run after a change, but not required for MVP.

**`src/self_modify/enforcement_orchestrator.py`** → DEFER
Unified security enforcement coordinator for 6 guard layers. Useful when all guards exist. Premature until the individual guards are proven.

**`src/self_modify/enforcement_state.py`** → DEFER
Persistence of enforcement state across restarts. Needed only when enforcement orchestrator is rebuilt.

**`src/self_modify/baseline_manager.py`** → DEFER
Persistent hash storage with HMAC-signed baseline files. IntegrityGuard can use a simpler mechanism initially. Rebuild when production-grade tamper resistance is needed.

**`src/self_modify/self_improving_fixer.py`** → DEFER
Three-tier fix system (mechanical → learned patterns → LLM). The core design is sound but the full learning flywheel is a Volume 3 (Learning) concern. Defer until learning pipeline is integrated.

**`src/self_modify/auto_fixer.py`** → DEFER
Facade for pluggable fix generation. Depends on self_improving_fixer, fix_templates, learning_manager. Defer until the pipeline it orchestrates is rebuilt.

**`src/self_modify/mechanical_fixes.py`** → DEFER
Deterministic fixes (remove unused imports, add underscore prefix). Clean and useful. Defer because it's an optimization on top of the core pipeline, not the pipeline itself.

**`src/self_modify/fix_templates.py`** → DEFER
Template-based deterministic fixes. Same rationale as mechanical_fixes.

**`src/self_modify/fix_pattern_extractor.py`** → DEFER
Extracts generalizable patterns from successful LLM fixes. This is the self-improvement flywheel. Defer to Phase 2 when learning pipeline exists.

**`src/sandbox/resource_guard.py`** → DEFER
Disk usage ceiling enforcement. Prevents Docker disk bloat. Important operationally but not architecturally critical for MVP. Rebuild after core sandbox works.

**`src/self_modify/subsystem_architect.py`** → DEFER
Autonomous subsystem design and implementation. Phase 2.3 of autonomy roadmap. Years away from being needed.

#### KILL (32 components — over-engineering, duplication, or wrong subsystem)

**`src/self_modify/meta_meta_monitor.py`** → KILL
A monitor that monitors the monitor. Volume 0 warns about this explicitly (A.4 item 3). The rebuild should have ONE monitor (`MetaCognitiveMonitor`). If the monitor is ineffective, improve it directly — don't add a meta layer.

**`src/self_modify/monitor_effectiveness.py`** → KILL
Tracks TP/FP/TN/FN outcomes of monitoring decisions. Over-engineering for a system that doesn't have basic self-modification working yet. If needed later, it belongs in Volume 3 (Learning).

**`src/self_modify/monitor_evolution.py`** → KILL
Autonomously evolves monitoring logic. Same rationale as meta_meta_monitor. Premature.

**`src/self_modify/import_guard.py`** → KILL
Import hooks to verify integrity on module load. Over-engineering: Python import hooks are fragile and cause debugging nightmares. IntegrityGuard at startup is sufficient.

**`src/self_modify/interpreter_guard.py`** → KILL
Validates Python interpreter hasn't been replaced. Paranoid security against a threat model that doesn't apply to a personal AI running on the user's own machine.

**`src/self_modify/database_guard.py`** → KILL
Cryptographic checkpoints of L4 database. Over-engineering: the L4 database is on the user's local disk. If someone has disk access, they can bypass any guard. SQLite WAL + periodic backups are sufficient.

**`src/self_modify/dependency_guard.py`** → KILL
Validates integrity of Python stdlib and packages. Supply chain security that should be handled by pip hash checking / lockfiles, not custom runtime guards.

**`src/self_modify/subprocess_enforcer.py`** → KILL
Monkey-patches subprocess module. Invasive and brittle. Breaks third-party libraries that use subprocess legitimately. The VerificationTracker already signs sandbox commands.

**`src/self_modify/code_execution_monitor.py`** → KILL
Monkey-patches eval/exec/compile. Same invasive approach as subprocess_enforcer. Not needed in rebuild where code execution is confined to sandbox.

**`src/self_modify/process_isolation.py`** → KILL
Separate verification process via Unix socket IPC. Massive complexity for marginal security gain. The sandbox IS the isolation boundary.

**`src/self_modify/remote_attestation.py`** → KILL
Periodic integrity reports to external endpoint. No external verification service exists. Pure aspirational code.

**`src/self_modify/trusted_time.py`** → KILL
NTP-cross-validated timestamps. Over-engineering: `datetime.now()` is sufficient. The HMAC nonce in VerificationTracker prevents replay attacks.

**`src/self_modify/trusted_timestamp.py`** → KILL
Cryptographically bound timestamps with clock manipulation detection. Same rationale as trusted_time.

**`src/self_modify/safe_file_ops.py`** → KILL
TOCTOU-safe file operations with fcntl locking. Over-engineering for a single-user local system. Git is the concurrency control mechanism.

**`src/self_modify/secure_key_manager.py`** → KILL
macOS Keychain integration for HMAC key. Over-engineering: an environment variable or config file is sufficient. The key protects against LLM forgery, not against a sophisticated adversary.

**`src/self_modify/verified_agent.py`** → KILL
Warp agent wrapper with mandatory validation. This is a Warp integration concern, not a self-modification concern. If Warp integration is needed, it belongs in Volume 8 (API).

**`src/self_modify/semantic_fixes.py`** → KILL
Semantic-aware mechanical fixes using Pyright type info. Depends on external SemanticBrain not present in the codebase. Dead code.

**`src/self_modify/pattern_extractor.py`** → KILL
Architectural pattern extraction from codebase AST. This is a code generation concern, not a self-modification concern. If rebuilt, belongs in Volume 5 (Intelligence) or Volume 3 (Learning).

**`src/self_modify/pattern_validator.py`** → KILL
Validates code against extracted architectural patterns. Same rationale as pattern_extractor.

**`src/self_modify/pattern_sandbox_validator.py`** → KILL
Sandbox-tests patterns before production use. Same rationale.

**`src/self_modify/pattern_version_tracker.py`** → KILL
Pattern version history in L7. Same rationale.

**`src/self_modify/pattern_doc_generator.py`** → KILL
Generates markdown docs from patterns. Same rationale.

**`src/self_modify/template_generator.py`** → KILL
Jinja2-based code generation from patterns. Same rationale.

**`src/self_modify/integration_planner.py`** → KILL
Plans subsystem integration. Part of the autonomous development pipeline (Phase 2.3). If ever rebuilt, belongs alongside subsystem_architect.

**`src/self_modify/requirements_analyzer.py`** → KILL
Parses requirements into Pydantic schemas. Part of the autonomous development pipeline.

**`src/self_modify/protocol_loader.py`** → KILL
Loads ATLAS Development Protocol text for fix generators. Should be handled by config or prompt templates, not a dedicated module.

**`src/self_modify/fabric_mixin.py`** → KILL
CognitiveFabric lazy-init mixin. CognitiveFabric is not part of the rebuild. If knowledge consultation is needed, it flows through the memory system.

**`src/sandbox/vm_provider.py`** → REBUILD (as abstract Protocol)
Base class for VM providers. Keep as `VMProvider` Protocol definition. DockerProvider implements it.

**`src/sandbox/utm_provider.py`** → KILL
UTM AppleScript-based VM provider. UTM is unreliable and slow. Docker is the rebuild's sandbox backend.

**`src/sandbox/utm_provider_cli.py`** → KILL
UTM CLI-based provider. Same rationale.

**`src/sandbox/screen_capture.py`** → KILL
macOS screenshot capture. Not related to self-modification. If needed, belongs in Volume 10 (External Tools).

**Summary:** 14 REBUILD, 12 DEFER, 32 KILL. The rebuild targets ~8 files in `self_modify/` and ~4 files in `sandbox/` — a 79% reduction from 58 files. This aligns with Volume 0 principles P7 (smaller and working) and A5 (scope explosion prevention).

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
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 source manifest per DISTILLATION_PROTOCOL.md Section 5 | Tagged files as essential vs. nice-to-have for the rebuild analysis |
| v5 | 2026-03-10 | Distillation Agent V4 | Phase 1: Filled B.1-B.4. B.1 defines proposal pipeline and sandbox layer. B.2 has 5-component architecture (SelfModifier, VerificationTracker, MetaCognitiveMonitor, RiskAssessor/ApprovalAutomator, ValidationOrchestrator) plus sandbox layer. B.3 has 6 interface contracts. B.4 triages 58 files (14 REBUILD, 12 DEFER, 32 KILL — 79% reduction). Registered 8 ownership claims, 5 dependency declarations, 1 conflict flag in AGENT_COMM. | The self-modification agent analyzed all 58 files, kept 14 essential ones, deferred 12, and eliminated 32 as unnecessary bloat |
