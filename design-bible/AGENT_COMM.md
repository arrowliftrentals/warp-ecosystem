# Agent Communication Hub

| Field | Value |
|---|---|
| **Doc ID** | `DB-X00-003` |
| **Name** | Agent Communication Hub |
| **Purpose** | Persistent coordination file where distillation agents register ownership claims, dependencies, and conflicts across volumes |
| **Owner** | Design Bible / Infrastructure |
| **Status** | `active` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz |
| **Version** | v5 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## Rules

### Ownership Claims
When a distillation agent determines that a component belongs to THEIR volume, they register ownership here. If two agents claim the same component, the conflict must be resolved before either volume is submitted.

Format:
```
CLAIM: [component name]
OWNER: Volume [N]
REASON: [one sentence]
CONTESTED: [yes/no]
```

### Dependency Declarations
When a distillation agent's subsystem needs something from another volume, they declare it here. The owning volume must define the interface; the consuming volume references it.

Format:
```
DEPENDENCY: Volume [consumer] needs [what] from Volume [provider]
STATUS: [pending/acknowledged/resolved]
INTERFACE: [schema name or method signature, once resolved]
```

### Conflict Flags
When two volumes have incompatible design decisions, flag it here for resolution.

Format:
```
CONFLICT: [description]
VOLUMES: [N] vs [M]
PROPOSED RESOLUTION: [suggestion]
STATUS: [open/resolved]
RESOLUTION: [final decision]
```

---

## Pre-Registered Ownership (Known Boundaries)

These ownership decisions are made upfront to prevent predictable conflicts:

### Memory Schemas
- **Owner: Volume 1 (Memory)**
- All Pydantic schemas for data entering/leaving memory layers are defined by Volume 1
- Other volumes CONSUME these schemas, they do not redefine them
- If another volume needs a new field or schema, they declare a DEPENDENCY here

### Intent Validation
- **Owner: Volume 9 (Governance)**
- DecisionValidator and all validation gate logic belongs to Volume 9
- Volume 2 (Orchestrator) CONSUMES validation, it does not own it

### Output Governance
- **Owner: Volume 9 (Governance)**
- GovernedOutput, AnswerGovernor, claim extraction, evidence grounding
- Volume 2 (Orchestrator) integrates governance into the response pipeline but does not own the governance logic

### Knowledge Pipeline
- **Owner: Volume 3 (Learning)** owns the ingestion, extraction, and synthesis pipeline
- **Volume 5 (Intelligence)** owns the amplification layer (analogical reasoning, hypothesis generation, Socratic challenge, growth tracking)
- **Boundary:** Volume 3 produces `RefinedKnowledge`. Volume 5 consumes it.
- Extractors (`src/learning/extractors/`) belong to Volume 3
- `src/intelligence/` components belong to Volume 5

### Tool Registry
- **Owner: Volume 10 (External Tools)** owns the tool infrastructure and individual tools
- Volume 2 (Orchestrator) owns tool INVOCATION (how tools are called during conversation)
- Volume 10 owns tool DEFINITION (what tools exist and what they do)

### Voice Governance Schemas
- **Owner: Volume 9 (Governance)** owns the governance pattern (AuthorityLevel, grounding)
- **Volume 6 (Voice)** owns the voice-specific implementation (TTS, STT, WebRTC)
- ApprovedUtterance is superseded by GovernedOutput in the rebuild; Volume 9 defines the unified schema

### API Endpoints
- **Owner: Volume 8 (API)** owns the server, routing, middleware, and endpoint registration
- Each subsystem volume defines WHAT endpoints their subsystem needs
- Volume 8 defines HOW those endpoints are implemented (FastAPI patterns, error responses, etc.)

---

## Ownership Claims (Agent-Registered)

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

---

## Dependency Declarations (Agent-Registered)

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
INTERFACE: validate_intent(intent, context) -> ValidationResult
```

```
DEPENDENCY: Volume 4 needs API endpoint registration from Volume 8
STATUS: pending
INTERFACE: POST /v1/proposals, GET /v1/proposals/{id}, POST /v1/sandbox/execute
```

```
DEPENDENCY: Volume 2 needs SelfModifier.propose_improvement() from Volume 4
STATUS: pending
INTERFACE: async propose_improvement(title, description, changes, progress_callback) -> ImprovementProposal
```

```
DEPENDENCY: Volume 3 needs proposal outcomes from Volume 4
STATUS: pending
INTERFACE: ImprovementProposal with status, risk_assessment, ValidationClaim records in L4
```

---

## Conflict Flags (Agent-Registered)

```
CONFLICT: Verification schemas ownership
VOLUMES: 1 vs 4
PROPOSED RESOLUTION: Volume 1 owns schemas (data entering memory). Volume 4 owns behavioral interface (sign, verify, claim).
STATUS: open
RESOLUTION: [awaiting gate review]
```

```
CONFLICT: RemediationEngine overlap
VOLUMES: 4 vs 5 vs 9
PROPOSED RESOLUTION: RemediationEngine is self-modification. Should flow through Volume 4 pipeline. Volume 5 owns diagnostics. Volume 4 owns remediation.
STATUS: open
RESOLUTION: [awaiting gate review]
```

---

## Integration Gate Output

The integration gate agent produces its output in `design-bible/gate-output/`. See `DISTILLATION_PROTOCOL.md` Section 3 for details.

**Gate output files:**
- `gate-output/conflict-report.md` — Cross-volume conflicts with resolutions
- `gate-output/shared-contracts.md` — Binding interface contracts for Phase 2
- `gate-output/build-order-refined.md` — Refined build order
- `gate-output/mva-refined.md` — Refined MVA criteria
- `gate-output/quality-flags.md` — Per-volume quality assessment
- `gate-output/final-review.md` — Final review after Phase 2 (created at end)

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial creation — defined ownership claim, dependency declaration, and conflict flag protocols; pre-registered 7 known boundary ownership decisions | Created the shared coordination file so agents working on different subsystems don't step on each other |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-X00-003`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added Integration Gate Output section referencing `gate-output/` directory and 6 output files per DISTILLATION_PROTOCOL.md | Added a section pointing to where the integration agent stores its analysis results |
