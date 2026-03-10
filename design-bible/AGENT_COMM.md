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
CLAIM: Governance schemas (GovernedOutput, ExtractedClaim, EvidenceItem, EvidenceContract, ApprovedUtterance, AuthorityLevel, OutputPhase, ClaimType, ClaimStatus)
OWNER: Volume 9 (currently in src/memory/schemas.py, must move to Volume 9 in rebuild)
REASON: Output/voice governance schemas owned by Volume 9 per pre-registered boundary; currently co-located in memory schemas file.
CLAIM: ToolRegistry (registration, lookup, schema export, execution orchestration)
OWNER: Volume 10
REASON: Central tool infrastructure per pre-registered boundary — Volume 10 owns DEFINITION, Volume 2 owns INVOCATION.
CONTESTED: no
```

```
CLAIM: APEX schemas (PromptStrategy, PromptMetrics, TaskOutcome, TurnAnalysis, PromptStrategyStatus)
OWNER: Volume 3/5 boundary (currently in src/memory/schemas.py, must move in rebuild)
REASON: Prompt optimization schemas belong to the learning/intelligence boundary, not memory.
CLAIM: ToolDefinition dataclass and tool_schemas.py Pydantic parameter/result schemas
OWNER: Volume 10
REASON: Boundary validation schemas for tool inputs and outputs live with tool definitions.
CONTESTED: no
```

```
CLAIM: BERT classification schema (BertClassificationResult)
OWNER: Volume 2 (currently in src/memory/schemas.py, must move in rebuild)
REASON: Intent classification belongs to the orchestrator pipeline, not memory.
CLAIM: Core tool handlers (FileTools, GitTools, MemoryTools, ConversationTools, SystemTools, WebTools)
OWNER: Volume 10
REASON: Tool implementation classes and their handler methods. Volume 10 owns what each tool does.
CONTESTED: no
```

```
CLAIM: Librarian schemas (LibrarianResponse, APIDefinition, SchemaDefinition, CodeReference, IndexResult, CoverageStats, DriftReport, ImpactReport)
OWNER: Volume 5 (currently in src/memory/schemas.py, must move in rebuild)
REASON: Knowledge librarian is an intelligence subsystem; schemas belong with it.
CLAIM: STEM computational backends (backends/mathematics.py, science.py, engineering.py, data_science.py, additive_manufacturing.py)
OWNER: Volume 10
REASON: ADR-0030 computation-first backends are tool-layer implementation with no orchestrator dependency.
CONTESTED: no
```

```
CLAIM: Meta-assessment schemas (JarvisBenchmark, Scorecard, BenchmarkEntry, RepoStats, MarketData, ComparativeAnalysis, etc.)
OWNER: KILL - not part of rebuild MVA
REASON: Meta-assessment/benchmarking schemas have no consumer in the rebuild pipeline. Remove from codebase.
CLAIM: Security/pentest tool stack (container_manager, engagement_scope, external_tool_manifest, external_tool_discovery, spec_generator, arsenal)
OWNER: Volume 10
REASON: External tool governance and discovery infrastructure per ADR-0028/0029.
CONTESTED: no
```

```
CLAIM: Screen control subsystem (accessibility.py, controller.py, app_launcher.py)
OWNER: Volume 10
REASON: macOS UI automation is an external capability surface, not orchestrator logic.
CONTESTED: no
```

```
CLAIM: External integration tools (email_tools, calendar_tools, messaging_tools, home_tools, voice_tools, screen_tools)
OWNER: Volume 10
REASON: Integration wrappers exposing external service APIs as tool handlers.
CONTESTED: no
```


```
CLAIM: ActiveLearner (correction collection, retraining triggers)
OWNER: Volume 3
REASON: Core learning loop component — collects user corrections and determines when retraining is needed
CONTESTED: no
```

```
CLAIM: ModelTrainer (intent classifier retraining pipeline)
OWNER: Volume 3
REASON: Trains and validates ML models using corrections; tightly coupled to ActiveLearner
CONTESTED: no
```

```
CLAIM: ModelRegistry (ML model version management)
OWNER: Volume 3
REASON: Manages model loading, promotion, rollback — consumed by learning effectiveness pipeline
CONTESTED: no
```

```
CLAIM: EffectivenessTracker + ABTestOrchestrator + StatisticalAnalyzer + GroundTruthCollector
OWNER: Volume 3
REASON: A/B testing and statistical validation of retraining outcomes — core learning measurement
CONTESTED: no
```

```
CLAIM: OutcomeDetector (implicit response quality signal)
OWNER: Volume 3
REASON: Detects whether user follow-up indicates satisfaction or dissatisfaction — feeds learning loop
CONTESTED: no
```

```
CLAIM: LearningManager (learning facade)
OWNER: Volume 3
REASON: Central coordinator for pattern learning, feedback processing, and improvement suggestions
CONTESTED: no
```

```
CLAIM: ContentIngester, DomainClassifier, DomainToolRouter, KnowledgeSynthesizer, ContradictionDetector
OWNER: Volume 3
REASON: Knowledge ingestion pipeline per pre-registered boundary in AGENT_COMM.md
CONTESTED: no
```

```
CLAIM: extractors/ (base.py, general.py, all domain extractors)
OWNER: Volume 3
REASON: Domain extractors are part of the knowledge pipeline per pre-registered boundary
CONTESTED: no
```

```
CLAIM: PatternLearner (command pattern tracking, workflow detection)
OWNER: Volume 3
REASON: Behavioral learning from user command patterns — core LearningManager dependency
CONTESTED: no
```

```
CLAIM: learning/schemas.py and learning/errors.py (learning-specific Pydantic schemas and error types)
OWNER: Volume 3
REASON: Pydantic schemas and error types specific to the learning subsystem
CONTESTED: no
```

---

## Dependency Declarations (Agent-Registered)

```
DEPENDENCY: Volume 2 (Orchestrator) needs MemoryManager.assemble_context() from Volume 1
STATUS: pending
INTERFACE: assemble_context(conversation_id: str, user_query: Optional[str], max_messages: int = 10, max_facts: int = 5, max_episodes: int = 3, max_semantic: int = 5) -> Dict[str, Any]
```

```
DEPENDENCY: Volume 3 (Learning) needs L4.search_facts(), L5 procedural store, L3.store_episode() from Volume 1
STATUS: pending
INTERFACE: L4DeclarativeMemory.search_facts(query, limit) -> list[dict]; L5ProceduralMemory.store_skill(Skill); L3EpisodicMemory.store_episode(Episode)
```

```
DEPENDENCY: Volume 8 (API) needs MemoryManager.get_stats(), MemoryManager.get_recent_conversations() from Volume 1
STATUS: pending
INTERFACE: get_stats() -> Dict[str, Any]; get_recent_conversations(hours: int, limit: int) -> List[Dict[str, Any]]
```

```
DEPENDENCY: Volume 9 (Governance) needs L4.search_facts() for evidence grounding from Volume 1
STATUS: pending
INTERFACE: L4DeclarativeMemory.search_facts(query: str, limit: int) -> list[dict]
```

```
DEPENDENCY: Volume 1 (Memory) needs shared infrastructure (shared/errors.py, shared/config.py, shared/logging.py) from cross-cutting infra
STATUS: pending
INTERFACE: Error hierarchy from shared/errors.py; config object from shared/config.py; structured logging from shared/logging.py
DEPENDENCY: Volume 10 needs MemoryManager interface (L1-L10 access) from Volume 1
STATUS: pending
INTERFACE: MemoryManager with layer accessors (.l1 through .l10), search methods, get_stats(), get_consolidation_health(), get_safeguards_status()
```

```
DEPENDENCY: Volume 10 needs DecisionValidator.validate(command, context) from Volume 9
STATUS: pending
INTERFACE: DecisionValidator.validate(command: str, context: dict | None) -> ValidationResult with is_safe(), blocked_reasons, requires_confirmation
```

```
DEPENDENCY: Volume 2 (Orchestrator) needs ToolRegistry.execute() and ToolRegistry.get_openai_schema_for_query() from Volume 10
STATUS: pending
INTERFACE: ToolRegistry.execute(tool_name, arguments, context) -> ToolResult; ToolRegistry.get_openai_schema_for_query(query, max_tools) -> list[dict]
```

```
DEPENDENCY: Volume 8 (API) needs tool introspection surface from Volume 10
STATUS: pending
INTERFACE: ToolRegistry.list_tools() -> list[str]; SystemTools.get_tool_list(category) -> dict
```


```
DEPENDENCY: Volume 3 needs MemoryManager (L3, L4, L5, L7, L10) from Volume 1
STATUS: pending
INTERFACE: MemoryManager with typed accessors for L3 (episodes), L4 (facts/assert_fact), L5 (procedural patterns/corrections), L7 (world state capture/query), L10 (vector search)
```

```
DEPENDENCY: Volume 3 needs Pydantic schemas (NormalizedContent, ContentType, DomainClassification, ScientificDomain, ExtractionResult, ExtractedEntity, ExtractedRelation, RefinedKnowledge, SynthesizedKnowledge, DomainKnowledgeEntry, ContradictionResult, ConflictType, OutcomeSignal, OutcomeType, Fact, FactSource, KnowledgeGap, Contradiction) from Volume 1
STATUS: pending
INTERFACE: Pydantic BaseModel subclasses in atlas.memory.schemas
```

```
DEPENDENCY: Volume 3 needs intent classification results (predicted_intent, confidence) from Volume 2
STATUS: pending
INTERFACE: IntentResult schema or equivalent with at minimum: intent: str, confidence: float, method: str
```

```
DEPENDENCY: Volume 3 needs DecisionValidator from Volume 9 for validating learning actions
STATUS: pending
INTERFACE: DecisionValidator.validate(action, context) -> ValidationResult
```

```
DEPENDENCY: Volume 2 needs LearningManager.suggest_patterns() from Volume 3
STATUS: pending
INTERFACE: suggest_patterns(trigger: str, context: dict | None, limit: int) -> list[dict] with keys trigger, action, confidence, type
```

```
DEPENDENCY: Volume 2 needs OutcomeDetector.analyze_follow_up() from Volume 3
STATUS: pending
INTERFACE: async analyze_follow_up(previous_query, previous_response, follow_up_message, provenance, conversation_id) -> OutcomeSignal
```

```
DEPENDENCY: Volume 4 needs LearningManager.record_proposal_outcome() from Volume 3
STATUS: pending
INTERFACE: record_proposal_outcome(proposal_id, proposal_type, status, ...) -> dict (insights)
```

```
DEPENDENCY: Volume 8 needs learning health/stats endpoints from Volume 3
STATUS: pending
INTERFACE: LearningManager.get_stats() -> dict, EffectivenessTracker.get_learning_patterns() -> dict
```

---

## Conflict Flags (Agent-Registered)
*No new conflicts identified by Volume 1 distillation. Schema co-location in schemas.py is a known migration task, not a cross-volume disagreement.*
*No new conflicts flagged by Volume 10 distillation. All ownership boundaries align with pre-registered decisions.*


```
CONFLICT: cross_layer_linker.py creates connections between memory layers — this is memory infrastructure, not learning
VOLUMES: 3 vs 1
PROPOSED RESOLUTION: Move to Volume 1 (Memory). Volume 3 DEFERs this component; Volume 1 should claim it if cross-layer linking is part of MemoryManager's responsibility.
STATUS: open
RESOLUTION: [awaiting integration gate]
```

```
CONFLICT: hybrid_retriever.py combines FTS5 + FAISS + graph retrieval — this is memory retrieval infrastructure, not learning
VOLUMES: 3 vs 1
PROPOSED RESOLUTION: Move to Volume 1 (Memory). The retrieval layer is a memory concern. Volume 3 DEFERs this component.
STATUS: open
RESOLUTION: [awaiting integration gate]
```

```
CONFLICT: Knowledge-pipeline Pydantic schemas (NormalizedContent, ExtractionResult, DomainClassification, etc.) are currently in src/memory/schemas.py owned by Volume 1, but they are knowledge-pipeline-specific, not memory-specific
VOLUMES: 3 vs 1
PROPOSED RESOLUTION: Knowledge-pipeline schemas should live in atlas.learning.schemas or a shared contracts location. Memory-generic schemas (OutcomeSignal, Fact, etc.) stay in Volume 1.
STATUS: open
RESOLUTION: [awaiting integration gate]
```

```
CONFLICT: memory_guard.py validates memory operations — governance or memory concern, not learning
VOLUMES: 3 vs 1 vs 9
PROPOSED RESOLUTION: Volume 3 KILLs this component. Volume 9 (Governance) or Volume 1 (Memory) should own memory validation if rebuilt.
STATUS: open
RESOLUTION: [awaiting integration gate]
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
| v5 | 2026-03-10 | Distillation Agent V1 | Phase 1: Registered 5 ownership claims (governance schemas->V9, APEX schemas->V3/5, BERT schema->V2, librarian schemas->V5, meta-assessment schemas->KILL), 5 dependency declarations, 0 new conflict flags | Volume 1 agent identified schema families that must move out of memory during rebuild and documented cross-volume dependencies |
|| v4 | 2026-03-10 | Oz | Added Integration Gate Output section referencing `gate-output/` directory and 6 output files per DISTILLATION_PROTOCOL.md | Added a section pointing to where the integration agent stores its analysis results |
|| v5 | 2026-03-10 | Distillation Agent V10 | Phase 1: Registered 7 ownership claims (ToolRegistry, tool schemas, core handlers, STEM backends, security/pentest stack, screen control, external integrations), 4 dependency declarations (MemoryManager from V1, DecisionValidator from V9, ToolRegistry execution to V2, tool introspection to V8). No new conflicts. | Volume 10 agent claimed all tool definitions, registries, and capability implementations; documented cross-volume interface needs |
| v5 | 2026-03-10 | Oz Phase 1 Vol 3 Agent | Phase 1: Registered 10 ownership claims (ActiveLearner, ModelTrainer, ModelRegistry, EffectivenessTracker+AB testing, OutcomeDetector, LearningManager, knowledge pipeline, extractors, PatternLearner, learning schemas/errors), 9 dependency declarations (Volumes 1, 2, 4, 8, 9), 4 conflict flags (cross_layer_linker and hybrid_retriever ownership with Vol 1, knowledge-pipeline schema location, memory_guard ownership) | The learning system agent registered what it owns, what it needs from other systems, and flagged 4 boundary disputes for the integration reviewer |
