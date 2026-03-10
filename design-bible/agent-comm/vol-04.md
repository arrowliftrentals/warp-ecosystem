# Agent Communication — Volume 4: Self-Modification & Sandbox

> **Rules:** Append new claims/dependencies/conflicts using the formats defined in `AGENT_COMM.md`.
> This file is the ONLY place Vol 4 agents register changes. Do NOT edit `AGENT_COMM.md` directly.

---

## Ownership Claims

```
CLAIM: SelfModifier pipeline (propose > sandbox > verify > approve > apply)
OWNER: Volume 4
REASON: Core self-modification lifecycle orchestrating CodeChange to ImprovementProposal with full sandbox testing.
CONTESTED: no
```

```
CLAIM: VerificationTracker (HMAC-SHA256 cryptographic proof of test execution)
OWNER: Volume 4
REASON: Enforcement arm of P4 (validation must be real). Signs command output, stores claims in L4.
CONTESTED: no
```

```
CLAIM: MetaCognitiveMonitor (validation theater detection)
OWNER: Volume 4
REASON: 7 heuristic checks for validation theater patterns. Operates on proposals pre-approval.
CONTESTED: no
```

```
CLAIM: RiskAssessor + ApprovalAutomator (risk scoring and graduated approval)
OWNER: Volume 4
REASON: 7-gate risk scoring with auto-approve (LOW risk only) / human escalation.
CONTESTED: no
```

```
CLAIM: ValidationOrchestrator + APIContractValidator (multi-stage code validation)
OWNER: Volume 4
REASON: 5-stage validation chain (syntax > imports > API contracts > patterns > intent).
CONTESTED: no
```

```
CLAIM: SandboxManager + SandboxExecutor + DockerProvider + DockerExecutor (sandbox layer)
OWNER: Volume 4
REASON: Docker-based isolated code execution with snapshot-and-rollback.
CONTESTED: no
```

```
CLAIM: IntegrityGuard (SHA-256 tamper detection)
OWNER: Volume 4
REASON: Critical file hash verification at startup. Detects unauthorized modification of validation code.
CONTESTED: no
```

```
CLAIM: enforcement_orchestrator.py and enforcement_state.py
OWNER: Volume 4
REASON: Self-modification enforcement execution. Vol 9 governs the DECISION (via DecisionValidator); Vol 4 owns the EXECUTION.
CONTESTED: no (resolved — conflict-report.md)
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 4 needs MemoryManager.l4 (store_fact, query_facts) from Volume 1
STATUS: pending
INTERFACE: store_fact(content, source, confidence, metadata) -> str; query_facts(query, min_confidence, limit) -> list[DeclarativeFact]
```

```
DEPENDENCY: Volume 4 needs CommandEvidence/ValidationClaim Pydantic schemas from Volume 1
STATUS: pending
INTERFACE: CommandEvidence(BaseModel), ValidationClaim(BaseModel), ValidationClaimType(str, Enum)
```

```
DEPENDENCY: Volume 4 needs DecisionValidator.validate_intent() from Volume 9
STATUS: pending
INTERFACE: DecisionValidator.validate_intent(intent: str, context: dict) → ValidationDecision
```

```
DEPENDENCY: Volume 4 needs API endpoint registration from Volume 8
STATUS: pending
INTERFACE: POST /v1/proposals, GET /v1/proposals/{id}, POST /v1/sandbox/execute
```

```
DEPENDENCY: Volume 4 needs LearningManager.record_proposal_outcome() from Volume 3
STATUS: pending
INTERFACE: record_proposal_outcome(proposal_id, proposal_type, status, ...) -> dict (insights)
```

---

## Conflict Acknowledgements

```
CONFLICT: Verification schemas ownership
VOLUMES: 1 vs 4
RESOLUTION: resolved — Vol 1 owns schemas (data at rest). Vol 4 owns behavioral interface (conflict-report.md C-07)
```

```
CONFLICT: enforcement_orchestrator.py and enforcement_state.py ownership
VOLUMES: 4 vs 9
RESOLUTION: resolved — Vol 4 owns execution. Vol 9 owns decision (conflict-report.md)
```

```
CONFLICT: RemediationEngine overlap
VOLUMES: 4 vs 5 vs 9
RESOLUTION: resolved — RemediationEngine → Vol 4. Vol 5 owns diagnostics (conflict-report.md C-08)
```
