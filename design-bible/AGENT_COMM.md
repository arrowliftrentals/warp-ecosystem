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
CLAIM: Governance schemas (GovernedOutput, ExtractedClaim, EvidenceItem, EvidenceContract, ApprovedUtterance, AuthorityLevel, OutputPhase, ClaimType, ClaimStatus)
OWNER: Volume 9 (currently in src/memory/schemas.py, must move to Volume 9 in rebuild)
REASON: Output/voice governance schemas owned by Volume 9 per pre-registered boundary; currently co-located in memory schemas file.
CLAIM: ToolRegistry (registration, lookup, schema export, execution orchestration)
OWNER: Volume 10
REASON: Central tool infrastructure per pre-registered boundary — Volume 10 owns DEFINITION, Volume 2 owns INVOCATION.
CLAIM: SelfModifier pipeline (propose > sandbox > verify > approve > apply)
OWNER: Volume 4
REASON: Core self-modification lifecycle orchestrating CodeChange to ImprovementProposal with full sandbox testing.
CLAIM: FastAPI app factory, startup/shutdown lifecycle, middleware stack
OWNER: Volume 8
REASON: Server creation, middleware registration, and lifespan management are API infrastructure concerns.
CLAIM: DecisionValidator (intent/action/tool validation gate)
OWNER: Volume 9
REASON: Central validation checkpoint for all intents, BERT classifications, LLM actions, tool executions, and external data. Produces ValidationDecision (SAFE/UNSAFE/NEEDS_REVIEW/NEEDS_USER_INPUT). Aligns with pre-registered Vol 9 ownership of Intent Validation.
CONTESTED: no
```

```
CLAIM: APEX schemas (PromptStrategy, PromptMetrics, TaskOutcome, TurnAnalysis, PromptStrategyStatus)
OWNER: Volume 3/5 boundary (currently in src/memory/schemas.py, must move in rebuild)
REASON: Prompt optimization schemas belong to the learning/intelligence boundary, not memory.
CLAIM: ToolDefinition dataclass and tool_schemas.py Pydantic parameter/result schemas
OWNER: Volume 10
REASON: Boundary validation schemas for tool inputs and outputs live with tool definitions.
CLAIM: VerificationTracker (HMAC-SHA256 cryptographic proof of test execution)
OWNER: Volume 4
REASON: Enforcement arm of P4 (validation must be real). Signs command output, stores claims in L4.
CLAIM: Error taxonomy (AtlasError hierarchy, ErrorCategory, ErrorSeverity)
OWNER: Volume 8 (shared/errors.py)
REASON: The error hierarchy is cross-cutting infrastructure consumed by every subsystem. Volume 8 defines it; others import it.
CLAIM: AnswerGovernor (output governance pipeline, ADR-0031)
OWNER: Volume 9
REASON: Governs all LLM-generated text via extract → ground → verify → downgrade → scrub → package pipeline. Produces GovernedOutput — single egress schema. Aligns with pre-registered Vol 9 ownership of Output Governance.
CONTESTED: no
```

```
CLAIM: BERT classification schema (BertClassificationResult)
OWNER: Volume 2 (currently in src/memory/schemas.py, must move in rebuild)
REASON: Intent classification belongs to the orchestrator pipeline, not memory.
CLAIM: Core tool handlers (FileTools, GitTools, MemoryTools, ConversationTools, SystemTools, WebTools)
OWNER: Volume 10
REASON: Tool implementation classes and their handler methods. Volume 10 owns what each tool does.
CLAIM: MetaCognitiveMonitor (validation theater detection)
OWNER: Volume 4
REASON: 7 heuristic checks for validation theater patterns. Operates on proposals pre-approval.
CLAIM: Configuration system (AtlasConfig, pydantic-settings)
OWNER: Volume 8 (shared/config.py)
REASON: Server configuration, feature flags, and env-var loading are infrastructure concerns.
CLAIM: EvidenceStore + EvidenceContractRegistry (evidence grounding)
OWNER: Volume 9
REASON: Per-request verbatim tool result store with SHA256 integrity. EvidenceContractRegistry defines required evidence per intent pattern. Core dependency for claim verification in AnswerGovernor.
CONTESTED: no
```

```
CLAIM: Librarian schemas (LibrarianResponse, APIDefinition, SchemaDefinition, CodeReference, IndexResult, CoverageStats, DriftReport, ImpactReport)
OWNER: Volume 5 (currently in src/memory/schemas.py, must move in rebuild)
REASON: Knowledge librarian is an intelligence subsystem; schemas belong with it.
CLAIM: STEM computational backends (backends/mathematics.py, science.py, engineering.py, data_science.py, additive_manufacturing.py)
OWNER: Volume 10
REASON: ADR-0030 computation-first backends are tool-layer implementation with no orchestrator dependency.
CLAIM: RiskAssessor + ApprovalAutomator (risk scoring and graduated approval)
OWNER: Volume 4
REASON: 7-gate risk scoring with auto-approve (LOW risk only) / human escalation.
CLAIM: API request/response Pydantic schemas for chat endpoint (ChatRequest, ChatResponse, EvidenceRef)
OWNER: Volume 8 (contracts/api_schemas.py)
REASON: Cross-boundary schemas shared with Console (Volume 7) live in contracts/. Volume 8 defines the HTTP contract; Volume 2 defines the orchestrator interface.
CLAIM: ConfidenceModel (evidence-based confidence scoring)
OWNER: Volume 9
REASON: Computes confidence from evidence coverage, claim support ratio, and evidence freshness. Replaces self-reported LLM confidence. Internal to governance pipeline.
CONTESTED: no
```

```
CLAIM: Meta-assessment schemas (JarvisBenchmark, Scorecard, BenchmarkEntry, RepoStats, MarketData, ComparativeAnalysis, etc.)
OWNER: KILL - not part of rebuild MVA
REASON: Meta-assessment/benchmarking schemas have no consumer in the rebuild pipeline. Remove from codebase.
CLAIM: Security/pentest tool stack (container_manager, engagement_scope, external_tool_manifest, external_tool_discovery, spec_generator, arsenal)
OWNER: Volume 10
REASON: External tool governance and discovery infrastructure per ADR-0028/0029.
CLAIM: ValidationOrchestrator + APIContractValidator (multi-stage code validation)
OWNER: Volume 4
REASON: 5-stage validation chain (syntax > imports > API contracts > patterns > intent).
CLAIM: ErrorResponse schema (structured error JSON body)
OWNER: Volume 8
REASON: HTTP error formatting is an API-layer concern.
CONTESTED: no
```

```
CLAIM: Screen control subsystem (accessibility.py, controller.py, app_launcher.py)
OWNER: Volume 10
REASON: macOS UI automation is an external capability surface, not orchestrator logic.
CLAIM: SandboxManager + SandboxExecutor + DockerProvider + DockerExecutor (sandbox layer)
OWNER: Volume 4
REASON: Docker-based isolated code execution with snapshot-and-rollback.
CLAIM: IntelligenceCoordinator
OWNER: Volume 5
REASON: Unified facade for intellectual amplification (analogical reasoning, hypothesis generation, Socratic challenge, growth tracking)
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
CLAIM: AnalogicalReasoner
OWNER: Volume 5
REASON: Cross-domain structural mapping with canonical and novel analogy discovery
CONTESTED: no
```

```
CLAIM: ModelTrainer (intent classifier retraining pipeline)
OWNER: Volume 3
REASON: Trains and validates ML models using corrections; tightly coupled to ActiveLearner
CLAIM: HypothesisGenerator
OWNER: Volume 5
REASON: Knowledge gap identification and testable hypothesis generation with provenance
CONTESTED: no
```

```
CLAIM: ModelRegistry (ML model version management)
OWNER: Volume 3
REASON: Manages model loading, promotion, rollback — consumed by learning effectiveness pipeline
CLAIM: SocraticChallenger
OWNER: Volume 5
REASON: Constructive reasoning challenge system with resolution tracking
CONTESTED: no
```

```
CLAIM: EffectivenessTracker + ABTestOrchestrator + StatisticalAnalyzer + GroundTruthCollector
OWNER: Volume 3
REASON: A/B testing and statistical validation of retraining outcomes — core learning measurement
CLAIM: GrowthTracker
OWNER: Volume 5
REASON: Per-user intellectual development tracking with domain mastery profiles
CONTESTED: no
```

```
CLAIM: OutcomeDetector (implicit response quality signal)
OWNER: Volume 3
REASON: Detects whether user follow-up indicates satisfaction or dissatisfaction — feeds learning loop
CLAIM: CausalInferenceEngine
OWNER: Volume 5
REASON: Temporal correlation analysis for anticipatory intelligence (deferred to later tier)
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
CLAIM: IntegrityGuard (SHA-256 tamper detection)
OWNER: Volume 4
REASON: Critical file hash verification at startup. Detects unauthorized modification of validation code.
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

```
CLAIM: Console SPA (React frontend application)
OWNER: Volume 7
REASON: The browser-hosted console is the sole UI surface for Atlas interaction and observability.
CONTESTED: no
```

```
CLAIM: Console TypeScript type definitions (console/src/lib/types.ts)
OWNER: Volume 7
REASON: Console-side TS types are owned by Volume 7; auto-generated from Pydantic schemas (Volume 8/9 source of truth) under R9.
CONTESTED: no (generation ownership TBD - see Conflict Flag below)
```

```
CLAIM: TTS/STT client integration (currently inlined in ChatPanel.tsx)
OWNER: Volume 7 (contested with Volume 6)
REASON: Voice logic is currently embedded in ChatPanel.tsx but belongs to Volume 6. Volume 7 consumes a clean interface after extraction.
CONTESTED: yes (see Conflict Flag below)
```

```
CLAIM: Session management client (console/src/lib/session.ts)
OWNER: Volume 7
REASON: Client-side session persistence and session API consumption is console-owned. Backend session storage is Volume 8.
CONTESTED: no
```

```
CLAIM: Console SPA (React frontend application)
OWNER: Volume 7
REASON: The browser-hosted console is the sole UI surface for Atlas interaction and observability.
CONTESTED: no
```

```
CLAIM: Console TypeScript type definitions (console/src/lib/types.ts)
OWNER: Volume 7
REASON: Console-side TS types are owned by Volume 7; auto-generated from Pydantic schemas (Volume 8/9 source of truth) under R9.
CONTESTED: no (generation ownership TBD - see Conflict Flag below)
```

```
CLAIM: TTS/STT client integration (currently inlined in ChatPanel.tsx)
OWNER: Volume 7 (contested with Volume 6)
REASON: Voice logic is currently embedded in ChatPanel.tsx but belongs to Volume 6. Volume 7 consumes a clean interface after extraction.
CONTESTED: yes (see Conflict Flag below)
```

```
CLAIM: Session management client (console/src/lib/session.ts)
OWNER: Volume 7
REASON: Client-side session persistence and session API consumption is console-owned. Backend session storage is Volume 8.
CLAIM: ClaimExtractor (factual claim extraction from LLM output)
OWNER: Volume 9
REASON: Regex-based extraction of 7 claim types (EXISTENCE, LOCATION, QUANTITATIVE, PROCEDURE, CAPABILITY, CAUSAL, POLICY). Called by AnswerGovernor. Pure function module.
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

```
DEPENDENCY: Volume 7 needs SSE streaming event format specification from Volume 8
STATUS: pending
INTERFACE: SSE event schema: { type: text|thinking|tool_call|tool_result|error|done } (see DB-V07-001 B.3.1)
```

```
DEPENDENCY: Volume 7 needs chat response schema (ChatMessage, ThinkingStep, ToolCall) from Volume 2
STATUS: pending
INTERFACE: ChatMessage, ThinkingStep, ToolCall interfaces (see DB-V07-001 B.3.4)
```

```
DEPENDENCY: Volume 7 needs session CRUD API endpoints from Volume 8
STATUS: pending
INTERFACE: GET/POST/DELETE /v1/sessions (see DB-V07-001 B.3.1)
```

```
DEPENDENCY: Volume 7 needs memory layer read API from Volume 1 (schemas) and Volume 8 (endpoints)
STATUS: pending
INTERFACE: GET /v1/memory/layers, /v1/memory/layers/:name, /v1/memory/search (see DB-V07-001 B.3.1)
```

```
DEPENDENCY: Volume 7 needs health endpoint format from Volume 8
STATUS: pending
INTERFACE: 10 health endpoints returning { status: string } minimum (see DB-V07-001 B.3.1)
```

```
DEPENDENCY: Volume 7 needs WebSocket telemetry protocol from Volume 8
STATUS: pending
INTERFACE: ws://host/ws/telemetry with { type: metrics, data: TelemetryPayload } (see DB-V07-001 B.3.2)
```

```
DEPENDENCY: Volume 7 needs Pydantic-to-TypeScript type generation pipeline from Volume 8 (R9 enablement)
STATUS: pending
INTERFACE: Build-time codegen producing shared/types/ from Pydantic schemas (see DB-V07-001 B.3.5)
```

```
DEPENDENCY: Volume 7 needs GovernedOutput type from Volume 9
STATUS: pending
INTERFACE: GovernedOutput schema replacing raw response text (see DB-V07-001 B.3.7)
```

```
DEPENDENCY: Volume 7 needs SSE streaming event format specification from Volume 8
STATUS: pending
INTERFACE: SSE event schema: { type: text|thinking|tool_call|tool_result|error|done } (see DB-V07-001 B.3.1)
```

```
DEPENDENCY: Volume 7 needs chat response schema (ChatMessage, ThinkingStep, ToolCall) from Volume 2
STATUS: pending
INTERFACE: ChatMessage, ThinkingStep, ToolCall interfaces (see DB-V07-001 B.3.4)
```

```
DEPENDENCY: Volume 7 needs session CRUD API endpoints from Volume 8
STATUS: pending
INTERFACE: GET/POST/DELETE /v1/sessions (see DB-V07-001 B.3.1)
```

```
DEPENDENCY: Volume 7 needs memory layer read API from Volume 1 (schemas) and Volume 8 (endpoints)
STATUS: pending
INTERFACE: GET /v1/memory/layers, /v1/memory/layers/:name, /v1/memory/search (see DB-V07-001 B.3.1)
```

```
DEPENDENCY: Volume 7 needs health endpoint format from Volume 8
STATUS: pending
INTERFACE: 10 health endpoints returning { status: string } minimum (see DB-V07-001 B.3.1)
```

```
DEPENDENCY: Volume 7 needs WebSocket telemetry protocol from Volume 8
STATUS: pending
INTERFACE: ws://host/ws/telemetry with { type: metrics, data: TelemetryPayload } (see DB-V07-001 B.3.2)
```

```
DEPENDENCY: Volume 7 needs Pydantic-to-TypeScript type generation pipeline from Volume 8 (R9 enablement)
STATUS: pending
INTERFACE: Build-time codegen producing shared/types/ from Pydantic schemas (see DB-V07-001 B.3.5)
```

```
DEPENDENCY: Volume 7 needs GovernedOutput type from Volume 9
STATUS: pending
INTERFACE: GovernedOutput schema replacing raw response text (see DB-V07-001 B.3.7)
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
CONFLICT: Verification schemas ownership
VOLUMES: 1 vs 4
PROPOSED RESOLUTION: Volume 1 owns schemas (data entering memory). Volume 4 owns behavioral interface (sign, verify, claim).

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

```
CONFLICT: Governance schema location — GovernedOutput, ExtractedClaim, EvidenceItem, EvidenceContract, AuthorityLevel, ClaimType, ClaimStatus, OutputPhase are governance-domain schemas currently co-located in src/memory/schemas.py (Volume 1 territory).
VOLUMES: 1 vs 9
PROPOSED RESOLUTION: These schemas are governance-specific, not general memory schemas. In the rebuild, extract them to governance/schemas.py owned by Volume 9. Volume 1 retains WorkingMemoryItem, Message, BufferedEvent, ConversationMetadata, and other memory-layer schemas. Pre-registered rule says Volume 1 owns schemas for data entering/leaving memory layers — but GovernedOutput is an output governance schema, not a memory storage schema.
STATUS: open
RESOLUTION: [awaiting gate review]
```

```
CONFLICT: RemediationEngine overlap
VOLUMES: 4 vs 5 vs 9
PROPOSED RESOLUTION: RemediationEngine is self-modification. Should flow through Volume 4 pipeline. Volume 5 owns diagnostics. Volume 4 owns remediation.
CONFLICT: Intelligence schemas ownership — are StructuralAnalogy, Hypothesis, etc. memory schemas or intelligence schemas?
VOLUMES: 1 vs 5
PROPOSED RESOLUTION: Per AGENT_COMM.md pre-registered ownership, Volume 1 owns all Pydantic schemas for data entering/leaving memory layers. These schemas (StructuralAnalogy, Hypothesis, ResearchGap, SocraticChallenge, IntellectualProfile) are stored in and queried from memory layers, so they belong to Volume 1. Volume 5 consumes them. Volume 5 defines interface contracts (method signatures, expected behavior); Volume 1 defines data schemas. The gate should confirm this split.
STATUS: open
RESOLUTION: [awaiting gate review]
```

```
CONFLICT: TTS/STT voice logic inlined in Console ChatPanel.tsx (Vol 7) but owned by Vol 6
VOLUMES: 7 vs 6
PROPOSED RESOLUTION: Vol 6 owns TTS/STT implementation. Vol 7 extracts inlined Cartesia/OpenAI voice code from ChatPanel.tsx and consumes a clean interface from Vol 6.
STATUS: open
RESOLUTION: [awaiting Vol 6 acknowledgement]
```

```
CONFLICT: Endpoint URL prefix inconsistency - console Vite proxy rewrites /api/* but backend uses /v1/* natively
VOLUMES: 7 vs 8
PROPOSED RESOLUTION: Vol 8 defines the canonical prefix. Console proxy should pass-through /v1/* directly. Eliminate /api prefix in production.
STATUS: open
RESOLUTION: [awaiting Vol 8 acknowledgement]
```

```
CONFLICT: TypeScript type generation ownership - who owns the Pydantic-to-TS codegen pipeline?
VOLUMES: 7 vs 8 vs 9
PROPOSED RESOLUTION: Vol 8 (API and Infrastructure) owns the codegen tool and CI step. Vol 9 provides governance schemas as input. Vol 7 consumes the generated output.
STATUS: open
RESOLUTION: [awaiting integration gate]
```

```
CONFLICT: TTS/STT voice logic inlined in Console ChatPanel.tsx (Vol 7) but owned by Vol 6
VOLUMES: 7 vs 6
PROPOSED RESOLUTION: Vol 6 owns TTS/STT implementation. Vol 7 extracts inlined Cartesia/OpenAI voice code from ChatPanel.tsx and consumes a clean interface from Vol 6.
STATUS: open
RESOLUTION: [awaiting Vol 6 acknowledgement]
```

```
CONFLICT: Endpoint URL prefix inconsistency - console Vite proxy rewrites /api/* but backend uses /v1/* natively
VOLUMES: 7 vs 8
PROPOSED RESOLUTION: Vol 8 defines the canonical prefix. Console proxy should pass-through /v1/* directly. Eliminate /api prefix in production.
STATUS: open
RESOLUTION: [awaiting Vol 8 acknowledgement]
```

```
CONFLICT: TypeScript type generation ownership - who owns the Pydantic-to-TS codegen pipeline?
VOLUMES: 7 vs 8 vs 9
PROPOSED RESOLUTION: Vol 8 (API and Infrastructure) owns the codegen tool and CI step. Vol 9 provides governance schemas as input. Vol 7 consumes the generated output.
STATUS: open
RESOLUTION: [awaiting integration gate]
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
| v5 | 2026-03-10 | Distillation Agent V1 | Phase 1: Registered 5 ownership claims (governance schemas->V9, APEX schemas->V3/5, BERT schema->V2, librarian schemas->V5, meta-assessment schemas->KILL), 5 dependency declarations, 0 new conflict flags | Volume 1 agent identified schema families that must move out of memory during rebuild and documented cross-volume dependencies |
|| v4 | 2026-03-10 | Oz | Added Integration Gate Output section referencing `gate-output/` directory and 6 output files per DISTILLATION_PROTOCOL.md | Added a section pointing to where the integration agent stores its analysis results |
|| v5 | 2026-03-10 | Distillation Agent V10 | Phase 1: Registered 7 ownership claims (ToolRegistry, tool schemas, core handlers, STEM backends, security/pentest stack, screen control, external integrations), 4 dependency declarations (MemoryManager from V1, DecisionValidator from V9, ToolRegistry execution to V2, tool introspection to V8). No new conflicts. | Volume 10 agent claimed all tool definitions, registries, and capability implementations; documented cross-volume interface needs |
| v5 | 2026-03-10 | Oz Phase 1 Vol 3 Agent | Phase 1: Registered 10 ownership claims (ActiveLearner, ModelTrainer, ModelRegistry, EffectivenessTracker+AB testing, OutcomeDetector, LearningManager, knowledge pipeline, extractors, PatternLearner, learning schemas/errors), 9 dependency declarations (Volumes 1, 2, 4, 8, 9), 4 conflict flags (cross_layer_linker and hybrid_retriever ownership with Vol 1, knowledge-pipeline schema location, memory_guard ownership) | The learning system agent registered what it owns, what it needs from other systems, and flagged 4 boundary disputes for the integration reviewer |
|| v4 | 2026-03-10 | Oz | Added Integration Gate Output section referencing `gate-output/` directory and 6 output files per DISTILLATION_PROTOCOL.md | Added a section pointing to where the integration agent stores its analysis results |
|| v5 | 2026-03-10 | Distillation Agent V8 | Phase 1: Registered 5 ownership claims (server factory, error taxonomy, config, chat schemas, error response), 5 dependency declarations (orchestrator, memory, governance, logging, console types), 2 conflict flags (error location resolved, query field name resolved) | Volume 8 agent claimed its territory and documented what it needs from other subsystems |
| v5 | 2026-03-10 | Vol-07 Distillation Agent | 4 ownership claims (Console SPA, TS types, TTS/STT client contested with Vol 6, session management), 8 dependency declarations (SSE format, chat schema, sessions, memory, health, WebSocket, type codegen, GovernedOutput from Vol 1/2/8/9), 3 conflict flags (TTS/STT Vol 7 vs 6, endpoint prefix Vol 7 vs 8, codegen ownership Vol 7 vs 8 vs 9) | Console agent registered what it owns, what it needs from other subsystems, and flagged three cross-volume disagreements |
| v5 | 2026-03-10 | Vol-07 Distillation Agent | 4 ownership claims (Console SPA, TS types, TTS/STT client contested with Vol 6, session management), 8 dependency declarations (SSE format, chat schema, sessions, memory, health, WebSocket, type codegen, GovernedOutput from Vol 1/2/8/9), 3 conflict flags (TTS/STT Vol 7 vs 6, endpoint prefix Vol 7 vs 8, codegen ownership Vol 7 vs 8 vs 9) | Console agent registered what it owns, what it needs from other subsystems, and flagged three cross-volume disagreements |
| v5 | 2026-03-10 | Distillation Agent V9 | Phase 1: Registered 5 ownership claims (DecisionValidator, AnswerGovernor, EvidenceStore+EvidenceContractRegistry, ConfidenceModel, ClaimExtractor), 8 dependency declarations (governance schemas from Vol 1, tool results from Vol 2, BERT from Vol 2, AnswerGovernor consumed by Vol 2, DecisionValidator consumed by Vol 2 and Vol 4, GovernedOutput consumed by Vol 6, failure patterns from Vol 3), 3 conflict flags (governance schema location Vol 1 vs 9, GovernedOutput supersedes ApprovedUtterance, enforcement files belong to Vol 4) | Volume 9 agent claimed governance pipeline components; documented cross-volume dependencies and resolved schema/ownership conflicts |
