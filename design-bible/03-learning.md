# ATLAS Design Bible — Volume 3: Learning & Adaptation

| Field | Value |
|---|---|
| **Doc ID** | `DB-V03-001` |
| **Name** | Volume 3: Learning & Adaptation |
| **Purpose** | Design specification for the active learning, correction pipeline, retraining, and knowledge ingestion systems |
| **Owner** | Design Bible / Volume 3 |
| **Status** | `draft` (scaffold — Part A pre-loaded, Part B awaiting distillation agent) |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / TBD distillation agent (Part B) |
| **Version** | v4 |
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
*[To be filled by distillation agent]*

### B.2 Architecture Overview
*[To be filled by distillation agent]*

### B.3 Interface Contracts
*[To be filled by distillation agent]*

### B.4 Scope Triage
*[To be filled by distillation agent — every component in A.2 must get a REBUILD/DEFER/KILL verdict]*

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
