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
CLAIM: DecisionValidator (intent/action/tool validation gate)
OWNER: Volume 9
REASON: Central validation checkpoint for all intents, BERT classifications, LLM actions, tool executions, and external data. Produces ValidationDecision (SAFE/UNSAFE/NEEDS_REVIEW/NEEDS_USER_INPUT). Aligns with pre-registered Vol 9 ownership of Intent Validation.
CONTESTED: no
```

```
CLAIM: AnswerGovernor (output governance pipeline, ADR-0031)
OWNER: Volume 9
REASON: Governs all LLM-generated text via extract → ground → verify → downgrade → scrub → package pipeline. Produces GovernedOutput — single egress schema. Aligns with pre-registered Vol 9 ownership of Output Governance.
CONTESTED: no
```

```
CLAIM: EvidenceStore + EvidenceContractRegistry (evidence grounding)
OWNER: Volume 9
REASON: Per-request verbatim tool result store with SHA256 integrity. EvidenceContractRegistry defines required evidence per intent pattern. Core dependency for claim verification in AnswerGovernor.
CONTESTED: no
```

```
CLAIM: ConfidenceModel (evidence-based confidence scoring)
OWNER: Volume 9
REASON: Computes confidence from evidence coverage, claim support ratio, and evidence freshness. Replaces self-reported LLM confidence. Internal to governance pipeline.
CONTESTED: no
```

```
CLAIM: ClaimExtractor (factual claim extraction from LLM output)
OWNER: Volume 9
REASON: Regex-based extraction of 7 claim types (EXISTENCE, LOCATION, QUANTITATIVE, PROCEDURE, CAPABILITY, CAUSAL, POLICY). Called by AnswerGovernor. Pure function module.
CONTESTED: no
```

---

## Dependency Declarations (Agent-Registered)

```
DEPENDENCY: Volume 9 needs governance Pydantic schemas (GovernedOutput, ExtractedClaim, EvidenceItem, EvidenceContract, AuthorityLevel, ClaimType, ClaimStatus, OutputPhase) extracted from src/memory/schemas.py
STATUS: pending
INTERFACE: Currently in Vol 1 schemas.py. Vol 9 proposes extracting to governance/schemas.py. See conflict flag.
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
DEPENDENCY: Volume 2 (Orchestrator) needs AnswerGovernor.govern() from Volume 9 to govern all LLM output
STATUS: pending
INTERFACE: AnswerGovernor.govern(content: str, phase: OutputPhase, evidence_store: EvidenceStore) → GovernedOutput
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs DecisionValidator.validate_tool_execution() from Volume 9 to validate tool calls
STATUS: pending
INTERFACE: DecisionValidator.validate_tool_execution(tool_name: str, args: dict, context: dict) → ValidationDecision
```

```
DEPENDENCY: Volume 6 (Voice) needs GovernedOutput from Volume 9 to replace ApprovedUtterance
STATUS: pending
INTERFACE: GovernedOutput schema (replaces ApprovedUtterance for all output modalities including voice)
```

```
DEPENDENCY: Volume 4 (Self-Modification) needs DecisionValidator.validate_intent() from Volume 9
STATUS: pending
INTERFACE: DecisionValidator.validate_intent(intent: str, context: dict) → ValidationDecision
```

```
DEPENDENCY: Volume 9 needs failure patterns from Volume 3 (Learning) for FailurePreventionValidator (DEFERRED to Tier 5+)
STATUS: pending
INTERFACE: TBD — failure pattern extraction from L3 episodic memory. Not needed until FailurePreventionValidator is built.
```

---

## Conflict Flags (Agent-Registered)

```
CONFLICT: Governance schema location — GovernedOutput, ExtractedClaim, EvidenceItem, EvidenceContract, AuthorityLevel, ClaimType, ClaimStatus, OutputPhase are governance-domain schemas currently co-located in src/memory/schemas.py (Volume 1 territory).
VOLUMES: 1 vs 9
PROPOSED RESOLUTION: These schemas are governance-specific, not general memory schemas. In the rebuild, extract them to governance/schemas.py owned by Volume 9. Volume 1 retains WorkingMemoryItem, Message, BufferedEvent, ConversationMetadata, and other memory-layer schemas. Pre-registered rule says Volume 1 owns schemas for data entering/leaving memory layers — but GovernedOutput is an output governance schema, not a memory storage schema.
STATUS: open
RESOLUTION: [awaiting gate review]
```

```
CONFLICT: GovernedOutput supersedes ApprovedUtterance for all output modalities.
VOLUMES: 6 vs 9
PROPOSED RESOLUTION: GovernedOutput (Vol 9) extends ApprovedUtterance (Vol 6 voice precursor) to ALL output modalities. In the rebuild, ApprovedUtterance is KILLED; GovernedOutput is the single egress schema. Volume 6 (Voice) consumes GovernedOutput for voice output. AuthorityLevel enum is shared.
STATUS: resolved
RESOLUTION: GovernedOutput replaces ApprovedUtterance. Volume 6 consumes GovernedOutput from Volume 9.
```

```
CONFLICT: enforcement_orchestrator.py and enforcement_state.py belong to Volume 4, not Volume 9.
VOLUMES: 4 vs 9
PROPOSED RESOLUTION: These files are in the Volume 9 A.2 source manifest but implement self-modification enforcement. Volume 4 already claims SelfModifier pipeline and related enforcement. Volume 9 KILLS these from its scope; Volume 4 owns them.
STATUS: resolved
RESOLUTION: Volume 4 owns enforcement_orchestrator.py and enforcement_state.py. Volume 9 governs the DECISION (via DecisionValidator); Volume 4 owns the EXECUTION.
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
| v5 | 2026-03-10 | Distillation Agent V9 | Phase 1: Registered 5 ownership claims (DecisionValidator, AnswerGovernor, EvidenceStore+EvidenceContractRegistry, ConfidenceModel, ClaimExtractor), 8 dependency declarations (governance schemas from Vol 1, tool results from Vol 2, BERT from Vol 2, AnswerGovernor consumed by Vol 2, DecisionValidator consumed by Vol 2 and Vol 4, GovernedOutput consumed by Vol 6, failure patterns from Vol 3), 3 conflict flags (governance schema location Vol 1 vs 9, GovernedOutput supersedes ApprovedUtterance, enforcement files belong to Vol 4) | Volume 9 agent claimed governance pipeline components; documented cross-volume dependencies and resolved schema/ownership conflicts |
