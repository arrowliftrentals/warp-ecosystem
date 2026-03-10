# ATLAS Design Bible — Volume 3: Learning & Adaptation

| Field | Value |
|---|---|
| **Doc ID** | `DB-V03-001` |
| **Name** | Volume 3: Learning & Adaptation |
| **Purpose** | Design specification for the active learning, correction pipeline, retraining, and knowledge ingestion systems |
| **Owner** | Design Bible / Volume 3 |
| **Status** | `draft` (Phase 1 distillation complete — B.1-B.4 filled, B.5-B.13 awaiting Phase 2) |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / TBD distillation agent (Part B) |
| **Version** | v5 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## Part A: Context (Pre-loaded)

### A.1 Subsystem Identity
- **Volume 3: Learning & Adaptation**
- **Purpose:** Enables Atlas to learn from user corrections, retrain classifiers, adapt to user preferences, and improve over time — the system that makes Atlas get smarter, not just remember more.
- **Rebuild phase:** Phase 2 (after memory system). Learning depends on memory layers for storage and retrieval.

### A.2 Source Manifest

**Code files to read** (paths relative to `atlas/`):

*Core learning:*
- `src/learning/active_learner.py` — collects user corrections, triggers retraining
- `src/learning/auto_retrain_daemon.py` — automatic retraining pipeline
- `src/learning/effectiveness_tracker.py` — tracks if learning actually improves performance
- `src/learning/effectiveness_coordinator.py`
- `src/learning/feedback_processor.py` — processes user feedback
- `src/learning/learning_manager.py` — coordinates learning components
- `src/learning/learning_scheduler.py`
- `src/learning/learning_verifier.py`
- `src/learning/model_trainer.py` — model training
- `src/learning/model_registry.py` — model versioning
- `src/learning/retrain_triggers.py` — retraining trigger conditions
- `src/learning/ab_testing.py` — A/B testing for model comparison
- `src/learning/ab_testing_classification_service.py`
- `src/learning/outcome_detector.py` — detects interaction outcomes

*Knowledge pipeline:*
- `src/learning/content_ingester.py` — content normalization
- `src/learning/domain_classifier.py` — domain classification
- `src/learning/domain_tool_router.py` — routes to domain extractors
- `src/learning/knowledge_synthesizer.py` — merges extractions
- `src/learning/knowledge_graph.py`
- `src/learning/knowledge_engine.py`
- `src/learning/knowledge_council.py`
- `src/learning/knowledge_librarian.py`
- `src/learning/knowledge_scheduler.py`
- `src/learning/knowledge_versioning.py`
- `src/learning/knowledge_extractor.py`
- `src/learning/contradiction_detector.py`
- `src/learning/gap_identifier.py`
- `src/learning/semantic_graph.py`
- `src/learning/cross_layer_linker.py`
- `src/learning/hybrid_retriever.py`

*Domain extractors:*
- `src/learning/extractors/base.py`
- `src/learning/extractors/atlas_self.py`
- `src/learning/extractors/chemistry.py`
- `src/learning/extractors/physics.py`
- `src/learning/extractors/biology.py`
- `src/learning/extractors/materials.py`
- `src/learning/extractors/engineering.py`
- `src/learning/extractors/general.py`
- `src/learning/extractors/earth_science.py`
- `src/learning/extractors/autocad.py`
- `src/learning/extractors/matlab.py`
- `src/learning/extractors/fea_suite.py`
- `src/learning/extractors/rate_limiter.py`

*Advanced learning:*
- `src/learning/pattern_learner.py`
- `src/learning/pattern_matching.py`
- `src/learning/principle_abstractor.py`
- `src/learning/concept_builder.py`
- `src/learning/abstraction_engine.py`
- `src/learning/domain_transfer.py`
- `src/learning/domain_knowledge_base.py`
- `src/learning/prompt_optimizer.py`
- `src/learning/hyperparameter_optimizer.py`

*Other:*
- `src/learning/schemas.py`
- `src/learning/errors.py`
- `src/learning/consolidation.py`
- `src/learning/code_explainer.py`
- `src/learning/documentation_exporters.py`
- `src/learning/feature_detector.py`
- `src/learning/file_watcher.py`
- `src/learning/fix_learner.py`
- `src/learning/human_review.py`
- `src/learning/intelligence_learning_engine.py`
- `src/learning/memory_guard.py`
- `src/learning/proposal_learner.py`
- `src/learning/skill_router.py`
- `src/learning/statistical_analysis.py`
- `src/learning/system_scaffolder.py`
- `src/learning/db_migrations.py`
- `src/learning/ai_agent_failure_patterns.py`
- `src/learning/architecture_experimenter.py`

**Documentation to read:**
- `docs/architecture/intelligence-system.md`
- `docs/architecture/knowledge-ingestion-design.md`
- `docs/architecture/learning-tools.md`
- `docs/guides/intelligence-pipeline-manual.md`
- `docs/guides/knowledge-council-chat.md`
- `docs/guides/knowledge-librarian-quickstart.md`
- `docs/development/bert-integration-complete.md`
- `docs/adr/0019-automated-retraining.md`
- `docs/adr/0027-cross-domain-knowledge-transfer.md`
- `docs/plans/intelligence-system-part-a.md` through `part-e.md`
- `docs/LEARNING_FROM_AI_FAILURES.md`

**Test files to read:**
- `tests/learning/` (entire directory)

**CORE/PERIPHERAL Classification** (per `DISTILLATION_PROTOCOL.md` Section 5):
- **CORE** (15 files): `active_learner.py`, `learning_manager.py`, `feedback_processor.py`, `model_trainer.py`, `model_registry.py`, `retrain_triggers.py`, `outcome_detector.py`, `effectiveness_tracker.py`, `content_ingester.py`, `domain_classifier.py`, `knowledge_synthesizer.py`, `knowledge_extractor.py`, `contradiction_detector.py`, `schemas.py`, `errors.py`
- **PERIPHERAL** (55 files): All domain extractors (13), all advanced learning (9), remaining knowledge pipeline (11), remaining core utilities (6), and all other files (16)

### A.3 Context Brief

**What worked in Attempt 3:**
- Active learner collects user corrections
- Corrections stored in `data/training/intent_corrections.jsonl`
- Auto-retraining at 50 corrections threshold
- Content ingestion pipeline normalizes multiple formats (PDF, code, markdown, URL)
- Domain classification routes to 7 specialized extractors
- Knowledge synthesizer merges extractions with deduplication

**What failed or was never wired:**
- AutoRetrainingDaemon — complete pipeline, never instantiated at startup
- Effectiveness tracking existed but unclear if it measured real improvement
- Knowledge council, librarian, scheduler — built but integration status unclear
- 60+ files in src/learning/ — massive scope, unclear which are actually used
- Feature flag for research agent set to FALSE

**What was simulated/fake:**
- No specific evidence of fake learning capabilities, but effectiveness claims need verification

**Relevant Volume 0 principles:**
- P1: ML advises, symbolic core decides
- P3: Nothing ships without integration
- P4: Validation must be real
- L5: The memory system is the differentiator (learning + memory = the moat)
- A1: Feature factory without integration (60+ files, unclear integration)

### A.4 Known Failures & Warnings
1. **60+ files is scope explosion**: This is the largest module in the codebase. The distillation agent must aggressively triage — most of these files are candidates for DEFER or KILL in the initial rebuild.
2. **AutoRetrainingDaemon never started**: The complete pipeline existed but was never wired. Classic A1 pattern.
3. **Knowledge pipeline vs. learning pipeline**: These are conceptually different systems sharing a module. The distillation agent should determine if they belong in the same volume or if the knowledge pipeline belongs in Volume 5 (Intelligence).
4. **Engineering-specific extractors**: AutoCAD, MATLAB, FEA suite extractors exist because the user is a mechanical engineer PhD. These are high-value for the user but niche — determine rebuild priority.

---

## Part B: Design Specification (Agent Fills Out)

### B.1 Subsystem Purpose (Rebuild)

The Learning & Adaptation subsystem should make Atlas measurably smarter over time by closing the loop between user interaction and model/behavior improvement. It should: (1) collect explicit user corrections on intent classifications and implicit outcome signals from follow-up messages; (2) accumulate corrections until a data-driven trigger fires (threshold count, accuracy degradation, error-rate spike, staleness, coverage gap); (3) retrain the intent classifier using merged base + correction training data, validate accuracy improvement on a held-out test set, and deploy only if the new model is statistically better via A/B testing with Bonferroni-corrected hypothesis tests; (4) track whether the retraining cycle actually improved real-world classification accuracy (effectiveness measurement) and roll back if it did not; (5) learn behavioral patterns from command usage and user feedback to surface proactive suggestions and workflow automations; (6) persist all learned patterns and corrections through the memory system (L3 episodic, L4 declarative, L5 procedural, L7 world state) so learning survives restarts. The knowledge ingestion pipeline (content normalization -> domain classification -> extraction -> synthesis -> contradiction detection) also lives in this subsystem, producing `RefinedKnowledge` that Volume 5 (Intelligence) consumes for amplification. Every data boundary must be Pydantic-validated (P8). Retraining claims must be backed by real execution evidence (P4). The subsystem must degrade gracefully without an LLM (P1/R6) -- the symbolic/ML learning pipeline operates independently of any LLM provider.

### B.2 Architecture Overview

The subsystem has two major pipelines and one cross-cutting coordinator:

**Pipeline 1 -- Correction-Driven Learning (intent improvement)**
```
User correction -> ActiveLearner.record_correction()
                     |
              corrections.jsonl (append-only)
                     |
              TriggerDetector.check_all_triggers()
                     | (fires when threshold met)
              ModelTrainer.retrain()
                  +-- load base NLU data (Rasa YAML)
                  +-- merge with corrections (corrections win duplicates)
                  +-- train spaCy textcat model
                  +-- evaluate on held-out test set
                     |
              EffectivenessTracker.deploy_ab_test()
                  +-- ABTestOrchestrator routes traffic 50/50
                  +-- StatisticalAnalyzer compares accuracy, latency, error rate
                  +-- auto-promote if p < 0.05 (Bonferroni-corrected)
                     |
              ModelRegistry.promote_model() or rollback_model()
                  +-- persists state to L7
```

**Pipeline 2 -- Knowledge Ingestion (content -> structured knowledge)**
```
Raw content (file, URL, text, PDF)
     |
ContentIngester.ingest() -> NormalizedContent (Pydantic)
     |
DomainClassifier.classify() -> DomainClassification
     |
DomainToolRouter -> selects domain extractors
     |
Extractors (base Protocol) -> ExtractionResult per extractor
     |
KnowledgeSynthesizer.synthesize()
  +-- merge entities (deduplicate by normalized name)
  +-- merge relations (deduplicate by key tuple)
  +-- ContradictionDetector.check() (negation, numerical, semantic)
  +-- GapIdentifier.identify_gaps()
     |
RefinedKnowledge (Pydantic) -> stored in L4, handed to Vol 5
```

**Cross-cutting: LearningManager**
Coordinates PatternLearner (command patterns, workflow detection), FeedbackProcessor (user corrections), FixLearner (error-fix patterns), FeatureRequestDetector (implicit user needs from failed queries), ProposalLearner (self-modification outcome patterns), and PromptOptimizer (APEX adaptive prompts). Exposes `suggest_patterns()` as the read path for the orchestrator to incorporate learned patterns into responses.

**Key components and responsibilities:**
- `ActiveLearner` -- JSONL-based correction storage, threshold detection, stats
- `ModelTrainer` -- spaCy textcat training, train/test split, accuracy evaluation, model backup/deploy
- `ModelRegistry` -- thread-safe model version management, load/unload, promote/rollback, L7 state persistence
- `TriggerDetector` -- 5 trigger types checking memory layers (L3, L5, L7), configurable thresholds
- `EffectivenessTracker` -- A/B test lifecycle, statistical analysis integration, auto-promote/rollback
- `ABTestOrchestrator` -- traffic routing, metrics collection, inference result storage
- `StatisticalAnalyzer` -- z-test for accuracy, Mann-Whitney for latency, Fisher exact for error rate, Bonferroni correction
- `GroundTruthCollector` -- captures user corrections during A/B tests for true accuracy measurement
- `OutcomeDetector` -- implicit signal classification from user follow-up messages (positive/negative/neutral via keywords + overlap analysis)
- `LearningManager` -- facade coordinating PatternLearner, FeedbackProcessor, FixLearner, FeatureRequestDetector, ProposalLearner
- `ContentIngester` -- multi-format normalization (code, markdown, PDF, URL, JSON, event), SHA-256 dedup cache
- `DomainClassifier` -- keyword + optional L10 semantic scoring across 36 scientific domains
- `KnowledgeSynthesizer` -- entity/relation/fact merge, contradiction detection, gap identification
- `ContradictionDetector` -- negation patterns, numerical conflicts, semantic similarity with opposite polarity

### B.3 Interface Contracts

**3.1 ActiveLearner**
- Constructor: `ActiveLearner(corrections_file: Path, retraining_threshold: int = 50, min_confidence_for_ask: float = 0.6, max_confidence_for_ask: float = 0.8)`
- `record_correction(query: str, predicted_intent: str, correct_intent: str, confidence: float, session_id: str | None, user_id: str | None) -> None`
- `get_all_corrections() -> list[IntentCorrection]`
- `get_stats() -> dict` -- returns total_corrections, confirmations, actual_corrections, corrections_since_training, needs_retraining, corrections_by_intent
- `mark_training_completed() -> None` -- resets counter
- `trigger_retraining(classification_service, project_root: Path) -> dict`
- **Depends on:** filesystem (JSONL storage). In rebuild: should depend on L5 procedural memory via MemoryManager instead.
- **Consumed by:** ModelTrainer, OutcomeDetector, orchestrator (for recording corrections from conversation)

**3.2 ModelTrainer**
- Constructor: `ModelTrainer(project_root: Path, base_nlu_file: Path, model_output_dir: Path, active_learner: ActiveLearner, min_accuracy_improvement: float = 0.01)`
- `retrain(force: bool = False) -> dict` -- returns status, current_accuracy, new_accuracy, improvement, deployed, corrections_used, total_training_examples
- **Depends on:** ActiveLearner, spaCy, Rasa NLU YAML training data, filesystem for model storage
- **Consumed by:** AutoRetrainingDaemon, EffectivenessTracker

**3.3 ModelRegistry**
- Constructor: `ModelRegistry(memory_manager=None, base_path: Path | None = None)`
- `async load_model(model_name: str, model_path: Path, version_id: str | None, set_active: bool) -> LoadedModel`
- `get_active_model(model_name: str) -> LoadedModel | None`
- `async promote_model(model_name: str, new_version_path: Path, create_backup: bool = True) -> bool`
- `async rollback_model(model_name: str, target_version_id: str | None) -> bool`
- `unload_model(model_name: str, version_id: str) -> bool`
- **Depends on:** MemoryManager.L7 (state persistence), filesystem
- **Consumed by:** EffectivenessTracker, orchestrator intent pipeline

**3.4 TriggerDetector**
- Constructor: `TriggerDetector(memory_manager, model_path: Path | None)`
- `async check_all_triggers() -> list[RetrainingTrigger]`
- Trigger types: CORRECTION_THRESHOLD (>=50), ACCURACY_DEGRADATION (<95%), ERROR_RATE_SPIKE (>5%), STALENESS (>=30 days), COVERAGE_GAP (new intents)
- **Depends on:** MemoryManager (L3, L5, L7), filesystem (model metadata)
- **Consumed by:** AutoRetrainingDaemon

**3.5 EffectivenessTracker**
- Constructor: `LearningEffectivenessTracker(memory_manager=None, orchestrator=None, analyzer=None)`
- `deploy_ab_test(old_model_path: Path, new_model_path: Path, traffic_split: float, min_samples: int, max_duration_days: int) -> str` (test_id)
- `analyze_results(test_id: str | None) -> ABTestResults`
- `get_learning_patterns() -> dict`
- **Depends on:** ABTestOrchestrator, StatisticalAnalyzer, ModelRegistry, MemoryManager (L1 working, L4 declarative, L5 procedural)
- **Consumed by:** AutoRetrainingDaemon, health/stats endpoints

**3.6 OutcomeDetector**
- Constructor: `OutcomeDetector(learning_verifier=None, overlap_rephrase_threshold: float = 0.50, overlap_topic_change_threshold: float = 0.20)`
- `async analyze_follow_up(previous_query: str, previous_response: str, follow_up_message: str, provenance: dict | None, conversation_id: str) -> OutcomeSignal`
- Output schema: `OutcomeSignal` (from `src.memory.schemas`) with `signal_type: OutcomeType`, `confidence: float`, `indicators: list[str]`, `provenance: dict`
- **Depends on:** LearningVerifier (optional), ActiveLearner (optional, for feeding negative outcomes back), OutcomeSignal/OutcomeType schemas from Volume 1
- **Consumed by:** Orchestrator conversation loop (called after each response with the next user message)

**3.7 LearningManager (facade)**
- Constructor: `LearningManager(data_dir: Path | None, memory_manager=None)`
- `record_command_execution(command: str, success: bool) -> None`
- `record_user_correction(original: str, corrected: str, notes: str) -> None`
- `suggest_patterns(trigger: str, context: dict | None, limit: int) -> list[dict]` -- returns patterns with trigger, action, confidence, type
- `record_proposal_outcome(proposal_id, proposal_type, status, ...) -> dict` -- returns insights
- `get_stats() -> dict` -- comprehensive learning statistics
- `save_patterns() -> None` -- persist to L5
- `close() -> None` -- shutdown hook
- **Depends on:** PatternLearner, FeedbackProcessor, FixLearner, FeatureRequestDetector, ProposalLearner, PromptOptimizer, MemoryManager
- **Consumed by:** Orchestrator (for pattern suggestions during response generation), self-modification pipeline (for proposal outcome recording)

**3.8 ContentIngester**
- Constructor: `ContentIngester()`
- `async ingest(source: str | Path | bytes, content_type: ContentType, metadata: dict | None, source_url: str | None) -> NormalizedContent`
- ContentType enum: CODE, MARKDOWN, PDF, URL, JSON, TEXT, EVENT
- Output: `NormalizedContent` (from `src.memory.schemas`) -- raw_text, content_type, source, content_hash, metadata
- **Depends on:** pypdf (optional), httpx + beautifulsoup4 (optional), filesystem
- **Consumed by:** KnowledgeEngine, knowledge pipeline entry point

**3.9 DomainClassifier**
- Constructor: `DomainClassifier(memory=None, keyword_weight: float = 0.7, semantic_weight: float = 0.3)`
- `async classify(content: str, top_k: int = 3) -> DomainClassification`
- Output: `DomainClassification` -- domain: ScientificDomain, confidence: float, all_scores: dict, method: str
- 36 scientific domains in ScientificDomain enum (physics, chemistry, biology, math, CS, engineering, cross-disciplinary)
- **Depends on:** MemoryManager.L10 (optional, for semantic scoring), DOMAIN_KEYWORDS dict
- **Consumed by:** DomainToolRouter, KnowledgeEngine

**3.10 KnowledgeSynthesizer**
- Constructor: `KnowledgeSynthesizer(contradiction_detector=None, gap_identifier=None, memory_manager=None)`
- `async synthesize(extractions: list[ExtractionResult]) -> RefinedKnowledge`
- `async synthesize_full(extractions: list[ExtractionResult]) -> SynthesizedKnowledge` (includes gap identification)
- Output schemas: `RefinedKnowledge` (knowledge_id, domain, entries, graph_edges, contradictions_found/resolved), `SynthesizedKnowledge` (entities, relations, facts, gaps, contradictions)
- **Depends on:** ContradictionDetector, GapIdentifier, MemoryManager (for semantic dedup via FAISS)
- **Consumed by:** KnowledgeEngine, Volume 5 Intelligence pipeline

**3.11 ContradictionDetector**
- Constructor: `ContradictionDetector(memory=None, similarity_threshold: float = 0.7)`
- `async check(new_entry: DomainKnowledgeEntry, existing_entries: list[DomainKnowledgeEntry]) -> ContradictionResult`
- Output: `ContradictionResult` -- has_contradiction, conflicting_entry_id, conflict_type (DIRECT_NEGATION, NUMERICAL_CONFLICT, SEMANTIC_CONFLICT, TEMPORAL_CONFLICT), confidence, auto_resolvable
- **Depends on:** MemoryManager (optional, for semantic comparison)
- **Consumed by:** KnowledgeSynthesizer

**3.12 DomainExtractor Protocol (base)**
- `async extract(content: NormalizedContent) -> ExtractionResult`
- `domain: ScientificDomain` (class attribute)
- **Consumed by:** DomainToolRouter

**Cross-volume interface summary:**
- **Consumes from Volume 1 (Memory):** MemoryManager, L3 (episodes), L4 (facts), L5 (procedural patterns), L7 (world state snapshots), L10 (vector/semantic search). Pydantic schemas: NormalizedContent, ContentType, DomainClassification, ScientificDomain, ExtractionResult, ExtractedEntity, ExtractedRelation, RefinedKnowledge, SynthesizedKnowledge, DomainKnowledgeEntry, ContradictionResult, ConflictType, OutcomeSignal, OutcomeType, Fact, FactSource, KnowledgeGap, Contradiction, etc.
- **Consumes from Volume 2 (Orchestrator):** Intent classification results (predicted_intent, confidence) as input to ActiveLearner and OutcomeDetector
- **Consumes from Volume 9 (Governance):** DecisionValidator for validating learning actions before execution
- **Provides to Volume 2 (Orchestrator):** `LearningManager.suggest_patterns()` -- learned behavioral patterns for response augmentation; `OutcomeDetector.analyze_follow_up()` -- quality signal for the previous response
- **Provides to Volume 4 (Self-Modification):** `LearningManager.record_proposal_outcome()` -- learning from self-modification outcomes; `LearningManager.should_generate_proposal()` -- learned advisory on whether to attempt a proposal
- **Provides to Volume 5 (Intelligence):** `RefinedKnowledge` as output of the knowledge ingestion pipeline; `DomainClassification` for routing decisions
- **Provides to Volume 8 (API):** Stats and health endpoints for learning subsystem status

### B.4 Scope Triage

**Legend:** REBUILD = include in Atlas v4 rebuild. DEFER = valuable but not for initial release; build after MVA passes. KILL = remove, no rebuild value.

**Core learning (14 files):**
- `active_learner.py` -- **REBUILD**. Core correction collection. Simplify: replace JSONL file storage with L5 memory layer, use Pydantic IntentCorrection instead of dataclass.
- `auto_retrain_daemon.py` -- **REBUILD**. Never wired in Attempt 3 (A.4 #2). The design intent is correct -- periodic background trigger checking and retraining. Rebuild as a lightweight async task, not a heavyweight daemon.
- `effectiveness_tracker.py` -- **REBUILD**. Critical for P4 (validation must be real). Proves retraining actually helps. Simplify: reduce coupling to ABTestOrchestrator internals.
- `effectiveness_coordinator.py` -- **KILL**. Orchestration layer on top of EffectivenessTracker that adds indirection without value. Fold any unique logic into EffectivenessTracker.
- `feedback_processor.py` -- **REBUILD**. Simple and clean. In-memory correction pattern tracking. Add persistence to L5.
- `learning_manager.py` -- **REBUILD**. Good facade pattern. Remove PromptOptimizer and FixLearner sub-components initially; add back as DEFER.
- `learning_scheduler.py` -- **DEFER**. Autonomous background learning cycles -- valuable but not needed for MVA-4. Build after core learning loop works.
- `learning_verifier.py` -- **DEFER**. Validates learning improves performance -- overlaps with EffectivenessTracker. Consolidate into one component during Phase 2.
- `model_trainer.py` -- **REBUILD**. Core retraining pipeline. Decouple from spaCy-specific API; use an abstract TrainerProtocol so the model framework can be swapped.
- `model_registry.py` -- **REBUILD**. Thread-safe model version management with L7 persistence. Clean design. Remove placeholder `predict()` in LoadedModel; real model loading needed.
- `retrain_triggers.py` -- **REBUILD**. 5 trigger types, well-designed Pydantic schemas. Reduce dependency on specific L5/L7 method signatures -- use MemoryManager facade.
- `ab_testing.py` -- **REBUILD**. A/B test orchestration with ModelVersion, ABTestConfig, inference routing. Needed for EffectivenessTracker.
- `ab_testing_classification_service.py` -- **DEFER**. Classification service wrapper for A/B routing. Can be built after core A/B testing works.
- `outcome_detector.py` -- **REBUILD**. Implicit outcome signal detection is high-value for closing the learning loop without requiring explicit user corrections. Keyword + overlap approach is simple and effective.

**Knowledge pipeline (16 files):**
- `content_ingester.py` -- **REBUILD**. Clean multi-format normalization with Pydantic output. Essential entry point for knowledge pipeline.
- `domain_classifier.py` -- **REBUILD**. 36-domain keyword classification with optional L10 semantic scoring. Well-structured. Trim domain list to ~10 most relevant domains initially.
- `domain_tool_router.py` -- **REBUILD**. Routes content to appropriate extractors by domain. Simple dispatch logic.
- `knowledge_synthesizer.py` -- **REBUILD**. Entity/relation/fact merge with deduplication and contradiction detection. Core knowledge pipeline component.
- `knowledge_graph.py` -- **DEFER**. Graph-based knowledge representation. Valuable for cross-domain connections but not needed for MVA-4.
- `knowledge_engine.py` -- **DEFER**. Top-level orchestrator for the full knowledge pipeline. Heavy -- 5+ patterns, many sub-components. Build after individual pipeline components work.
- `knowledge_council.py` -- **KILL**. Federated knowledge aggregation -- built but integration status unclear (A.4 #3). Over-engineered for current needs.
- `knowledge_librarian.py` -- **KILL**. Chat-based knowledge browsing interface -- novel but not core learning functionality.
- `knowledge_scheduler.py` -- **DEFER**. Background knowledge processing tasks. Valuable for autonomous ingestion but not for MVA-4.
- `knowledge_versioning.py` -- **DEFER**. Knowledge version management (rollback, diff). Valuable for safety but not initial priority.
- `knowledge_extractor.py` -- **DEFER**. Multi-language code analysis (Python AST + TypeScript regex + JSON). High-value for user but not for MVA-4 learning round-trip.
- `contradiction_detector.py` -- **REBUILD**. Negation pattern, numerical conflict, and semantic contradiction detection. Essential for knowledge integrity.
- `gap_identifier.py` -- **DEFER**. Knowledge gap identification. Useful for proactive learning but not critical path.
- `semantic_graph.py` -- **DEFER**. Cross-domain knowledge transfer via semantic graph. Phase 3+ capability.
- `cross_layer_linker.py` -- **DEFER**. Memory layer cross-referencing. Belongs more to Volume 1 (Memory) -- flag as potential ownership conflict.
- `hybrid_retriever.py` -- **DEFER**. Multi-source retrieval (FTS5, FAISS, graph). Belongs partially to Volume 1 -- flag as potential ownership conflict.

**Domain extractors (13 files):**
- `extractors/base.py` -- **REBUILD**. DomainExtractor Protocol definition. Required for any extractor.
- `extractors/general.py` -- **REBUILD**. General-purpose extractor as fallback. Required.
- `extractors/atlas_self.py` -- **DEFER**. Self-knowledge extraction -- meta-capability, not initial priority.
- `extractors/chemistry.py` -- **DEFER**. Chemistry-specific extraction (ChemDataExtractor integration).
- `extractors/physics.py` -- **DEFER**. Physics-specific extraction.
- `extractors/biology.py` -- **DEFER**. Biology-specific extraction.
- `extractors/materials.py` -- **DEFER**. Materials science extraction.
- `extractors/engineering.py` -- **DEFER**. Engineering-specific extraction. High-value for user (mechanical engineer PhD) -- prioritize after general extractor works.
- `extractors/earth_science.py` -- **DEFER**. Earth science extraction.
- `extractors/autocad.py` -- **DEFER**. AutoCAD-specific extraction. Very niche but high-value for user (A.4 #4).
- `extractors/matlab.py` -- **DEFER**. MATLAB-specific extraction. High-value for user.
- `extractors/fea_suite.py` -- **DEFER**. FEA suite extraction. High-value for user.
- `extractors/rate_limiter.py` -- **DEFER**. Rate limiting for extractors -- utility, build when extractors are active.

**Advanced learning (9 files):**
- `pattern_learner.py` -- **REBUILD**. Command pattern tracking, workflow detection. Used by LearningManager. Core behavioral learning.
- `pattern_matching.py` -- **DEFER**. Pattern matching with semantic graph integration. Advanced capability.
- `principle_abstractor.py` -- **DEFER**. Extracts abstract principles from code patterns. Meta-learning capability.
- `concept_builder.py` -- **DEFER**. Builds concept hierarchies. Meta-learning.
- `abstraction_engine.py` -- **DEFER**. Orchestrates principle abstraction + concept building. Meta-learning.
- `domain_transfer.py` -- **DEFER**. Cross-domain knowledge transfer. Phase 3+ capability per Volume 0 S3.3.
- `domain_knowledge_base.py` -- **DEFER**. Domain-specific knowledge storage.
- `prompt_optimizer.py` -- **DEFER**. APEX adaptive prompt strategies. Requires L5 procedural memory maturity.
- `hyperparameter_optimizer.py` -- **DEFER**. Hyperparameter tuning for retraining. Optimization, not core.

**Other (18 files):**
- `schemas.py` -- **REBUILD**. Core Pydantic schemas (LearningSource, FeatureRequest, CommandPatternData, ProposalOutcome, LearnedPattern, LabeledSample, ABTestMetrics, EffectivenessReport). Migrate to atlas.learning.schemas.
- `errors.py` -- **REBUILD**. Error taxonomy (ExtractionError, IngestionError, SynthesisError, ContradictionError, RouterError, RetrievalError, SchedulerError, VersioningError). Migrate to atlas.learning.errors inheriting from atlas.shared.errors.
- `consolidation.py` -- **DEFER**. Event bus integration for pattern consolidation. Build after event bus exists.
- `code_explainer.py` -- **KILL**. Code explanation utility -- not learning functionality. Belongs in tools (Volume 10) if rebuilt.
- `documentation_exporters.py` -- **KILL**. Documentation export -- not learning functionality.
- `feature_detector.py` -- **DEFER**. Feature request detection from user behavior. Valuable but not MVA-4.
- `file_watcher.py` -- **KILL**. File system watching -- not learning functionality. Belongs in tools.
- `fix_learner.py` -- **DEFER**. Error-fix pattern learning. Valuable for self-modification but not initial priority.
- `human_review.py` -- **DEFER**. Human review queue for contradictions. Build when contradiction handling matures.
- `intelligence_learning_engine.py` -- **KILL**. Overlaps with knowledge_engine.py. Consolidate.
- `memory_guard.py` -- **KILL**. Memory validation guard -- belongs in Volume 1 (Memory) or Volume 9 (Governance), not learning.
- `proposal_learner.py` -- **DEFER**. Self-modification outcome learning. Build when Volume 4 exists.
- `skill_router.py` -- **KILL**. Skill routing -- overlaps with orchestrator intent routing (Volume 2).
- `statistical_analysis.py` -- **REBUILD**. Statistical hypothesis testing (z-test, Mann-Whitney, Fisher exact, Bonferroni). Required by EffectivenessTracker.
- `system_scaffolder.py` -- **KILL**. System scaffolding utility -- not learning functionality.
- `db_migrations.py` -- **DEFER**. Database migration scripts for learning tables. Build when schema stabilizes.
- `ai_agent_failure_patterns.py` -- **KILL**. AI failure pattern documentation -- informational, not executable code.
- `architecture_experimenter.py` -- **KILL**. Architecture experimentation -- meta-capability, not learning.

**Triage summary:** 70 files total. REBUILD: 20 files. DEFER: 32 files. KILL: 18 files. The 20 REBUILD files form a coherent minimal learning subsystem capable of passing MVA-4 (correct a classification, verify persistence).

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
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (60+ code files, 10+ docs), context brief, and 4 known failure warnings including scope explosion and never-started AutoRetrainingDaemon | Created the learning system analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V03-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 source manifest per DISTILLATION_PROTOCOL.md Section 5 | Tagged files as essential vs. nice-to-have for the rebuild analysis |
| v5 | 2026-03-10 | Oz Phase 1 Vol 3 Agent | Phase 1 distillation complete — filled B.1 (purpose), B.2 (architecture with two pipelines + facade), B.3 (12 interface contracts with full signatures), B.4 (scope triage: 20 REBUILD, 32 DEFER, 18 KILL) | The analysis agent read all 70 source files and wrote the technical specification for what to rebuild and what to drop |
