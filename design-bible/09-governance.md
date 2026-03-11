# ATLAS Design Bible — Volume 9: Governance & Validation

| Field | Value |
|---|---|
| **Doc ID** | `DB-V09-001` |
| **Name** | Volume 9: Governance & Validation |
| **Purpose** | Design specification for the constitutional enforcement layer — intent validation, output governance, and boundary compliance |
| **Owner** | Design Bible / Volume 9 |
| **Status** | `draft` (Phase 1 complete — B.1-B.4 filled, B.5-B.13 awaiting Phase 2) |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / Distillation Agent V9 (Part B) |
| **Version** | v5 |
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

Volume 9 is the **constitutional enforcement layer**. It guarantees that Atlas never returns ungoverned output and never executes unvalidated actions. Three core responsibilities:

1. **Intent Validation** — Gate every intent, action, and tool execution before it runs. DecisionValidator is the single validation checkpoint. It validates symbolic intents, BERT classifications, LLM-suggested actions, tool executions, and external data. Produces a `ValidationDecision` with result (SAFE/UNSAFE/NEEDS_REVIEW), confidence, and suggestions.

2. **Output Governance** — Gate every LLM-generated text before it reaches the user. The AnswerGovernor pipeline (ADR-0031) extracts factual claims from LLM output, verifies them against the EvidenceStore (verbatim tool results), downgrades unsupported claims, scrubs speculation, and packages the result as a `GovernedOutput` — the single egress schema for all user-facing text. This directly addresses A.4 Warning #1: all LLM output was previously ungoverned.

3. **Evidence Grounding** — Maintain a verbatim record of all tool results (`EvidenceStore`), score evidence coverage (`ConfidenceModel`), and detect evidence omissions (`EvidenceContractRegistry`). Claims must reference `EvidenceItem` IDs to be GROUNDED. Self-reported LLM confidence is replaced by evidence-based scoring.

**Volume 0 alignment:**
- P1 (ML advises, symbolic decides): AnswerGovernor is the symbolic gate over ML output
- P4 (Validation must be real): DecisionValidator performs real checks, not theater
- P8 (Pydantic at boundaries): GovernedOutput, ExtractedClaim, EvidenceItem, EvidenceContract are all Pydantic schemas
- P9 (Output governance — not just action governance): The entire output governance pipeline exists to satisfy this principle
- L3 (Validation theater is #1 risk): Evidence grounding ensures claims are backed by actual tool results
- L4 (Governance must be graduated): Hard rules (schema validation, evidence grounding) enforced from Tier 0; full constitutional framework (PolicyEngine) deferred to Tier 4+

**Graduated governance strategy (per A.4 Warning #2):**
- **Tier 0-1**: 3 hard rules — (1) All output passes through GovernedOutput schema, (2) All intents pass through DecisionValidator, (3) All claims verified against EvidenceStore
- **Tier 2-3**: Evidence contracts, confidence thresholds, claim downgrading
- **Tier 4+**: Full PolicyEngine with constitutional articles, FailurePreventionValidator

### B.2 Architecture Overview

The governance subsystem has three subsystems with a clear data flow:

```
User Query → [DecisionValidator] → validated intent → Orchestrator
                                                          ↓
                                                    Tool Execution
                                                          ↓
                                                    EvidenceStore ← verbatim tool results
                                                          ↓
                                                    LLM Response
                                                          ↓
                                               [AnswerGovernor.govern()]
                                                    ↓         ↓
                                           ClaimExtractor  EvidenceStore.get_by_tool()
                                                    ↓         ↓
                                               claim verification
                                                    ↓
                                           [ConfidenceModel.compute()]
                                                    ↓
                                            GovernedOutput → User
```

**Subsystem 1: Intent Validation Gate**
- `DecisionValidator` — Single class, 7 validation methods:
  - `validate(command, bert_result)` → `ValidationDecision` — validates user commands against BERT classification
  - `validate_llm_action(suggested_cmd, original_cmd, context)` → `ValidationDecision` — validates LLM-suggested actions for escalation/destructiveness
  - `validate_intent(intent, context)` → `ValidationDecision` — async, validates parsed intents
  - `validate_external_data(data, source)` → `ValidationDecision` — async, validates external data
  - `validate_tool_execution(tool_name, args, context)` → `ValidationDecision` — validates tool calls with per-tool rules
  - `_check_destructive_keywords(command)` — destructive keyword scanning
  - `_validate_symbolic_intent(intent)` — symbolic intent structure validation
- `ValidationResult` enum: SAFE, UNSAFE, NEEDS_REVIEW, NEEDS_USER_INPUT
- `ValidationDecision` dataclass: result, confidence, reason, suggestions, is_safe(), needs_user_input()

**Subsystem 2: Output Governance Pipeline (ADR-0031)**
- `AnswerGovernor.govern(content, phase, evidence_store)` → `GovernedOutput` — the master pipeline:
  1. Extract claims via `ClaimExtractor.extract_claims(content)` → `list[ExtractedClaim]`
  2. Ground claims against EvidenceStore via `_ground_claims()` / `_verify_claims()`
  3. Downgrade unsupported claims via `_downgrade_unsupported()`
  4. Scrub speculation via `_scrub_speculation()`
  5. Compute authority level via `_compute_authority(claims)` → `AuthorityLevel`
  6. Package as `GovernedOutput` with SHA256 integrity hash
- `ClaimExtractor` — regex-based extraction of 7 claim types (EXISTENCE, LOCATION, QUANTITATIVE, PROCEDURE, CAPABILITY, CAUSAL, POLICY)
- Per-type verification functions: `_verify_existence()`, `_verify_location()`, `_verify_procedure()`, `_verify_quantitative()`

**Subsystem 3: Evidence Grounding**
- `EvidenceStore` — per-request store of verbatim tool results:
  - `store(tool_name, args, result)` → `EvidenceItem` — stores with SHA256 integrity
  - `get(evidence_id)` / `get_by_tool(tool_name)` — retrieval
  - `get_index(token_budget)` — compressed index for LLM context
  - Auto-pruning when size exceeds budget
- `ConfidenceModel.compute(claims, evidence_store)` → `float` — evidence-based confidence:
  - `_evidence_coverage()` — ratio of grounded claims
  - `_claim_support_ratio()` — SUPPORTED vs total claims
  - `_evidence_freshness()` — recency of evidence
- `EvidenceContractRegistry.check(query, evidence_store)` → `ContractResult` — omission detection:
  - Matches query against intent patterns
  - Checks required tools were called
  - Returns missing evidence list with failure action (block/flag/disclaimer)

**Key Pydantic schemas** (currently in `src/memory/schemas.py`, governance-specific):
- `GovernedOutput` — single egress schema, fields: phase, authority_level, content, content_sha256, claims, grounding_refs, approval (approved/revise/blocked), policy_violations, governor_latency_ms
- `ExtractedClaim` — fields: text, claim_type, source_span, status, grounding_refs, verification_method
- `EvidenceItem` — fields: id, correlation_id, tool_name, args_hash, result_blob, result_sha256, timestamp, span_index
- `EvidenceContract` — fields: intent_pattern, required_evidence, required_tools, failure_action
- `AuthorityLevel` enum: GROUNDED, ADVISORY, SPECULATIVE
- `ClaimType` enum: QUANTITATIVE, EXISTENCE, CAPABILITY, CAUSAL, LOCATION, PROCEDURE, POLICY
- `ClaimStatus` enum: SUPPORTED, UNSUPPORTED, UNVERIFIABLE, SUBJECTIVE
- `OutputPhase` enum: THINK, OBSERVE_SUMMARY, REFLECT, ANSWER, COUNCIL_SYNTHESIS

### B.3 Interface Contracts

#### 3.1 Interfaces PROVIDED by Volume 9 (consumed by other volumes)

**Contract 1: Intent Validation Gate**
- **Consumer:** Volume 2 (Orchestrator), Volume 4 (Self-Modification)
- **Interface:** `DecisionValidator.validate(command: str, bert_result) → ValidationDecision`
- **Also:** `validate_intent(intent, context)`, `validate_tool_execution(tool_name, args, context)`, `validate_llm_action(suggested_cmd, original_cmd, context)`, `validate_external_data(data, source)`
- **Contract:** Returns `ValidationDecision` with `result` in {SAFE, UNSAFE, NEEDS_REVIEW, NEEDS_USER_INPUT}, `confidence: float`, `reason: str`, `suggestions: list[str]`
- **Guarantee:** Every call returns a decision; never raises on valid input; UNSAFE is the default for unrecognized patterns

**Contract 2: Output Governance Pipeline**
- **Consumer:** Volume 2 (Orchestrator) — must call before returning any LLM text to user
- **Interface:** `AnswerGovernor.govern(content: str, phase: OutputPhase, evidence_store: EvidenceStore) → GovernedOutput`
- **Contract:** Returns `GovernedOutput` with `approval` in {approved, revise, blocked}, `authority_level` in {GROUNDED, ADVISORY, SPECULATIVE}, claim list with verification status, SHA256 integrity hash
- **Guarantee:** Content is never modified silently — changes tracked via claims and approval status; blocked output must not be shown to user

**Contract 3: Evidence Storage**
- **Consumer:** Volume 2 (Orchestrator) — stores tool results during ReAct loop
- **Interface:** `EvidenceStore(correlation_id: str)` — per-request instance
  - `.store(tool_name: str, args: dict, result: Any) → EvidenceItem`
  - `.get(evidence_id: str) → Optional[EvidenceItem]`
  - `.get_by_tool(tool_name: str) → list[EvidenceItem]`
  - `.get_index(token_budget: int) → str`
- **Contract:** Verbatim storage with SHA256 integrity; auto-prunes oldest items when over budget

**Contract 4: Confidence Scoring**
- **Consumer:** Volume 2 (Orchestrator), Volume 9 internal (AnswerGovernor)
- **Interface:** `ConfidenceModel.compute(claims: list[ExtractedClaim], evidence_store: EvidenceStore) → float`
- **Contract:** Returns 0.0-1.0 score based on evidence coverage, claim support ratio, and evidence freshness. Replaces self-reported LLM confidence.

**Contract 5: Evidence Contract Registry**
- **Consumer:** Volume 9 internal (AnswerGovernor)
- **Interface:** `EvidenceContractRegistry.check(query: str, evidence_store: EvidenceStore) → ContractResult`
- **Contract:** Returns `ContractResult` with satisfied (bool), missing_evidence (list), failure_action (block_answer/flag_insufficient/inject_disclaimer)

#### 3.2 Interfaces CONSUMED by Volume 9 (provided by other volumes)

**Dependency 1: Pydantic Schemas (from Volume 1 Memory)**
- Vol 9 governance schemas (GovernedOutput, ExtractedClaim, EvidenceItem, EvidenceContract, AuthorityLevel, ClaimType, ClaimStatus, OutputPhase) are currently defined in `src/memory/schemas.py` owned by Volume 1
- **Conflict:** These schemas are governance-specific and should move to `governance/schemas.py` in the rebuild. See AGENT_COMM.md conflict flag.

**Dependency 2: Tool Results (from Volume 10 / Volume 2)**
- AnswerGovernor depends on tool results being stored in EvidenceStore before govern() is called
- Volume 2 (Orchestrator) is responsible for calling `EvidenceStore.store()` after each tool execution

**Dependency 3: BERT Classification (from Volume 2)**
- DecisionValidator.validate() accepts `bert_result` from BERT intent classifier
- Volume 2 owns the BERT pipeline; Volume 9 consumes the classification result

### B.4 Scope Triage

Every component from A.2 receives a verdict. Rebuild target paths assume a `governance/` package in the rebuilt project.

#### REBUILD (7 components) — Include in initial rebuild

**1. `src/intent/decision_validator.py` → `governance/validator.py`**
- Verdict: **REBUILD**
- Rationale: Core validation gate, directly implements P1 and P4. 7 validation methods, well-structured. Remove BERT-specific coupling (accept generic classification result), clean up 600+ line file into focused validator.
- Rebuild priority: Tier 0 (required from first line of code per Vol 0 Section 6)

**2. `src/orchestrator/answer_governor.py` → `governance/output.py`**
- Verdict: **REBUILD**
- Rationale: Implements ADR-0031, directly addresses A.4 Warning #1 (ungoverned output). The govern() pipeline (extract → ground → verify → downgrade → scrub → package) is the most critical new capability. 500+ lines, well-designed.
- Rebuild priority: Tier 0 (P9 requires output governance from day one)

**3. `src/orchestrator/claim_extractor.py` → `governance/claims.py`**
- Verdict: **REBUILD**
- Rationale: Regex-based claim extraction for 7 claim types. Called by AnswerGovernor. 250 lines, pure functions. Extract as standalone module.
- Rebuild priority: Tier 0 (required by AnswerGovernor)

**4. `src/orchestrator/confidence_model.py` → `governance/confidence.py`**
- Verdict: **REBUILD**
- Rationale: Evidence-based confidence scoring replaces self-reported LLM confidence. Three scoring dimensions (coverage, support ratio, freshness). ~200 lines, clean design.
- Rebuild priority: Tier 1 (can use default confidence initially, wire in at Tier 1)

**5. `src/orchestrator/evidence_store.py` → `governance/evidence.py`**
- Verdict: **REBUILD**
- Rationale: Per-request verbatim tool result store with SHA256 integrity. Core dependency for claim verification. ~350 lines with pruning and indexing.
- Rebuild priority: Tier 0 (required by AnswerGovernor for claim grounding)

**6. `src/orchestrator/evidence_contracts.py` → `governance/contracts.py`**
- Verdict: **REBUILD**
- Rationale: Evidence requirement definitions per intent pattern. Omission detection. ~300 lines, well-structured with ContractResult and EvidenceContractRegistry.
- Rebuild priority: Tier 2 (enhancement — core governance works without contracts initially)

**7. Governance Pydantic schemas → `governance/schemas.py`**
- Verdict: **REBUILD**
- Rationale: GovernedOutput, ExtractedClaim, EvidenceItem, EvidenceContract, AuthorityLevel, ClaimType, ClaimStatus, OutputPhase are governance-domain schemas currently co-located in `src/memory/schemas.py`. They should be extracted to a governance-owned schema file. See AGENT_COMM.md conflict flag for coordination with Volume 1.
- Rebuild priority: Tier 0 (schemas required before any governance code)

#### DEFER (2 components) — Not in initial rebuild

**8. `src/intent/failure_prevention_validator.py` → DEFER to Tier 5+**
- Verdict: **DEFER**
- Rationale: Prevents known failure patterns by learning from past failures. Depends on learning pipeline (Volume 3) to supply failure patterns. Cannot function without L3 episodic memory and pattern extraction. Add after Volume 3 is operational.

**9. `src/orchestrator/policy_engine.py` → DEFER to Tier 4+**
- Verdict: **DEFER**
- Rationale: Full constitutional policy enforcement with 10 articles. Per A.4 Warning #2, over-governance killed Attempt 2. Start with 3 hard rules (Tier 0), prove core governance works, then layer PolicyEngine on top. Requires mature governance pipeline to evaluate policies against.

#### KILL (3 components) — Do not rebuild

**10. `src/orchestrator/response_validator.py` → KILL**
- Verdict: **KILL**
- Rationale: Superseded by AnswerGovernor. ResponseValidator was a simpler validation step; AnswerGovernor subsumes its functionality with claim extraction, evidence grounding, and confidence scoring. Keeping both would be redundant.

**11. `src/voice/governance.py` → KILL**
- Verdict: **KILL**
- Rationale: Superseded by GovernedOutput. ApprovedUtterance was the voice-only precursor; GovernedOutput extends the pattern to ALL output modalities. The schemas (AuthorityLevel, UtteranceMode) are already shared. Volume 6 (Voice) should consume GovernedOutput, not maintain a parallel governance path. Coordinate with Volume 6 per A.4 Warning #3.

**12. `src/self_modify/enforcement_orchestrator.py` + `src/self_modify/enforcement_state.py` → KILL (reassign to Volume 4)**
- Verdict: **KILL** from Volume 9 scope
- Rationale: These files implement self-modification enforcement (EnforcementOrchestrator, EnforcementState). Self-modification security belongs to Volume 4 (Self-Modification), not Volume 9 (Governance). Volume 4 already claims SelfModifier pipeline, VerificationTracker, and related enforcement in AGENT_COMM.md. Volume 9 governs the DECISION to allow self-modification (via DecisionValidator); Volume 4 owns the EXECUTION of self-modification enforcement.

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
| v5 | 2026-03-10 | Distillation Agent V9 | Phase 1: Filled B.1-B.4 — subsystem purpose (3 responsibilities: intent validation, output governance, evidence grounding), architecture overview (DecisionValidator → AnswerGovernor → GovernedOutput pipeline), interface contracts (5 provided, 3 consumed), scope triage (7 REBUILD / 2 DEFER / 3 KILL) | Agent analyzed all 12 governance source files and wrote the design specification for what to rebuild, what to defer, and what to remove |
