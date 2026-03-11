# Agent Communication — Volume 9: Governance & Validation
## Phase 2 Distillation Outputs

---

## Ownership Claims

\`\`\`
CLAIM: Governance-domain Pydantic schemas (GovernedOutput, ExtractedClaim, EvidenceItem, EvidenceContract, ContractResult, ValidationDecision, plus enums)
OWNER: Volume 9
REASON: Per AGENT_COMM.md pre-registered boundary and C-01 resolution
CONTESTED: no (resolved by C-01, C-14)
\`\`\`

\`\`\`
CLAIM: DecisionValidator (intent validation, tool execution validation, LLM action validation)
OWNER: Volume 9
REASON: Per AGENT_COMM.md pre-registered IntentValidation boundary
CONTESTED: no
\`\`\`

\`\`\`
CLAIM: AnswerGovernor (extract-ground-verify-downgrade-scrub-emit pipeline)
OWNER: Volume 9
REASON: Per AGENT_COMM.md pre-registered OutputGovernance boundary
CONTESTED: no
\`\`\`

\`\`\`
CLAIM: EvidenceStore (per-request ephemeral evidence storage with SHA256 integrity)
OWNER: Volume 9
CONTESTED: no
\`\`\`

\`\`\`
CLAIM: EvidenceContractRegistry (intent-pattern to required-evidence mapping)
OWNER: Volume 9
CONTESTED: no
\`\`\`

\`\`\`
CLAIM: ConfidenceModel (3-signal weighted confidence scoring)
OWNER: Volume 9
CONTESTED: no
\`\`\`

\`\`\`
CLAIM: ClaimExtractor (regex-based 7-type factual claim extraction)
OWNER: Volume 9
CONTESTED: no
\`\`\`

\`\`\`
CLAIM: SpeculationScrubber (deterministic regex replacement of hedging language)
OWNER: Volume 9 (candidate for promotion to Volume 0)
CONTESTED: no
\`\`\`

---

## Dependency Declarations

\`\`\`
DEPENDENCY: Volume 9 needs AtlasError base class from shared/errors.py (Volume 8)
STATUS: pending
\`\`\`

\`\`\`
DEPENDENCY: Volume 9 needs AtlasConfig from shared/config.py (Volume 8)
STATUS: pending
\`\`\`

\`\`\`
DEPENDENCY: Volume 9 needs structlog from shared/logging.py
STATUS: pending
\`\`\`

\`\`\`
DEPENDENCY: Volume 9 needs tool execution results from Volume 2
STATUS: pending
\`\`\`

\`\`\`
DEPENDENCY: Volume 9 needs BERT classification from Volume 2
STATUS: pending
\`\`\`

\`\`\`
DEPENDENCY: Volume 9 needs L4 fact search from Volume 1
STATUS: pending
\`\`\`

---

## Conflict Flags

\`\`\`
CONFLICT: memory_guard.py assigned to Volume 9 by C-06 but not in A.2 source manifest
SEVERITY: medium
AFFECTED VOLUMES: Vol 1, Vol 3
\`\`\`

\`\`\`
CONFLICT: OperationalDiagnostician assigned to Volume 9 by C-08 for health truthfulness
SEVERITY: low
AFFECTED VOLUMES: Vol 5
\`\`\`

---

## Modification History

| Version | Date | Modified By | Summary |
|---|---|---|---|
| v1 | 2026-03-11 | Distillation Agent V9 (Phase 2) | Initial creation — 8 ownership claims, 6 dependency declarations, 2 conflict flags |
