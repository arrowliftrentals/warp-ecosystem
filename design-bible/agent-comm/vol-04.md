# Agent Communication — Volume 4: Self-Modification & Sandbox

**Status:** Phase 2 complete
**Last updated:** 2026-03-11

## Claims (what Vol 4 provides)

- **C-04-01:** Owns `atlas/self_modify/schemas.py` with 16 Pydantic schemas: `CodeChange`, `ProposalStatus`, `ImprovementProposal`, `RiskLevel`, `RiskFactor`, `RiskAssessment`, `ValidationTheaterIssue`, `ApprovalResult`, `ValidationStage`, `StageResult`, `OrchestratorResult`, `APIViolation`, `APIValidationResult`, `ExecutionResult`, `ResourceLimits`, `DiskReport`.
- **C-04-02:** Owns behavioral interface for verification: `VerificationTracker.sign_command_output()`, `verify_signature()`, `claim_validation()`. Uses Vol 1's `CommandEvidence`/`ValidationClaim`/`ValidationClaimType` schemas as data-at-rest (C-07 resolution).
- **C-04-03:** Owns `enforcement_orchestrator.py` and `enforcement_state.py` (C-15 resolution). Both DEFERRED to Phase 2.
- **C-04-04:** Provides `SelfModifier.propose_improvement()` as the entry point for self-modification proposals, consumed by Vol 2 (Orchestrator) tool calls.
- **C-04-05:** Provides sandbox execution via `SandboxManager` and `SandboxExecutor` (Docker-only).
- **C-04-06:** Error hierarchy rooted at `SandboxError(AtlasError)` with 5 subtypes: `ValidationTheaterError`, `IntegrityViolation`, `SandboxExecutionError`, `SandboxProvisionError`, `ProposalRejectedError`.

## Dependencies (what Vol 4 consumes)

- **D-04-01:** Vol 1 (Memory) — `MemoryManager.l4.store_fact()` and `query_facts()` for validation claim storage (shared contract Section 2.9).
- **D-04-02:** Vol 1 (Memory) — L7 world state for execution proof storage (shared contract Section 3).
- **D-04-03:** Vol 9 (Governance) — `DecisionValidator.validate_intent()` as optional intent validation stage in `ValidationOrchestrator` (shared contract Section 2.10).
- **D-04-04:** Vol 1 (Memory) — `CommandEvidence`, `ValidationClaim`, `ValidationClaimType` schemas imported from `atlas/memory/schemas.py` (C-07 resolution: Vol 1 owns data-at-rest schemas, Vol 4 owns behavioral interface).

## Resolved Conflicts

- **C-07:** Verification schema ownership. Resolution: Vol 1 owns `CommandEvidence`/`ValidationClaim`/`ValidationClaimType` as data-at-rest schemas. Vol 4 owns the behavioral interface (sign, verify, claim).
- **C-08:** `RemediationEngine` ownership. Resolution: moves to Vol 4. Currently DEFERRED (depends on `design_validator.py`).
- **C-15:** `enforcement_orchestrator.py` and `enforcement_state.py` ownership. Resolution: Vol 4 owns both. Both DEFERRED to Phase 2.

## Open Items

- None. All cross-volume conflicts resolved.
