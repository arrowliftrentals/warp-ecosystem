# Agent Communication — Volume 5: Intelligence Pipeline
## Phase 2 Distillation Outputs

---

## Ownership Claims

```
CLAIM: IntelligenceCoordinator (intelligence/coordinator.py) — unified facade for all amplification
OWNER: Volume 5
REASON: Core subsystem entry point. Composes AnalogicalReasoner, HypothesisGenerator, SocraticChallenger, GrowthTracker behind async API. Single point of contact for Vol 2 orchestrator.
CONTESTED: no
```

```
CLAIM: AnalogicalReasoner (intelligence/analogical_reasoner.py) — cross-domain structural mapping
OWNER: Volume 5
REASON: Maintains canonical analogy registry, novel discovery via L10, and knowledge transfer with provenance. Pure intelligence-domain component.
CONTESTED: no
```

```
CLAIM: HypothesisGenerator (intelligence/hypothesis_generator.py) — gap identification + hypothesis creation
OWNER: Volume 5
REASON: Scans L4 for 4 gap types, produces Hypothesis objects with falsification criteria and calibrated confidence. Intelligence-specific reasoning.
CONTESTED: no
```

```
CLAIM: SocraticChallenger (intelligence/socratic_challenger.py) — constructive reasoning challenges
OWNER: Volume 5
REASON: Analyzes claims for contradiction/assumption/missing-evidence/scope issues. Tracks resolutions, adapts challenge frequency. Intelligence-specific component.
CONTESTED: no
```

```
CLAIM: GrowthTracker (intelligence/growth_tracker.py) — user intellectual development tracking
OWNER: Volume 5
REASON: Maintains IntellectualProfile in L9, tracks domain mastery, concept progression, blind spots, growth trajectory. Intelligence-specific user modeling.
CONTESTED: no
```

```
CLAIM: Intelligence result schemas (intelligence/schemas.py) — AmplificationResult, CrossDomainResult, ChallengeResult, ResearchAgenda, IntellectualSummary
OWNER: Volume 5
REASON: These are intelligence-specific response containers that compose Vol 1 base schemas. They do not cross into memory storage — they are returned by coordinator methods to Vol 2 orchestrator. Per C-03, Vol 1 owns the base data schemas (StructuralAnalogy, Hypothesis, etc.) and Vol 5 owns these result wrappers.
CONTESTED: no
```

```
CLAIM: Canonical analogies data (CANONICAL_ANALOGIES constant in analogical_reasoner.py)
OWNER: Volume 5
REASON: Static domain knowledge (thermal↔electrical, mechanical↔electrical, evolution↔optimization, quantum↔computing) embedded as Pydantic-validated StructuralAnalogy instances. Purely intelligence-domain reference data.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 5 (Intelligence) needs MemoryManager from Volume 1
STATUS: pending
INTERFACE: MemoryManager providing L4 (declarative facts), L9 (user profiles), L10 (vector search), L3 (episodic)
NOTE: L4 — fact retrieval for analogies, gap detection, contradiction checks. L9 — IntellectualProfile read/write. L10 — semantic similarity for novel analogy discovery. L3 — SocraticChallenger records resolution episodes. All memory access is optional; components degrade gracefully to empty results if unavailable.
```

```
DEPENDENCY: Volume 5 (Intelligence) needs AtlasError base class from shared/errors.py (Volume 8)
STATUS: pending
INTERFACE: class AtlasError(Exception) — base for error hierarchy. Also MemoryLayerError, ValidationError.
NOTE: Intelligence uses shared error hierarchy, no subsystem-specific error subclass needed. B.7 specifies 3 error types, 5 propagation rules.
```

```
DEPENDENCY: Volume 5 (Intelligence) needs AtlasConfig from shared/config.py (Volume 8)
STATUS: pending
INTERFACE: AtlasConfig(BaseSettings) with env_prefix="ATLAS_". Intelligence reads ATLAS_ENABLE_INTELLIGENCE, ATLAS_INTELLIGENCE_MIN_SIMILARITY, ATLAS_INTELLIGENCE_CHALLENGE_THRESHOLD, ATLAS_INTELLIGENCE_GROWTH_DECAY_RATE, ATLAS_INTELLIGENCE_MAX_ANALOGIES, ATLAS_INTELLIGENCE_MAX_CHALLENGES, ATLAS_INTELLIGENCE_MAX_GAPS, ATLAS_INTELLIGENCE_TRAJECTORY_MAX, ATLAS_INTELLIGENCE_TRAJECTORY_KEEP.
```

```
DEPENDENCY: Volume 5 (Intelligence) needs structlog from shared/logging.py (cross-cutting)
STATUS: pending
INTERFACE: from atlas.shared.logging import get_logger -> structlog.BoundLogger
NOTE: Replaces Attempt 3's loguru. Per PROJECT_CONVENTIONS.md Section 7.
```

```
DEPENDENCY: Volume 5 (Intelligence) needs IntellectualProfile as first-class field on Volume 1's UserProfile schema
STATUS: pending — requires Vol 1 schema update
INTERFACE: UserProfile.intellectual_profile: IntellectualProfile | None (L9 social memory)
NOTE: Currently stored in user_profile.metadata['intellectual_profile'] (untyped dict, magic key). B.10 L-INT-05 documents this as fragile. Rebuild needs Vol 1 to promote IntellectualProfile from metadata dict to typed field on UserProfile. This is a schema change request, not a code dependency.
```

---

## Conflict Flags

```
CONFLICT ACKNOWLEDGEMENT: C-03 (Intelligence Data Schema Ownership — Vol 1 vs Vol 5)
VOLUMES: 1 vs 5
DESCRIPTION: Already resolved. Vol 1 (Memory) owns the base Pydantic schemas (StructuralAnalogy, Hypothesis, ResearchGap, SocraticChallenge, IntellectualProfile, CalibratedConfidence, ProvenanceChain, ProvenanceStep) because they cross the memory boundary. Vol 5 consumes them and owns result wrapper schemas (AmplificationResult, CrossDomainResult, ChallengeResult, ResearchAgenda, IntellectualSummary).
STATUS: resolved (no action needed)
```

```
CONFLICT ACKNOWLEDGEMENT: C-08 (OperationalDiagnostician Location — Vol 5 vs Vol 9/Vol 4)
VOLUMES: 5 vs 9, 4
DESCRIPTION: Already resolved. OperationalDiagnostician + InvariantEvaluator move to Vol 9 (Governance). RemediationEngine moves to Vol 4 (Self-Modification). All three are DEFER'd in Vol 5 B.4. Source imports confirm governance/infrastructure nature (src.memory.schemas_diagnostics, src.introspection.self_model).
STATUS: resolved (no action needed)
```

---

## Discoveries for Other Volumes

**For Volume 0:**
- D-INT-01: The amplification layer is the purest R6 (model independence) implementation across all volumes — zero LLM dependency, entirely symbolic + memory-based. Recommend as gold standard reference for R6 compliance evaluation.
- D-INT-02: Two-layer contradiction detection (cheap heuristic → expensive semantic) is a reusable pattern. Recommend promoting to `atlas/shared/text.py` as a utility.

**For Volume 1:**
- D-INT-05/L-INT-05: IntellectualProfile needs to become a first-class field on UserProfile schema in L9 (see dependency declaration above).
- D-INT-03: Growth trajectory truncation (1000→500) drops oldest entries without summarization. Same pattern may affect L3 episodic consolidation — consider consolidated summary approach.

**For Volume 2:**
- IntelligenceCoordinator exposes 3 primary methods consumed by the orchestrator: `amplify_query()`, `cross_domain_insight()`, `challenge_and_refine()`. Two secondary methods (`generate_research_agenda()`, `get_intellectual_summary()`) are not orchestrator-invoked — they may be exposed via API routes (Vol 8) or tools (Vol 10) in the future.

**For Volume 3:**
- D-INT-05: Acquisition layer (4 DEFER files) feeds directly into Vol 3's ContentIngester. Boundary is clean: `QueueItem` → `ContentIngester.ingest()` → `RefinedKnowledge`. No intelligence-specific logic in acquisition. When acquisition is rebuilt, coordinate with Vol 3.
- D-INT-02: Two-layer contradiction detection is applicable to Vol 3 for detecting contradictory learned facts.

**For Volume 4:**
- C-08: RemediationEngine from operational_diagnostics.py (DEFER) moves to Vol 4 when self-modification pipeline is ready.

**For Volume 8:**
- shared/errors.py must define AtlasError, MemoryLayerError, ValidationError before Vol 5 can build. Tier 0 dependency.
- shared/config.py must define AtlasConfig(BaseSettings) with env_prefix support before Vol 5 can load its 9 configuration fields.

**For Volume 9:**
- C-08: OperationalDiagnostician + InvariantEvaluator move to Vol 9 when governance infrastructure is ready.
- D-INT-02: Two-layer contradiction detection is applicable to Vol 9 for claim verification.
- B.4 cross-cutting note #2: Intelligence amplification results flow through Vol 9's output governance gate before reaching the user.

---

## Phase 2 B.4 Verdict Amendment

No B.4 verdict changes from Phase 1. All REBUILD/DEFER decisions remain as specified. Phase 2 source reading confirmed:
- 5 REBUILD (IntelligenceCoordinator, AnalogicalReasoner, HypothesisGenerator, SocraticChallenger, GrowthTracker) — all verified, design specified in B.5-B.13.
- 6 DEFER (CausalInferenceEngine, OperationalDiagnostician, AcquisitionCoordinator, ArXivFetcher, LocalWatcher, ContentQueue) — all confirmed appropriate for later tiers.
- 0 KILL — no components identified for removal.

---

## Modification History

| Version | Date | Modified By | Summary |
|---|---|---|---|
| v1 | 2026-03-11 | Oz Phase 2 Distillation Agent | Initial creation — 7 ownership claims, 5 dependency declarations, 2 conflict acknowledgements (C-03, C-08), 9 cross-volume notifications, 0 B.4 amendments |
