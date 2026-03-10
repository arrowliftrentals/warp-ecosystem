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
|| **Version** | v5 |
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
CLAIM: FastAPI app factory, startup/shutdown lifecycle, middleware stack
OWNER: Volume 8
REASON: Server creation, middleware registration, and lifespan management are API infrastructure concerns.
CONTESTED: no
```

```
CLAIM: Error taxonomy (AtlasError hierarchy, ErrorCategory, ErrorSeverity)
OWNER: Volume 8 (shared/errors.py)
REASON: The error hierarchy is cross-cutting infrastructure consumed by every subsystem. Volume 8 defines it; others import it.
CONTESTED: no
```

```
CLAIM: Configuration system (AtlasConfig, pydantic-settings)
OWNER: Volume 8 (shared/config.py)
REASON: Server configuration, feature flags, and env-var loading are infrastructure concerns.
CONTESTED: no
```

```
CLAIM: API request/response Pydantic schemas for chat endpoint (ChatRequest, ChatResponse, EvidenceRef)
OWNER: Volume 8 (contracts/api_schemas.py)
REASON: Cross-boundary schemas shared with Console (Volume 7) live in contracts/. Volume 8 defines the HTTP contract; Volume 2 defines the orchestrator interface.
CONTESTED: no
```

```
CLAIM: ErrorResponse schema (structured error JSON body)
OWNER: Volume 8
REASON: HTTP error formatting is an API-layer concern.
CONTESTED: no
```

```
CLAIM: IntelligenceCoordinator
OWNER: Volume 5
REASON: Unified facade for intellectual amplification (analogical reasoning, hypothesis generation, Socratic challenge, growth tracking)
CONTESTED: no
```

```
CLAIM: AnalogicalReasoner
OWNER: Volume 5
REASON: Cross-domain structural mapping with canonical and novel analogy discovery
CONTESTED: no
```

```
CLAIM: HypothesisGenerator
OWNER: Volume 5
REASON: Knowledge gap identification and testable hypothesis generation with provenance
CONTESTED: no
```

```
CLAIM: SocraticChallenger
OWNER: Volume 5
REASON: Constructive reasoning challenge system with resolution tracking
CONTESTED: no
```

```
CLAIM: GrowthTracker
OWNER: Volume 5
REASON: Per-user intellectual development tracking with domain mastery profiles
CONTESTED: no
```

```
CLAIM: CausalInferenceEngine
OWNER: Volume 5
REASON: Temporal correlation analysis for anticipatory intelligence (deferred to later tier)
CONTESTED: no
```

```
CLAIM: OperationalDiagnostician + InvariantEvaluator + RemediationEngine
OWNER: Volume 5 (contested)
REASON: System self-diagnostics lives in src/intelligence/ but is infrastructure-oriented. See conflict flag below.
CONTESTED: yes — potential overlap with Volume 8 (observability) and Volume 9 (health truthfulness governance)
```

```
CLAIM: AcquisitionCoordinator + ArXivFetcher + LocalWatcher + ContentQueue
OWNER: Volume 5
REASON: Content acquisition layer (src/acquisition/) feeding the intelligence pipeline. All deferred.
CONTESTED: no
```

---

## Dependency Declarations (Agent-Registered)

```
DEPENDENCY: Volume 8 needs Orchestrator.process_command() and Orchestrator.process_command_streaming() from Volume 2
STATUS: pending
INTERFACE: async def process_command(command: str, device_id: str, conversation_id: str | None) -> dict; async generator process_command_streaming(...) -> AsyncIterator[StreamEvent]
```

```
DEPENDENCY: Volume 8 needs MemoryManager.get_stats(), MemoryManager.get_recent_conversations() from Volume 1
STATUS: pending
INTERFACE: To be defined by Volume 1 in B.3
```

```
DEPENDENCY: Volume 8 needs GovernedOutput / output governance gate from Volume 9
STATUS: pending
INTERFACE: ChatResponse.governed field + EvidenceRef list depend on Volume 9's governance output schema
```

```
DEPENDENCY: Volume 8 needs structlog configured logging from shared/logging.py (cross-cutting, no single volume owner)
STATUS: pending
INTERFACE: from atlas.shared.logging import log (structlog.BoundLogger)
```

```
DEPENDENCY: Volume 7 (Console) needs the ChatRequest/ChatResponse/ErrorResponse schemas from Volume 8 contracts/api_schemas.py for TypeScript type generation
STATUS: pending
INTERFACE: Pydantic models in contracts/api_schemas.py → generated TypeScript types via scripts/generate_contracts.sh
```

```
DEPENDENCY: Volume 5 needs MemoryManager (L4 query_facts, L9 get_profile/update_profile, L10 search_similar, L3 store_episode) from Volume 1
STATUS: pending
INTERFACE: MemoryManager.l4.query_facts(query, min_confidence, limit) -> list[DeclarativeFact]; MemoryManager.l9.get_profile(user_id) -> UserProfile; MemoryManager.l10.search_similar(query, n_results) -> list[dict]; MemoryManager.l3.store_episode(Episode) -> None
```

```
DEPENDENCY: Volume 5 needs RefinedKnowledge schema from Volume 3 (Learning)
STATUS: pending
INTERFACE: RefinedKnowledge Pydantic schema produced by KnowledgeSynthesizer, consumed by intelligence amplification via L4 memory queries
```

```
DEPENDENCY: Volume 5 needs ContentIngester and KnowledgeEngine from Volume 3 (Learning) for AcquisitionCoordinator (DEFERRED)
STATUS: pending
INTERFACE: ContentIngester.ingest(source, content_type, metadata) -> NormalizedContent; KnowledgeEngine.acquire(KnowledgeSource) -> AcquisitionResult
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs IntelligenceCoordinator.amplify_query(), cross_domain_insight(), challenge_and_refine() from Volume 5
STATUS: pending
INTERFACE: IntelligenceCoordinator methods as specified in Volume 5 B.3
```

```
DEPENDENCY: Volume 5 needs Pydantic schemas (StructuralAnalogy, Hypothesis, ResearchGap, SocraticChallenge, IntellectualProfile, CalibratedConfidence, ProvenanceChain, ProvenanceStep, SourceQuality) from Volume 1 (Memory schemas)
STATUS: pending
INTERFACE: All schemas as specified in Volume 5 B.3 schema listing
```

---

## Conflict Flags (Agent-Registered)

```
CONFLICT: Error taxonomy location — PROJECT_CONVENTIONS.md Section 6 specifies shared/errors.py, but Attempt 3's errors.py is at src/errors.py (top-level). The rebuild MUST use shared/errors.py per conventions.
VOLUMES: 8 (owns errors) vs all consumers
PROPOSED RESOLUTION: Follow PROJECT_CONVENTIONS.md: atlas/shared/errors.py. No conflict expected — just documenting the relocation.
STATUS: resolved
RESOLUTION: shared/errors.py per PROJECT_CONVENTIONS.md Section 6.
```

```
CONFLICT: Chat endpoint request field naming — Attempt 3 uses 'query' in ConsoleQueryRequest. The rebuild must preserve this to maintain Console compatibility. Volume 2 (Orchestrator) should accept 'query' as the input field name, not 'message' or 'command'.
VOLUMES: 8 vs 2 vs 7
PROPOSED RESOLUTION: ChatRequest.query is the canonical field name. Orchestrator accepts 'query'. Console sends 'query'. Already aligned with Attempt 3.
STATUS: resolved
RESOLUTION: Field name is 'query' everywhere.
```

```
CONFLICT: OperationalDiagnostician ownership ambiguity
VOLUMES: 5 vs 8 vs 9
PROPOSED RESOLUTION: OperationalDiagnostician lives in src/intelligence/ but its purpose (health truthfulness checking, data flow analysis, remediation patches) overlaps with Volume 8 (Infrastructure/observability) and Volume 9 (Governance/validation). The InvariantEvaluator is governance-adjacent. The RemediationEngine is self-modification-adjacent (Volume 4). Proposed: Move operational diagnostics to Volume 9 (Governance) since health truthfulness is fundamentally a governance concern per Volume 0 P4 (Validation Must Be Real). Volume 5 retains only user-facing amplification components.
STATUS: open
RESOLUTION: [awaiting gate review]
```

```
CONFLICT: Intelligence schemas ownership — are StructuralAnalogy, Hypothesis, etc. memory schemas or intelligence schemas?
VOLUMES: 1 vs 5
PROPOSED RESOLUTION: Per AGENT_COMM.md pre-registered ownership, Volume 1 owns all Pydantic schemas for data entering/leaving memory layers. These schemas (StructuralAnalogy, Hypothesis, ResearchGap, SocraticChallenge, IntellectualProfile) are stored in and queried from memory layers, so they belong to Volume 1. Volume 5 consumes them. Volume 5 defines interface contracts (method signatures, expected behavior); Volume 1 defines data schemas. The gate should confirm this split.
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
|| v4 | 2026-03-10 | Oz | Added Integration Gate Output section referencing `gate-output/` directory and 6 output files per DISTILLATION_PROTOCOL.md | Added a section pointing to where the integration agent stores its analysis results |
|| v5 | 2026-03-10 | Distillation Agent V8 | Phase 1: Registered 5 ownership claims (server factory, error taxonomy, config, chat schemas, error response), 5 dependency declarations (orchestrator, memory, governance, logging, console types), 2 conflict flags (error location resolved, query field name resolved) | Volume 8 agent claimed its territory and documented what it needs from other subsystems |
