# Agent Communication — Volume 3: Learning & Knowledge

> **Rules:** Append new claims/dependencies/conflicts using the formats defined in `AGENT_COMM.md`.
> This file is the ONLY place Vol 3 agents register changes. Do NOT edit `AGENT_COMM.md` directly.

---

## Ownership Claims

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

```
CLAIM: APEX schemas (PromptStrategy, PromptMetrics, TaskOutcome, TurnAnalysis, PromptStrategyStatus)
OWNER: Volume 3/5 boundary (currently in src/memory/schemas.py, must move in rebuild)
REASON: Prompt optimization schemas belong to the learning/intelligence boundary, not memory.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 3 (Learning) needs L4.search_facts(), L5 procedural store, L3.store_episode() from Volume 1
STATUS: pending
INTERFACE: L4DeclarativeMemory.search_facts(query, limit) -> list[dict]; L5ProceduralMemory.store_skill(Skill); L3EpisodicMemory.store_episode(Episode)
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
DEPENDENCY: Volume 3 needs proposal outcomes from Volume 4
STATUS: pending
INTERFACE: ImprovementProposal with status, risk_assessment, ValidationClaim records in L4
```

---

## Conflict Acknowledgements

```
CONFLICT: cross_layer_linker.py — memory infrastructure, not learning
VOLUMES: 3 vs 1
RESOLUTION: resolved — Vol 1 owns (conflict-report.md C-04)
```

```
CONFLICT: hybrid_retriever.py — memory retrieval infrastructure, not learning
VOLUMES: 3 vs 1
RESOLUTION: resolved — Vol 1 owns (conflict-report.md C-05)
```

```
CONFLICT: Knowledge-pipeline Pydantic schemas location
VOLUMES: 3 vs 1
RESOLUTION: resolved — learning-pipeline schemas → Vol 3. Shared schemas stay Vol 1 (conflict-report.md C-02)
```

```
CONFLICT: memory_guard.py ownership
VOLUMES: 3 vs 1 vs 9
RESOLUTION: resolved — Vol 1 owns (conflict-report.md C-06)
```
