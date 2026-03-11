# Agent Communication — Volume 9: Governance & Validation
## Phase 2 Distillation Outputs

---

## Ownership Claims

```
CLAIM: Governance-domain Pydantic schemas (GovernedOutput, ExtractedClaim, EvidenceItem, EvidenceContract, ContractResult, ValidationDecision, plus enums AuthorityLevel, ClaimType, ClaimStatus, OutputPhase, ValidationResult)
OWNER: Volume 9
REASON: Per AGENT_COMM.md pre-registered boundary and C-01 resolution. All governance schemas consolidated in atlas/governance/schemas.py. Moved from Vol 1 and Vol 6 per conflict resolution.
CONTESTED: no (resolved by C-01, C-14)
```

```
CLAIM: DecisionValidator (intent validation, tool execution validation, LLM action validation)
OWNER: Volume 9
REASON: Per AGENT_COMM.md pre-registered IntentValidation boundary. DecisionValidator is the single validation gate for all intents entering the system, all tool executions, and all LLM-suggested actions.
CONTESTED: no
```

```
CLAIM: AnswerGovernor (extract → ground → verify → downgrade → scrub → emit pipeline)
OWNER: Volume 9
REASON: Per AGENT_COMM.md pre-registered OutputGovernance boundary. AnswerGovernor is the sole output governance component — supersedes ResponseValidator (KILLed) and voice/governance.py (KILLed per C-14).
CONTESTED: no
```

```
CLAIM: EvidenceStore (per-request ephemeral evidence storage with SHA256 integrity)
OWNER: Volume 9
REASON: Stores verbatim tool results for claim grounding. Consumed by AnswerGovernor. Vol 2 calls store() after tool execution; Vol 9 owns the store implementation and pruning logic.
CONTESTED: no
```

```
CLAIM: EvidenceContractRegistry (intent-pattern → required-evidence mapping)
OWNER: Volume 9
REASON: Defines and checks evidence contracts — which tool evidence is required for which intent patterns. Feature-flagged to Tier 2+.
CONTESTED: no
```

```
CLAIM: ConfidenceModel (3-signal weighted confidence scoring)
OWNER: Volume 9
REASON: Computes confidence from evidence coverage, claim support ratio, and evidence freshness. Feature-flagged to Tier 1+.
CONTESTED: no
```

```
CLAIM: ClaimExtractor (regex-based 7-type factual claim extraction)
OWNER: Volume 9
REASON: Extracts QUANTITATIVE, EXISTENCE, LOCATION, PROCEDURE, CAPABILITY, CAUSAL, and POLICY claims from LLM output. Used by AnswerGovernor grounding pipeline.
CONTESTED: no
```

```
CLAIM: SpeculationScrubber (deterministic regex replacement of hedging language)
OWNER: Volume 9 (candidate for promotion to Volume 0)
REASON: 25+ ordered regex patterns removing "likely", "probably", "seems to be" and similar speculative language. Currently in AnswerGovernor; B.11.1 recommends promotion to atlas/shared/text.py.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 9 (Governance) needs AtlasError base class from shared/errors.py (Volume 8)
STATUS: pending
INTERFACE: class AtlasError(Exception) with subsystem, context, severity fields. GovernanceViolation and ValidationError inherit from it.
```

```
DEPENDENCY: Volume 9 (Governance) needs AtlasConfig from shared/config.py (Volume 8)
STATUS: pending
INTERFACE: AtlasConfig(BaseSettings) with env_prefix="ATLAS_". Governance reads 13 configuration fields specified in B.9 (governance_strict_mode, evidence_max_item_bytes, confidence weights, thresholds, feature flags, etc.).
```

```
DEPENDENCY: Volume 9 (Governance) needs structlog configured logging from shared/logging.py (cross-cutting)
STATUS: pending
INTERFACE: from atlas.shared.logging import get_logger -> structlog.BoundLogger. All governance log entries must include subsystem="governance".
```

```
DEPENDENCY: Volume 9 (Governance) needs tool execution results from Volume 2 (Orchestrator)
STATUS: pending
INTERFACE: Volume 2 calls EvidenceStore.store(tool_name: str, args: dict, result: Any, correlation_id: str) after each tool execution in the ReAct loop. Vol 9 does not invoke tools — it receives evidence passively.
```

```
DEPENDENCY: Volume 9 (Governance) needs BERT classification results from Volume 2 (Orchestrator)
STATUS: pending
INTERFACE: Volume 2 passes bert_result (BERTClassification or None) and symbolic_intent to DecisionValidator.validate(). Vol 9 uses these as advisory input, never executes based on BERT alone.
```

```
DEPENDENCY: Volume 9 (Governance) needs L4 fact search from Volume 1 (Memory)
STATUS: pending
INTERFACE: AnswerGovernor may query L4 (factual memory) to verify EXISTENCE and QUANTITATIVE claims against previously stored facts. Interface: MemoryManager.search_facts(query: str) -> list[Fact].
```

---

## Conflict Flags

```
CONFLICT: memory_guard.py assigned to Volume 9 by C-06 but not in A.2 source manifest
SEVERITY: medium
DESCRIPTION: The conflict report (C-06) assigns memory write validation to Volume 9. However, no Attempt 3 implementation exists within Vol 9's source files — src/learning/memory_guard.py was owned by Vol 3 (which KILLed it). Vol 9 must design validate_memory_write(layer_id: str, data: BaseModel) -> ValidationDecision from scratch.
RECOMMENDATION: Add as Tier 2+ feature after core governance is proven. DecisionValidator or a sibling MemoryWriteValidator handles this.
AFFECTED VOLUMES: Vol 1 (memory layers being validated), Vol 3 (original owner of memory_guard.py)
```

```
CONFLICT: OperationalDiagnostician assigned to Volume 9 by C-08 for health truthfulness
SEVERITY: low
DESCRIPTION: C-08 assigns health truthfulness checking to Vol 9. The component lives in src/intelligence/ (Vol 5's manifest) and was DEFERred by Vol 5. Vol 9 should incorporate health truthfulness validation into DecisionValidator as a Tier 4+ feature, not as a separate component.
RECOMMENDATION: Absorb into DecisionValidator.validate_health_report() at Tier 4+.
AFFECTED VOLUMES: Vol 5 (original owner of OperationalDiagnostician)
```

---

## Discoveries for Other Volumes

**For Volume 0:**
- B.11.1: Speculation scrubbing (`_scrub_speculation` — 25+ deterministic regex patterns) is a system-wide concern applicable to ALL LLM-generated text: commit messages, proposal descriptions, error explanations, learning summaries. Candidate for promotion to `atlas/shared/text.py` as a shared utility.

**For Volume 1:**
- B.6 confirms GovernedOutput, ExtractedClaim, EvidenceItem, EvidenceContract, AuthorityLevel, ClaimType, ClaimStatus, OutputPhase schemas are removed from Vol 1's `schemas.py` in the rebuild per C-01. Vol 1 no longer defines these.
- B.11.4: memory_guard.py is assigned to Vol 9 per C-06. Vol 1 should not rebuild this component. If memory write validation is needed before data enters layers, Vol 9's DecisionValidator handles it.

**For Volume 2:**
- AnswerGovernor.govern() is the single governance call after ReAct loop completion. Vol 2 must call `evidence_store.store()` after EVERY tool execution to populate evidence for grounding.
- DecisionValidator.validate() must be called before executing any user intent. Vol 2 passes bert_result and symbolic_intent; if result is UNSAFE, Vol 2 must block execution.

**For Volume 4:**
- DecisionValidator.validate_intent() interface is available for self-modification approval per shared-contracts.md Section 2.10. Vol 4 should use this to gate modification proposals.

**For Volume 5:**
- OperationalDiagnostician health truthfulness is absorbed into Vol 9's DecisionValidator at Tier 4+ per C-08. Vol 5 should not rebuild this component.

**For Volume 6:**
- voice/governance.py is KILLed. GovernedOutput supersedes ApprovedUtterance per C-14. Vol 6 consumes GovernedOutput from Vol 9 — no separate voice governance path.

**For Volume 8:**
- `shared/errors.py` must define AtlasError base class **before** Vol 9 can build GovernanceViolation and ValidationError. This is a Tier 0 dependency.
- `shared/config.py` must define AtlasConfig(BaseSettings) with env_prefix support before Vol 9 can load its 13 governance configuration fields.

---

## Modification History

| Version | Date | Modified By | Summary |
|---|---|---|---|
| v1 | 2026-03-11 | Distillation Agent V9 (Phase 2) | Initial creation — 8 ownership claims, 6 dependency declarations, 2 conflict flags, 8 cross-volume notifications |
