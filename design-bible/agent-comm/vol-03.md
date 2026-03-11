# Agent Communication — Volume 3: Learning & Adaptation
## Phase 2 Distillation Outputs

---

## Ownership Claims

```
CLAIM: Knowledge-pipeline Pydantic schemas (NormalizedContent, ContentType, DomainClassification, ScientificDomain, ExtractionResult, ExtractedEntity, ExtractedRelation, RefinedKnowledge, SynthesizedKnowledge, DomainKnowledgeEntry, ContradictionResult, ConflictType)
OWNER: Volume 3
REASON: Per C-02 resolution, knowledge-pipeline-specific schemas move from memory/schemas.py to learning/schemas.py. Vol 3 is the owner going forward.
CONTESTED: no (resolved by C-02)
```

```
CLAIM: Learning-domain Pydantic schemas (IntentCorrection, LabeledSample, LearningSource, TrainingConfig, TrainedModel, EvaluationResult, ModelVersion, ABTestConfig, ABTestStatus, ABTestWinner, ABTestRecommendation, InferenceResult, ModelMetrics, ABTestResults, TriggerType, RetrainingTrigger, CommandPatternData, LearnedPattern, FeatureRequest, ProposalOutcome, EffectivenessReport)
OWNER: Volume 3
REASON: All Pydantic schemas specific to the learning subsystem's correction pipeline, training pipeline, A/B testing, triggers, and behavioral learning.
CONTESTED: no
```

```
CLAIM: Learning error hierarchy (LearningError, ExtractionError, IngestionError, SynthesisError, ContradictionError, RetrainError, RegistryError, TriggerError)
OWNER: Volume 3
REASON: Error types specific to the learning subsystem. All inherit from AtlasError (shared/errors.py, Vol 8).
CONTESTED: no
```

```
CLAIM: TrainerProtocol (abstract ML training interface)
OWNER: Volume 3
REASON: Protocol decoupling training logic from framework-specific implementation. Initial implementation: SpacyTextcatTrainer. Defined in atlas.learning.
CONTESTED: no
```

```
CLAIM: EffectivenessCoordinator
OWNER: KILL
REASON: Redundant orchestration layer over EffectivenessTracker. deploy_ab_test_for_model() folded into EffectivenessTracker in rebuild.
CONTESTED: no
```

```
CLAIM: APEX schemas (PromptStrategy, PromptMetrics, PromptStrategyStatus, TaskOutcome, TurnAnalysis)
OWNER: Volume 3 (DEFER)
REASON: Per Phase 1 claim, APEX schemas belong to Vol 3/5 boundary. Currently in memory/schemas.py. Deferred until L5 procedural memory matures.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 3 needs AtlasError base class from shared/errors.py (Volume 8)
STATUS: pending
INTERFACE: class AtlasError(Exception) with subsystem, context, severity. LearningError inherits from it.
```

```
DEPENDENCY: Volume 3 needs AtlasConfig from shared/config.py (Volume 8) for ATLAS_LEARNING_* env vars
STATUS: pending
INTERFACE: AtlasConfig(BaseSettings) with env_prefix="ATLAS_". Learning reads 22 config fields specified in B.9.
```

```
DEPENDENCY: Volume 3 needs structlog from shared/logging.py (cross-cutting)
STATUS: pending
INTERFACE: from atlas.shared.logging import get_logger -> structlog.BoundLogger
```

```
DEPENDENCY: Volume 3 needs MemoryManager (L3, L4, L5, L7, L10) from Volume 1
STATUS: pending
INTERFACE: MemoryManager.l3.store_episode(Episode); MemoryManager.l4.search_facts(query, limit); MemoryManager.l5.store_skill(Skill); MemoryManager.l7 (world state); MemoryManager.l10 (vector search)
```

```
DEPENDENCY: Volume 3 needs OutcomeSignal and OutcomeType schemas from Volume 1
STATUS: pending
INTERFACE: OutcomeSignal(BaseModel), OutcomeType(str, Enum) — defined in Vol 1 schemas.py, consumed by OutcomeDetector
```

```
DEPENDENCY: Volume 3 needs intent classification results from Volume 2
STATUS: pending
INTERFACE: UnifiedIntent schema with at minimum: category, confidence, classification_source
```

```
DEPENDENCY: Volume 3 needs DecisionValidator from Volume 9 for governance of learning actions
STATUS: pending
INTERFACE: DecisionValidator.validate(action, context) -> ValidationDecision
```

```
DEPENDENCY: Volume 3 needs ImprovementProposal and ProposalStatus from Volume 4 (for ProposalLearner, DEFERRED)
STATUS: pending
INTERFACE: ImprovementProposal(BaseModel) with status, risk_assessment, affected_components
```

```
DEPENDENCY: Volume 1 needs NLP/LLM extraction strategy from Volume 3 for MemoryConsolidator._extract_facts_from_messages()
STATUS: acknowledged
INTERFACE: Callable[[list[dict]], list[Fact]] — Vol 3 supplies extraction logic for consolidation (discovered in Vol 1 Phase 2)
```

---

## Conflict Acknowledgements

```
CONFLICT: C-02 — Knowledge-pipeline schema location
STATUS: resolved
RESOLUTION: Vol 3 owns knowledge-pipeline schemas in atlas/learning/schemas.py. Vol 1 provides thin re-exports during migration.
VOL 3 ACTION: Define NormalizedContent, ExtractionResult, DomainClassification, RefinedKnowledge, SynthesizedKnowledge, DomainKnowledgeEntry, ContradictionResult, ConflictType in learning/schemas.py.
```

```
CONFLICT: C-04 — cross_layer_linker.py ownership
STATUS: resolved
RESOLUTION: Assigned to Vol 1 (Memory). Vol 3 DEFERed correctly in B.4.
VOL 3 ACTION: None — removed from Vol 3 scope.
```

```
CONFLICT: C-05 — hybrid_retriever.py ownership
STATUS: resolved
RESOLUTION: Assigned to Vol 1 (Memory). Vol 3 DEFERed correctly in B.4.
VOL 3 ACTION: None — removed from Vol 3 scope.
```

```
CONFLICT: C-06 — memory_guard.py ownership
STATUS: resolved
RESOLUTION: Assigned to Vol 9 (Governance). Vol 3 KILLed correctly in B.4.
VOL 3 ACTION: None — removed from Vol 3 scope.
```

---

## Discoveries for Other Volumes

**For Volume 1:**
- B.11.6: C-02 migration creates a task for Vol 1 — thin re-exports of knowledge-pipeline schemas during transition period.
- B.6.2: Vol 3 consumes OutcomeSignal/OutcomeType from Vol 1 schemas (confirmed, does not redefine).
- B.9: Vol 3 acknowledged Vol 1's consolidation dependency — Vol 3 must provide fact extraction logic (Callable[[list[dict]], list[Fact]]).

**For Volume 2:**
- B.3.7: `LearningManager.suggest_patterns()` is the read path for incorporating learned behavioral patterns into response generation. Returns patterns sorted by confidence.
- B.3.6: `OutcomeDetector.analyze_follow_up()` should be called after each response with the next user message. Returns OutcomeSignal with signal_type, confidence, indicators.

**For Volume 4:**
- B.3.7: `LearningManager.record_proposal_outcome()` accepts ProposalOutcome and returns insights dict. Vol 4 should call this after every proposal apply/reject.
- B.3.7: `LearningManager.should_generate_proposal()` uses learned patterns to advise whether a proposal type is worth attempting.

**For Volume 5:**
- B.3.10: `RefinedKnowledge` is the output of the knowledge ingestion pipeline, produced by `KnowledgeSynthesizer.synthesize()`. Vol 5 consumes this via L4 memory queries.
- B.11.2: APEX PromptOptimizer is DEFERRED as a self-contained unit. When rebuilt, its schemas (currently in memory/schemas.py) should move to learning/schemas.py per Vol 3 ownership.

**For Volume 8:**
- B.9: Vol 3 defines 22 ATLAS_LEARNING_* environment variables that must be registered in AtlasConfig. Feature flags default OFF per Volume 0 R7.
- B.3.8: Learning health/stats endpoints needed: `GET /v1/learning/stats`, `GET /v1/learning/effectiveness`.

**For Volume 9:**
- B.7: All learning actions that modify system state (retrain, promote, rollback) must pass through DecisionValidator. Vol 3 depends on this gate.
- B.8.3: "No learning action executes without passing DecisionValidator governance check" is a critical test invariant.

---

## Phase 2 B.4 Verdict Amendments

**EffectivenessCoordinator reclassification:** B.4 Phase 1 assigned KILL verdict. Phase 2 deep dive confirmed this is correct — the component is a thin orchestration wrapper over EffectivenessTracker + ABTestOrchestrator + StatisticalAnalyzer. The one useful method (`deploy_ab_test_for_model`) is absorbed into EffectivenessTracker. KILL verdict retained.

**statistical_analysis.py reclassification:** B.4 Phase 1 classified this under "Other" as REBUILD. Phase 2 confirms it is a critical dependency of the A/B testing pipeline — the `StatisticalAnalyzer` class with Z-test, Welch's t-test, Cohen's d, and Bonferroni correction is required for any model promotion decision. REBUILD verdict confirmed and elevated to "Core learning" group.

---

## Modification History

| Version | Date | Modified By | Summary |
|---|---|---|---|
| v1 | 2026-03-11 | Distillation Agent V3 (Phase 2) | Initial creation — 6 ownership claims (knowledge-pipeline schemas per C-02, learning-domain schemas, error hierarchy, TrainerProtocol, EffectivenessCoordinator KILL, APEX schemas DEFER), 9 dependency declarations (Vol 1/2/4/8/9), 4 conflict acknowledgements (C-02/C-04/C-05/C-06), cross-volume notifications for Vol 1/2/4/5/8/9, 2 B.4 verdict amendments |
