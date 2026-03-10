# Agent Communication — Volume 9: Governance & Validation

> **Rules:** Append new claims/dependencies/conflicts using the formats defined in `AGENT_COMM.md`.
> This file is the ONLY place Vol 9 agents register changes. Do NOT edit `AGENT_COMM.md` directly.

---

## Ownership Claims

```
CLAIM: DecisionValidator (intent/action/tool validation gate)
OWNER: Volume 9
REASON: Central validation checkpoint for all intents, BERT classifications, LLM actions, tool executions, and external data. Produces ValidationDecision (SAFE/UNSAFE/NEEDS_REVIEW/NEEDS_USER_INPUT).
CONTESTED: no
```

```
CLAIM: AnswerGovernor (output governance pipeline, ADR-0031)
OWNER: Volume 9
REASON: Governs all LLM-generated text via extract → ground → verify → downgrade → scrub → package pipeline. Produces GovernedOutput — single egress schema.
CONTESTED: no
```

```
CLAIM: EvidenceStore + EvidenceContractRegistry (evidence grounding)
OWNER: Volume 9
REASON: Per-request verbatim tool result store with SHA256 integrity. EvidenceContractRegistry defines required evidence per intent pattern.
CONTESTED: no
```

```
CLAIM: ConfidenceModel (evidence-based confidence scoring)
OWNER: Volume 9
REASON: Computes confidence from evidence coverage, claim support ratio, and evidence freshness. Replaces self-reported LLM confidence.
CONTESTED: no
```

```
CLAIM: ClaimExtractor (factual claim extraction from LLM output)
OWNER: Volume 9
REASON: Regex-based extraction of 7 claim types (EXISTENCE, LOCATION, QUANTITATIVE, PROCEDURE, CAPABILITY, CAUSAL, POLICY). Called by AnswerGovernor.
CONTESTED: no
```

```
CLAIM: Governance schemas (GovernedOutput, ExtractedClaim, EvidenceItem, EvidenceContract, AuthorityLevel, OutputPhase, ClaimType, ClaimStatus)
OWNER: Volume 9 (currently in src/memory/schemas.py, must move to governance/schemas.py in rebuild)
REASON: Output/voice governance schemas owned by Volume 9 per pre-registered boundary.
CONTESTED: no
```

```
CLAIM: OperationalDiagnostician + InvariantEvaluator (system health truthfulness)
OWNER: Volume 9
REASON: Health truthfulness is fundamentally a governance concern per P4. Moved from Vol 5 per conflict resolution C-08.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 9 needs governance Pydantic schemas extracted from src/memory/schemas.py (Volume 1)
STATUS: pending
INTERFACE: Currently in Vol 1 schemas.py. Vol 9 extracts to governance/schemas.py in rebuild.
```

```
DEPENDENCY: Volume 9 needs tool results stored in EvidenceStore before AnswerGovernor.govern() is called from Volume 2
STATUS: pending
INTERFACE: Volume 2 calls EvidenceStore.store(tool_name, args, result) after each tool execution in the ReAct loop
```

```
DEPENDENCY: Volume 9 needs BERT classification result from Volume 2 for DecisionValidator.validate()
STATUS: pending
INTERFACE: DecisionValidator.validate(command: str, bert_result) — bert_result from BertIntentClassifier owned by Vol 2
```

```
DEPENDENCY: Volume 9 needs L4.search_facts() for evidence grounding from Volume 1
STATUS: pending
INTERFACE: L4DeclarativeMemory.search_facts(query: str, limit: int) -> list[dict]
```

```
DEPENDENCY: Volume 9 needs failure patterns from Volume 3 (Learning) for FailurePreventionValidator (DEFERRED to Tier 5+)
STATUS: pending
INTERFACE: TBD — failure pattern extraction from L3 episodic memory. Not needed until FailurePreventionValidator is built.
```

---

## Conflict Acknowledgements

```
CONFLICT: Governance schema location
VOLUMES: 1 vs 9
RESOLUTION: resolved — Vol 9 owns governance schemas in rebuild (conflict-report.md C-01)
```

```
CONFLICT: GovernedOutput supersedes ApprovedUtterance
VOLUMES: 6 vs 9
RESOLUTION: resolved — GovernedOutput replaces ApprovedUtterance for all output modalities (conflict-report.md)
```

```
CONFLICT: enforcement_orchestrator.py and enforcement_state.py ownership
VOLUMES: 4 vs 9
RESOLUTION: resolved — Vol 4 owns execution, Vol 9 owns decision (conflict-report.md)
```

```
CONFLICT: OperationalDiagnostician ownership
VOLUMES: 5 vs 8 vs 9
RESOLUTION: resolved — OperationalDiagnostician → Vol 9 (conflict-report.md C-08)
```

```
CONFLICT: memory_guard.py ownership
VOLUMES: 3 vs 1 vs 9
RESOLUTION: resolved — Vol 1 owns (conflict-report.md C-06)
```

```
CONFLICT: TypeScript type generation ownership
VOLUMES: 7 vs 8 vs 9
RESOLUTION: resolved — Vol 8 owns codegen tool. Vol 9 provides governance schemas as input (conflict-report.md C-11)
```

```
CONFLICT: RemediationEngine overlap
VOLUMES: 4 vs 5 vs 9
RESOLUTION: resolved — RemediationEngine → Vol 4 (conflict-report.md C-08)
```
