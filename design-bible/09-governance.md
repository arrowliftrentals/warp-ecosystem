# ATLAS Design Bible — Volume 9: Governance & Validation

| Field | Value |
|---|---|
| **Doc ID** | `DB-V09-001` |
| **Name** | Volume 9: Governance & Validation |
| **Purpose** | Design specification for the constitutional enforcement layer — intent validation, output governance, and boundary compliance |
| **Owner** | Design Bible / Volume 9 |
| **Status** | `phase-2-complete` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / Distillation Agent V9 (Part B) |
| **Version** | v6 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-11 |

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

**Language & Runtime:** Python 3.11+ (required for `X | None` type hints, per PROJECT_CONVENTIONS.md).

**Libraries:**

| Library | Purpose | Justification |
|---|---|---|
| `pydantic` v2 | Schema validation for GovernedOutput, ExtractedClaim, EvidenceItem, ValidationDecision, ContractResult, EvidenceContract, and all enums | P8 mandate — Pydantic at every boundary. v2 for performance (Rust core). |
| `structlog` | Structured JSON logging | PROJECT_CONVENTIONS.md Section 7. Replaces `loguru` used in Attempt 3. All governance log entries must include `subsystem="governance"` plus operation-specific context. |
| `hashlib` (stdlib) | SHA256 integrity hashing for GovernedOutput.content_sha256 and EvidenceItem.result_sha256 | No external dependency needed. SHA256 used for content tamper detection and evidence provenance. |
| `re` (stdlib) | Regex-based claim extraction and speculation scrubbing | Deterministic, no ML dependency. ClaimExtractor uses 12+ compiled patterns; SpeculationScrubber uses 25+ replacement patterns. Pure regex avoids LLM dependency (P1 alignment). |
| `uuid` (stdlib) | EvidenceItem ID generation | UUID4 for collision-free per-request item IDs. |
| `json` (stdlib) | Evidence blob serialization for hashing and size measurement | Used in EvidenceStore for args hashing, result serialization, and pruning size calculations. |

**Departures from defaults:**
- `dataclass` → `pydantic.BaseModel`: Attempt 3 used `@dataclass` for `ValidationDecision`. The rebuild uses Pydantic `BaseModel` for consistency with P8 and to gain validation, serialization, and `model_config = {"frozen": True}` immutability for all governance output types.
- `loguru` → `structlog`: Per PROJECT_CONVENTIONS.md. All governance modules must replace `from loguru import logger` with `from atlas.shared.logging import log`.

**Storage:** No persistent storage owned by this subsystem. EvidenceStore is ephemeral (per-request, in-memory `dict[str, EvidenceItem]`). EvidenceContractRegistry is loaded from configuration at startup (static contract definitions). If governance audit trails are needed, they are written to L3 (episodic memory) via Volume 1's MemoryManager — Volume 9 does not own a database.

**No ML dependencies:** The entire governance subsystem is deterministic and symbolic. Claim extraction uses regex. Confidence scoring uses arithmetic. Speculation scrubbing uses regex replacements. This is by design — governance cannot depend on the components it governs (P1).

### B.6 Data Model

All governance Pydantic schemas live in `atlas/governance/schemas.py` per C-01 resolution. These schemas are the authoritative definitions — no other volume redefines them.

**Enums:**

`AuthorityLevel(str, Enum)` — Confidence tier for governed output.
- `GROUNDED` — All verifiable claims are SUPPORTED by evidence.
- `ADVISORY` — At least 50% of verifiable claims SUPPORTED, or no verifiable claims present.
- `SPECULATIVE` — Below 50% support ratio, or pipeline error fallback.

`ClaimType(str, Enum)` — Category of factual claim.
- `QUANTITATIVE` — Numbers, counts, percentages, durations.
- `EXISTENCE` — File paths, class names, function names, URLs.
- `LOCATION` — Line numbers, character offsets.
- `PROCEDURE` — Action verbs asserting something was done ("created", "deleted", "passed").
- `CAPABILITY` — Self-referential assertions ("I can", "Atlas supports").
- `CAUSAL` — Cause-effect claims ("because", "due to").
- `POLICY` — Normative language ("must", "should", "required").

`ClaimStatus(str, Enum)` — Verification result for a claim.
- `SUPPORTED` — Claim matched against evidence in EvidenceStore.
- `UNSUPPORTED` — Claim has no matching evidence; will be hedged/downgraded.
- `UNVERIFIABLE` — Initial status before grounding; also for claims that cannot be checked.
- `SUBJECTIVE` — CAPABILITY, CAUSAL, POLICY claims that are opinion-like; excluded from support ratio.

`OutputPhase(str, Enum)` — Which pipeline phase produced the output.
- `THINK` — Internal reasoning (never shown to user).
- `OBSERVE_SUMMARY` — Tool result summary.
- `REFLECT` — Self-critique phase.
- `ANSWER` — Final user-facing answer.
- `COUNCIL_SYNTHESIS` — Multi-model consensus output.

`ValidationResult(str, Enum)` — Intent validation outcome.
- `SAFE` — Proceed with execution.
- `UNSAFE` — Block execution.
- `NEEDS_REVIEW` — Requires human confirmation.
- `NEEDS_USER_INPUT` — Needs clarification from user.

**Core Schemas:**

`ValidationDecision(BaseModel, frozen=True)` — Result of DecisionValidator.
Fields:
- `result: ValidationResult` — Overall outcome.
- `confidence: float` — Field(ge=0.0, le=1.0). Confidence in the decision.
- `safety_score: float` — Field(ge=0.0, le=1.0). Safety assessment.
- `reasons: list[str]` — Explanations for the decision.
- `suggestions: list[str]` — Alternative actions or clarification requests.
- `blocked_reasons: list[str]` — Specific blocking reasons if UNSAFE/NEEDS_REVIEW.
Methods:
- `is_safe() -> bool` — Returns `result == ValidationResult.SAFE`.
- `needs_user_input() -> bool` — Returns `result in {NEEDS_REVIEW, NEEDS_USER_INPUT}`.
Validation: Confidence and safety_score constrained to [0.0, 1.0] via Field.

`ExtractedClaim(BaseModel)` — A single factual claim extracted from LLM output. Mutable (status updated during grounding/verification).
Fields:
- `text: str` — The claim text as extracted.
- `claim_type: ClaimType` — Classification of the claim.
- `source_span: tuple[int, int]` — Character offsets (start, end) in original content.
- `status: ClaimStatus` — Default UNVERIFIABLE, updated during pipeline.
- `grounding_refs: list[str]` — EvidenceItem IDs supporting this claim. Default empty.
- `verification_method: str` — How verification was performed (e.g., "evidence_file_match", "evidence_number_fuzzy"). Default empty string.
Validation: source_span[0] < source_span[1].

`EvidenceItem(BaseModel, frozen=True)` — Verbatim tool result stored for claim grounding.
Fields:
- `id: str` — UUID4 string.
- `correlation_id: str` — Request scope identifier.
- `tool_name: str` — Which tool produced this (min_length=1).
- `args_hash: str` — SHA256 of serialized tool arguments.
- `result_blob: Any` — Verbatim tool output (any JSON-serializable type).
- `result_sha256: str` — SHA256 of serialized result_blob.
- `timestamp: datetime` — When evidence was stored.
Validation: tool_name cannot be empty.

`GovernedOutput(BaseModel, frozen=True)` — Single egress schema for ALL user-facing text.
Fields:
- `phase: OutputPhase` — Which pipeline phase produced this.
- `authority_level: AuthorityLevel` — Confidence tier.
- `content: str` — Governed text (the ONLY text allowed to reach the user).
- `content_sha256: str` — SHA256 of content for tamper detection.
- `claims: list[ExtractedClaim]` — Extracted and verified claims. Default empty.
- `grounding_refs: list[str]` — All EvidenceItem IDs referenced. Default empty.
- `approval: str` — One of "approved", "revise", "blocked". Constrained via field validator.
- `policy_violations: list[str]` — Contract violation codes. Default empty.
- `governor_latency_ms: float` — Pipeline execution time in milliseconds. Field(ge=0.0).
Class methods:
- `compute_hash(content: str) -> str` — Static. Returns SHA256 hex digest.
Validation: approval must be in {"approved", "revise", "blocked"}. If approval == "blocked", content must not be shown to user (enforced by consumer, documented in contract).

`EvidenceContract(BaseModel, frozen=True)` — Defines required evidence for an intent pattern.
Fields:
- `intent_pattern: str` — Regex pattern matched against user queries.
- `required_evidence: list[str]` — Evidence types that must be present.
- `required_tools: list[str]` — Tools that must have been called (any-of match).
- `failure_action: str` — One of "block_answer", "flag_insufficient", "inject_disclaimer". Constrained via Literal type.

`ContractResult(BaseModel)` — Result of checking query against EvidenceContracts.
Fields:
- `satisfied: bool` — Whether all matched contracts are satisfied. Default True.
- `violated_contracts: list[str]` — Intent patterns of violated contracts. Default empty.
- `missing_evidence: list[str]` — Evidence types not found. Default empty.
- `missing_tools: list[str]` — Tools not called. Default empty.
- `recommended_action: Literal["block_answer", "flag_insufficient", "inject_disclaimer", "none"]` — Strictest failure action. Default "none".

**Cross-subsystem schema notes:**
- `GovernedOutput` is consumed by Volume 2 (orchestrator response path), Volume 6 (voice output), Volume 7 (console display), and Volume 8 (API response serialization).
- `ValidationDecision` is consumed by Volume 2 (intent routing) and Volume 4 (self-modification approval).
- `EvidenceItem` is produced by Volume 2 (after tool execution in ReAct loop) and consumed by Volume 9 (AnswerGovernor grounding).

### B.7 Error Handling

All governance errors inherit from the shared hierarchy in `atlas/shared/errors.py` per P5 and PROJECT_CONVENTIONS.md Section 6.

**Error types owned by Volume 9:**

`GovernanceViolation(AtlasError)` — A governance rule was violated. Blocks execution.
- Raised when: DecisionValidator returns UNSAFE and `allow_override=False`; AnswerGovernor produces `approval="blocked"`; EvidenceContract check fails with `failure_action="block_answer"`.
- Fields: `rule: str` (which governance rule), `violation_detail: str`, `suggested_action: str`.
- Propagation: Raised to caller (Volume 2 orchestrator). Never swallowed. The orchestrator must either block the operation or present the violation to the user.

`ValidationError(AtlasError)` — Pydantic schema validation failed on governance input/output.
- Raised when: GovernedOutput, ValidationDecision, EvidenceItem, or ContractResult fails Pydantic validation.
- Propagation: Raised immediately. Indicates a programming error (malformed data), not a user error.

**Error handling patterns in governance modules:**

1. **AnswerGovernor.govern()**: Pipeline errors (claim extraction failure, grounding failure) are caught, logged with `log.warning("pipeline_error", ...)`, and the governor falls back to `AuthorityLevel.SPECULATIVE` with empty claims. The output is still governed (it passes through GovernedOutput schema) but at reduced authority. This is a degraded-but-safe pattern, not silent failure.

2. **DecisionValidator**: Never raises on valid input. Returns `ValidationDecision(result=UNSAFE, ...)` as the fail-safe default for unrecognized patterns. Invalid input (None command, empty dict) raises `ValidationError`.

3. **EvidenceStore.store()**: Raises `ValueError` if `tool_name` is empty. Truncation of oversized results (>256KB) is logged as warning but does not raise — the truncated result is still stored. Pruning of oldest items is logged as debug.

4. **EvidenceContractRegistry.check()**: Returns `ContractResult(satisfied=True)` for empty queries (fail-open for non-queries). Contract compilation errors (invalid regex in intent_pattern) raise at registry initialization, not at check time.

5. **ClaimExtractor.extract_claims()**: Returns empty list for empty content. Regex compilation happens at module load time; pattern match errors during extraction are logged and the pattern is skipped (individual claim extraction is non-fatal).

**Forbidden patterns (per P5):**
- No `except: pass` anywhere in governance code.
- No bare `except Exception: pass`.
- All exception handlers must log with context: `log.error("event_name", error=str(e), tool_name=..., claim_type=..., ...)`.
- Pipeline fallback (SPECULATIVE) must always be logged so the degradation is visible.

### B.8 Testing Strategy

**Acceptance Tests (MANDATORY — gate deployment per P11):**

All acceptance tests hit the live server. No mocks at governance boundaries.

1. **test_governed_response**: Send `{"query": "How many lines in src/atlas/shared/errors.py?"}` to `POST /v1/atlas/chat`. Verify the response: (a) `governed: true` in ChatResponse, (b) at least one `evidence` entry referencing a file_read tool, (c) any quantitative claim in the response matches the evidence. This proves MVA-2 (evidence-grounded response). If AnswerGovernor is deleted/stubbed, this test fails.

2. **test_ungoverned_blocked**: Temporarily disable AnswerGovernor (if feature-flagged). Send any query. Verify the response either (a) includes `governed: false` with a system warning, or (b) fails with a GovernanceViolation. This proves output governance cannot be silently bypassed.

3. **test_destructive_blocked**: Send `{"query": "delete all files in the project"}` to `POST /v1/atlas/chat`. Verify the response indicates the action was blocked or requires confirmation (ValidationResult.NEEDS_REVIEW or UNSAFE). This proves DecisionValidator is wired into the conversation loop.

4. **test_evidence_round_trip**: In an integration test (not full HTTP), create an EvidenceStore, store a tool result, create an AnswerGovernor, govern a response containing a quantitative claim matching the evidence. Verify the claim has status=SUPPORTED and authority_level=GROUNDED. This proves the grounding pipeline works end-to-end.

5. **test_contract_violation**: Store no evidence. Govern a response to a query matching an EvidenceContract (e.g., "read the file src/main.py"). Verify ContractResult.satisfied is False and the appropriate failure_action is applied. This proves omission detection works.

**Integration Tests:**

6. **test_claim_extraction_coverage**: Feed 20+ representative LLM output strings (containing file paths, line numbers, percentages, action verbs, capability assertions, causal language, policy language). Verify each produces the expected claim types with correct source_span offsets. This regression-tests the regex patterns.

7. **test_speculation_scrubber**: Feed 10+ strings containing speculative language ("likely", "probably", "seems to be", "may be"). Verify all are replaced by assertive equivalents or removed. Verify non-speculative content is unchanged.

8. **test_evidence_pruning**: Store items exceeding MAX_STORE_BYTES (2MB). Verify oldest items are pruned with tombstones. Verify remaining items have intact SHA256 hashes.

9. **test_confidence_model_signals**: Create EvidenceStore with known items. Create claims with known statuses. Compute confidence. Verify the score matches expected value within 0.01 tolerance. Test edge cases: no evidence (score=0.0), all claims supported (score near 1.0).

10. **test_validator_bert_agreement**: Provide matching and mismatching BERT + symbolic intents to DecisionValidator.validate(). Verify confidence boost on agreement and confidence reduction on disagreement.

**Unit Tests:**

11. `test_validation_decision_immutable` — Verify `ValidationDecision` fields cannot be mutated after creation (frozen=True).
12. `test_governed_output_hash_integrity` — Verify `GovernedOutput.compute_hash()` produces consistent SHA256 for same content.
13. `test_evidence_item_empty_tool_name` — Verify `EvidenceStore.store("", ...)` raises ValueError.
14. `test_contract_result_action_severity` — Verify block_answer > flag_insufficient > inject_disclaimer > none ordering.
15. `test_authority_computation` — Verify GROUNDED requires 100% support, ADVISORY ≥50%, SPECULATIVE <50%.

**Regression tests from A.4 failures:**

16. **test_no_raw_llm_to_user**: Instrument the response path. Verify every string reaching the user has passed through GovernedOutput schema validation. This directly addresses A.4 Warning #1 (ungoverned LLM output in Attempt 3 where 4 ReAct call sites had no governance).

### B.9 Configuration

Governance configuration is loaded via `AtlasConfig(BaseSettings)` from `atlas/shared/config.py` with `ATLAS_` prefix per PROJECT_CONVENTIONS.md Section 8.

**Configuration fields (all have safe defaults):**

| Field | Type | Default | Env Var | Description |
|---|---|---|---|---|
| `governance_strict_mode` | `bool` | `True` | `ATLAS_GOVERNANCE_STRICT_MODE` | When True, UNSAFE validations block execution. When False, they log warnings only. |
| `governance_require_confirmation` | `list[str]` | `["destructive_operations", "self_modification", "device_management"]` | `ATLAS_GOVERNANCE_REQUIRE_CONFIRMATION` | Operation categories requiring user confirmation. |
| `governance_allow_override` | `bool` | `True` | `ATLAS_GOVERNANCE_ALLOW_OVERRIDE` | Whether blocked operations can be overridden with user confirmation. |
| `evidence_max_item_bytes` | `int` | `262144` (256KB) | `ATLAS_EVIDENCE_MAX_ITEM_BYTES` | Maximum size per evidence item. Oversized items truncated. |
| `evidence_max_store_bytes` | `int` | `2097152` (2MB) | `ATLAS_EVIDENCE_MAX_STORE_BYTES` | Maximum total evidence per request. Oldest items pruned when exceeded. |
| `evidence_ttl_seconds` | `int` | `1800` (30 min) | `ATLAS_EVIDENCE_TTL_SECONDS` | Time-to-live for evidence items. |
| `confidence_w_coverage` | `float` | `0.4` | `ATLAS_CONFIDENCE_W_COVERAGE` | Weight for evidence coverage signal in ConfidenceModel. |
| `confidence_w_support` | `float` | `0.4` | `ATLAS_CONFIDENCE_W_SUPPORT` | Weight for claim support ratio signal. |
| `confidence_w_freshness` | `float` | `0.2` | `ATLAS_CONFIDENCE_W_FRESHNESS` | Weight for evidence freshness signal. |
| `grounded_threshold` | `float` | `1.0` | `ATLAS_GROUNDED_THRESHOLD` | Support ratio required for GROUNDED authority level. |
| `advisory_threshold` | `float` | `0.5` | `ATLAS_ADVISORY_THRESHOLD` | Minimum support ratio for ADVISORY (below = SPECULATIVE). |
| `enable_evidence_contracts` | `bool` | `False` | `ATLAS_ENABLE_EVIDENCE_CONTRACTS` | Feature flag for EvidenceContractRegistry. Off for Tier 0-1; enabled at Tier 2. |
| `enable_confidence_model` | `bool` | `False` | `ATLAS_ENABLE_CONFIDENCE_MODEL` | Feature flag for ConfidenceModel. Off for Tier 0; enabled at Tier 1. |

**Loading order:** Environment variables → `.env` file → defaults. Per `pydantic-settings` convention.

**Feature flag discipline (per A.4 Warning #2):** `enable_evidence_contracts` and `enable_confidence_model` default to `False`. Unlike Attempt 3 where ALL flags were False and capabilities were dead code, the rebuild requires that any feature with its flag set to `True` must have a passing acceptance test. Flags are turned on only when the acceptance test passes.

### B.10 Subsystem Lessons Learned

**10.1: ResponseValidator was correctly superseded but its failure pattern is instructive.** `response_validator.py` (424 lines) tried to fact-check LLM responses by querying system state at validation time (e.g., calling `self.atlas.memory.l1.get_stats()` to verify a memory claim). This created tight coupling to the Atlas instance, required runtime access to subsystems during validation, and could not verify claims about tool results that already happened. AnswerGovernor's evidence-based approach (store evidence during execution, verify claims against stored evidence) is fundamentally better because it decouples governance from runtime subsystem access.

**10.2: Speculation scrubber regex ordering matters.** The 25+ regex patterns in `_SPECULATION_REPLACEMENTS` are ordered by specificity (longer/more-specific patterns first). In Attempt 3, a reordering bug briefly caused "most likely due to" to be partially matched by the simpler "likely" pattern, producing garbled output ("most due to"). The rebuild must preserve pattern ordering and test it with regression cases.

**10.3: ValidationDecision was a dataclass, not Pydantic.** Attempt 3 used `@dataclass` for `ValidationDecision` while all other governance schemas used Pydantic. This inconsistency meant ValidationDecision lacked field-level validation (confidence could be negative, safety_score could exceed 1.0). The rebuild uses Pydantic for all governance schemas uniformly.

**10.4: DecisionValidator's validate() signature was overloaded.** The method accepted `bert_result`, `symbolic_intent`, `command`, and `context` — all optional. In practice, different callers used different subsets, making the interface unclear. The rebuild should provide focused methods: `validate_command(command, classification)` for user commands, `validate_tool(tool_name, args)` for tool execution, and `validate_llm_action(suggestion, original_command)` for LLM governance. The generic `validate()` becomes a router.

**10.5: EvidenceStore pruning was lossy.** Oldest-first pruning deleted evidence items needed for claim verification. The tombstone mechanism preserved SHA256 hashes but not the evidence content. If a claim references a pruned item, verification fails silently (claim stays UNSUPPORTED rather than raising an error). The rebuild should log a warning when a referenced item is pruned and consider LRU-based pruning instead of oldest-first.

**10.6: Evidence contracts used any-of matching for required_tools.** A contract requiring `["file_read", "code_execution"]` was satisfied if ANY of those tools was called, not ALL. This is too permissive for contracts like "run tests" which should require code_execution evidence specifically. The rebuild should support both `any_of` and `all_of` matching modes per contract.

### B.11 Discoveries

**11.1: Speculation scrubbing is a system-wide concern, not just governance.** The `_scrub_speculation` pattern (deterministic regex replacements removing hedging language like "likely", "probably", "seems to be") is applicable to ALL LLM-generated text in the system, not just user-facing answers. LLM-generated commit messages, proposal descriptions, error explanations, and learning summaries all contain speculative language that should be scrubbed. Candidate for promotion to Volume 0 as a shared utility in `atlas/shared/text.py`.

**11.2: Evidence contracts create an implicit tool dependency graph.** EvidenceContracts map intent patterns to required tools. This means the contract registry implicitly defines which tools the system MUST have for each capability. If a tool is removed or renamed, contracts break silently. The rebuild should validate contracts against the tool registry at startup and warn about contracts referencing non-existent tools.

**11.3: `<think>` tag stripping belongs in governance, not in the LLM provider.** AnswerGovernor strips `<think>…</think>`, `<reasoning>…</reasoning>`, and similar internal monologue tags from LLM output before governance. This is correct — the governance layer is the last checkpoint before user delivery, so it must guarantee no internal reasoning leaks. If stripping were in the LLM provider, it could be bypassed by direct LLM calls from other subsystems.

**11.4: memory_guard.py is assigned to Volume 9 per C-06.** The conflict report assigns memory write validation to Volume 9. This means DecisionValidator (or a sibling `MemoryWriteValidator`) should validate data before it enters memory layers. This is a new responsibility not present in Attempt 3's governance subsystem and must be designed in the rebuild. The interface: `validate_memory_write(layer_id: str, data: BaseModel) -> ValidationDecision`.

**Tier 2+ Stub Design — MemoryWriteValidator:**

```python
# Location: src/atlas/governance/memory_guard.py
# Owner: Vol 9 (Governance) per C-06
# Tier: 2+ (after core governance proven at Tier 0-1)

from pydantic import BaseModel
from atlas.governance.schemas import ValidationDecision
from atlas.shared.types import LayerId

class MemoryWritePolicy(BaseModel):
    """Per-layer write policy. Loaded from config."""
    layer_id: LayerId
    max_item_bytes: int = 262144  # 256KB
    require_schema_validation: bool = True
    allowed_writers: list[str] = ["orchestrator", "learning", "self_modification"]

class MemoryWriteValidator:
    """Validates data before it enters memory layers.

    Responsibilities:
    - Schema conformance (data matches layer's Pydantic model)
    - Size bounds (reject oversized writes)
    - Writer authorization (only allowed subsystems write to each layer)
    - Content safety (no raw LLM output to persistent layers without governance)
    """

    def __init__(self, policies: list[MemoryWritePolicy]) -> None: ...

    def validate_memory_write(
        self,
        layer_id: LayerId,
        data: BaseModel,
        writer: str,
    ) -> ValidationDecision:
        """Validate a proposed memory write.

        Args:
            layer_id: Target memory layer (e.g. 'l3', 'l9').
            data: The Pydantic model being written.
            writer: Subsystem identifier requesting the write.

        Returns:
            ValidationDecision with SAFE/NEEDS_REVIEW/UNSAFE.
        """
        ...
```

**Integration point:** Vol 1 MemoryManager calls `validate_memory_write()` before persisting to any layer. Wired at Tier 2 when `enable_memory_guard` config flag is True.

### B.12 Oversight Self-Review

**Q1: Does the design address every item in A.4 (Known Failures & Warnings)?**

- **A.4 #1 (ADR-0031 is the blueprint):** Addressed. B.1 defines the full AnswerGovernor pipeline (extract → ground → verify → downgrade → scrub → emit). B.4 rebuilds the 7 core components. B.5 specifies the technology. B.6 defines all schemas. B.8 includes acceptance test `test_governed_response` that proves MVA-2. The graduated approach defers ConfidenceModel and EvidenceContracts to later tiers while shipping core governance at Tier 0.

- **A.4 #2 (Graduated governance):** Addressed. B.1 explicitly defines the graduation strategy: Tier 0-1 = 3 hard rules (GovernedOutput, DecisionValidator, EvidenceStore), Tier 2-3 = evidence contracts + confidence thresholds, Tier 4+ = PolicyEngine. B.9 uses feature flags (`enable_evidence_contracts`, `enable_confidence_model`) that default to False. B.10.4 identifies the over-governance risk in the DecisionValidator signature.

- **A.4 #3 (Voice governance as template — coordinate with Vol 6):** Addressed. B.4 KILLs `voice/governance.py` (item 11). GovernedOutput supersedes ApprovedUtterance per C-14 resolution (shared-contracts.md Section 1.2). Vol 6 consumes GovernedOutput, not a parallel governance path.

- **A.4 #4 (DecisionValidator scope):** Addressed. B.1 defines DecisionValidator as the validation gate for intents, tool executions, LLM actions, and external data. B.2 shows it as the entry point in the governance data flow. B.10.4 identifies the signature overload problem and proposes focused methods. B.11.4 notes the new memory_guard responsibility from C-06.

**Q2: Are there cross-volume interface mismatches with shared-contracts.md?**

Verified against shared-contracts.md:
- Section 1.2 (Governance Schemas): All 9 types listed match B.6 definitions. Location `atlas/governance/schemas.py` matches.
- Section 2.3 (Vol 2 → Vol 9): `DecisionValidator.validate()`, `validate_intent()`, `validate_tool_execution()`, `AnswerGovernor.govern()` signatures match B.3 contracts.
- Section 2.7 (Vol 9 → Vol 2): `EvidenceStore.store()` signature matches B.3 Contract 3.
- Section 2.10 (Vol 4 → Vol 9): `DecisionValidator.validate_intent()` matches B.3.
- Section 3 (Memory Layer Interface): Vol 9 accesses L4 for fact search for evidence grounding — matches B.3 Dependency 1.
No mismatches found.

**Q3: Does the design violate any Volume 0 principle?**

- P1 (ML advises, symbolic decides): Compliant. AnswerGovernor is purely symbolic. DecisionValidator uses BERT results as advisory input, never executes based on them alone.
- P4 (Validation must be real): Compliant. All validation produces `ValidationDecision` or `GovernedOutput` with auditable fields. No stub health checks.
- P5 (Silent failure is a system fault): Compliant. B.7 forbids `except: pass`. Pipeline fallback logs warning and degrades to SPECULATIVE.
- P8 (Pydantic at boundaries): Compliant. Every schema in B.6 is Pydantic.
- P9 (Output governance): The entire subsystem exists to enforce this.
- P11 (Acceptance tests gate everything): B.8 defines 5 acceptance tests.

No violations found.

**Q4: Are there components in A.2 that are not addressed in B.4-B.10?**

All 12 A.2 files have verdicts in B.4: 7 REBUILD, 2 DEFER, 3 KILL. All REBUILD components have technology choices (B.5), data models (B.6), error handling (B.7), testing (B.8), and configuration (B.9) coverage. DEFERred components (failure_prevention_validator, policy_engine) are explicitly scoped to Tier 4-5+ with dependencies stated. KILLed components (response_validator, voice/governance, enforcement_*) have kill rationale documented.

**Q5: Are any B.4 verdicts changed from Phase 1?**

No B.4 verdicts are changed. All 7 REBUILD, 2 DEFER, 3 KILL decisions from Phase 1 are retained.

**Q6: What is missing or incomplete?**

Identified gap: **memory_guard.py is assigned to Vol 9 by C-06 but not in the A.2 source manifest.** This means the rebuild has a new responsibility (memory write validation) that was not analyzed in Phase 1. B.11.4 documents this discovery. The programming agent must design `validate_memory_write()` from scratch — there is no Attempt 3 implementation to distill from within Vol 9's files. The closest reference is `src/learning/memory_guard.py` (owned by Vol 3, which KILLed it). Recommended: add this as a Tier 2+ feature after core governance is proven.

Additional gap: **OperationalDiagnostician assigned to Vol 9 by C-08** for health truthfulness checking. This component lives in `src/intelligence/` (Vol 5's manifest) and was DEFERred by Vol 5. The rebuild should incorporate health truthfulness validation into DecisionValidator as a Tier 4+ feature, not as a separate component.

### B.13 Design Quality Scorecard

| # | Criterion | Score (1-5) | Justification |
|---|---|---|---|
| 1 | Volume 0 Alignment | 5 | Every principle (P1, P4, P5, P8, P9, P11) explicitly addressed with specific design decisions. Graduated governance (L4) is the core strategy. |
| 2 | Interface Completeness | 4 | 5 provided contracts, 3 consumed dependencies fully specified with signatures. Memory write validation (C-06) is identified but deferred. |
| 3 | Scope Clarity | 5 | 7 REBUILD / 2 DEFER / 3 KILL with clear rationale for each. Enforcement files correctly reassigned to Vol 4. |
| 4 | Data Model Rigor | 5 | All schemas defined with field types, constraints, defaults, validation rules, and cross-volume consumption notes. Enums exhaustively listed. |
| 5 | Error Handling | 4 | GovernanceViolation and ValidationError defined. All error patterns documented. Pipeline fallback is safe (SPECULATIVE). One gap: pruning-loss warning not formally specified. |
| 6 | Testing Coverage | 5 | 5 acceptance tests covering MVA-2, bypass prevention, destructive blocking, grounding, and contracts. 5 integration tests. 5 unit tests. 1 regression test for A.4 #1. |
| 7 | Configuration Design | 4 | 13 configuration fields with safe defaults and env var mapping. Feature flags with acceptance-test discipline. Gap: no runtime configuration reload. |
| 8 | Lessons Specificity | 5 | 6 specific lessons from actual source code analysis (ResponseValidator failure, regex ordering, dataclass inconsistency, overloaded signature, lossy pruning, contract matching). |
| 9 | Discovery Value | 4 | 4 discoveries: speculation scrubbing as system-wide utility, contract-tool dependency graph, think-tag governance placement, memory_guard assignment. Speculation scrubbing is promotable to Vol 0. |

**Total: 41/45** (Passing threshold: 30/45)

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (8 governance files, 14+ docs including ADR-0031), context brief, and 4 known failure warnings including ungoverned LLM output and graduated governance balance | Created the governance/validation analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V09-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 Source Manifest per DISTILLATION_PROTOCOL.md Section 5 | Labeled which files agents should read in full vs. skim during Phase 1 |
| v5 | 2026-03-10 | Distillation Agent V9 | Phase 1: Filled B.1-B.4 — subsystem purpose (3 responsibilities: intent validation, output governance, evidence grounding), architecture overview (DecisionValidator → AnswerGovernor → GovernedOutput pipeline), interface contracts (5 provided, 3 consumed), scope triage (7 REBUILD / 2 DEFER / 3 KILL) | Agent analyzed all 12 governance source files and wrote the design specification for what to rebuild, what to defer, and what to remove |
|| v6 | 2026-03-11 | Distillation Agent V9 (Phase 2) | Phase 2: Filled B.5-B.13 — technology choices (Pydantic v2 + structlog + stdlib, no ML), data model (6 schemas + 5 enums with full field specs), error handling (GovernanceViolation + 5 module patterns), testing (5 acceptance + 5 integration + 5 unit + 1 regression), configuration (13 fields), 6 lessons, 4 discoveries, self-review (all A.4 items addressed, 2 gaps identified), scorecard 41/45 | Deep-dive agent completed the full design spec for governance subsystem |
