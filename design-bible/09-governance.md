# ATLAS Design Bible — Volume 9: Governance & Validation

| Field | Value |
|---|---|
| **Doc ID** | `DB-V09-001` |
| **Name** | Volume 9: Governance & Validation |
| **Purpose** | Design specification for the constitutional enforcement layer — intent validation, output governance, and boundary compliance |
| **Owner** | Design Bible / Volume 9 |
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
- **Volume 9: Governance & Validation**
- **Purpose:** The constitutional enforcement layer — validates intents before execution, governs LLM output before it reaches the user, and ensures the system behaves within its defined boundaries.
- **Rebuild phase:** Phase 0-1 (governance is built into the foundation from day one, per Volume 0 Section 6). The 3 hard rules are enforced from the first line of code.

### A.2 Source Manifest

**Code files to read** (paths relative to `atlas/`):

*Intent validation:*
- `src/intent/decision_validator.py` — central validation gate for all intents and actions
- `src/intent/failure_prevention_validator.py` — prevents known failure patterns

*Output governance:*
- `src/orchestrator/answer_governor.py` — governs LLM text output (ADR-0031)
- `src/orchestrator/claim_extractor.py` — extracts factual claims from responses
- `src/orchestrator/confidence_model.py` — evidence-based confidence scoring
- `src/orchestrator/evidence_store.py` — verbatim tool output storage
- `src/orchestrator/evidence_contracts.py` — evidence requirements per intent
- `src/orchestrator/response_validator.py` — response validation

*Voice governance (precursor pattern):*
- `src/voice/governance.py` — ApprovedUtterance, AuthorityLevel schemas

*Constitutional framework:*
- `src/orchestrator/policy_engine.py` — policy enforcement
- `src/self_modify/enforcement_orchestrator.py` — enforcement coordination
- `src/self_modify/enforcement_state.py` — enforcement state tracking

**Documentation to read:**
- `docs/architecture/atlas-constitution-v2.md` — full constitutional framework (10 articles)
- `docs/architecture/atlas-constitution.md` — v1 constitution
- `docs/architecture/decision-validator.md`
- `docs/architecture/answer-governor.md`
- `docs/architecture/claim-extractor.md`
- `docs/architecture/confidence-model.md`
- `docs/architecture/evidence-store.md`
- `docs/architecture/evidence-contracts.md`
- `docs/architecture/response-validator.md`
- `docs/architecture/policy-engine.md`
- `docs/architecture/zero-bypass-enforcement.md`
- `docs/architecture/authority.md`
- `docs/development/constitutional-compliance.md`
- `docs/development/voice-governance-implementation.md`
- `docs/adr/0031-governed-utterance-pipeline.md` — THE critical ADR for this volume
- `docs/adr/0015-validation-enforcement.md`
- `docs/atlas-evolution-pattern.md` — 5-rule safe evolution

**Test files to read:**
- `tests/intent/` (if exists, for decision_validator tests)
- Any tests related to governance/validation

**CORE/PERIPHERAL Classification:** All 12 files are **CORE** (≤40 code files). Read all in full during both Phase 1 and Phase 2.

### A.3 Context Brief

**What worked in Attempt 3:**
- DecisionValidator existed and validated intents
- Voice governance (ApprovedUtterance) had a well-designed schema with AuthorityLevel
- Constitutional framework was ratified (v2) with 10 articles
- 3 hard rules defined (schema validation, test gate, layer separation)

**What failed or was never wired:**
- ADR-0031 identified that ALL LLM text output was ungoverned — the biggest architectural gap
- Constitution was partially enforced — policies existed but enforcement was inconsistent
- 4 LLM call sites in the ReAct loop had no system prompt or governance
- Self-reported confidence (LLM says "0.85") never calibrated against evidence
- Evidence contracts concept designed but implementation unclear

**What was simulated/fake:**
- Some validation claims may have been theater (P4 violation)
- Health checks reported true for stub subsystems (A2, A3)

**Relevant Volume 0 principles:**
- P1: ML advises, symbolic core decides
- P4: Validation must be real
- P8: Pydantic schemas at every boundary
- P9: Output governance — not just action governance
- L3: Validation theater is the #1 risk
- L4: Governance must be graduated
- Section 6: Constitutional governance (3 hard rules, 3 soft rules, 3 aspirational)

### A.4 Known Failures & Warnings
1. **ADR-0031 is the blueprint**: The Governed Utterance Pipeline is the most detailed design document for output governance. It defines GovernedOutput, EvidenceStore, ConfidenceModel, and AnswerGovernor. The distillation agent must determine how much to include in the initial rebuild vs. defer.
2. **Graduated governance**: Volume 0 says start with 3 hard rules. The full constitution (10 articles) is aspirational. Do not over-govern at the start (that's what killed Attempt 2).
3. **Voice governance as template**: ApprovedUtterance/AuthorityLevel from voice was the precursor to GovernedOutput. Coordinate with Volume 6 to avoid duplication.
4. **DecisionValidator scope**: Currently validates intents and tool executions. The rebuild must extend it (or create a sibling) for output governance. Clear boundary needed.

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
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (8 governance files, 14+ docs including ADR-0031), context brief, and 4 known failure warnings including ungoverned LLM output and graduated governance balance | Created the governance/validation analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V09-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 Source Manifest per DISTILLATION_PROTOCOL.md Section 5 | Labeled which files agents should read in full vs. skim during Phase 1 |
