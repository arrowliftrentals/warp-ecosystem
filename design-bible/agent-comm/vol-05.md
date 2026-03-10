# Agent Communication — Volume 5: Intelligence & Amplification

> **Rules:** Append new claims/dependencies/conflicts using the formats defined in `AGENT_COMM.md`.
> This file is the ONLY place Vol 5 agents register changes. Do NOT edit `AGENT_COMM.md` directly.

---

## Ownership Claims

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
CLAIM: AcquisitionCoordinator + ArXivFetcher + LocalWatcher + ContentQueue
OWNER: Volume 5
REASON: Content acquisition layer (src/acquisition/) feeding the intelligence pipeline. All deferred.
CONTESTED: no
```

```
CLAIM: Librarian schemas (LibrarianResponse, APIDefinition, SchemaDefinition, CodeReference, IndexResult, CoverageStats, DriftReport, ImpactReport)
OWNER: Volume 5 (currently in src/memory/schemas.py, must move in rebuild)
REASON: Knowledge librarian is an intelligence subsystem; schemas belong with it.
CONTESTED: no
```

---

## Dependency Declarations

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
DEPENDENCY: Volume 5 needs Pydantic schemas (StructuralAnalogy, Hypothesis, ResearchGap, SocraticChallenge, IntellectualProfile, CalibratedConfidence, ProvenanceChain, ProvenanceStep, SourceQuality) from Volume 1 (Memory schemas)
STATUS: pending
INTERFACE: All schemas as specified in Volume 5 B.3 schema listing
```

---

## Conflict Acknowledgements

```
CONFLICT: OperationalDiagnostician ownership
VOLUMES: 5 vs 8 vs 9
RESOLUTION: resolved — OperationalDiagnostician → Vol 9 (governance). Vol 5 retains user-facing amplification only (conflict-report.md C-08)
```

```
CONFLICT: Intelligence schemas ownership (StructuralAnalogy, Hypothesis, etc.)
VOLUMES: 1 vs 5
RESOLUTION: resolved — Vol 1 owns base schemas (cross memory boundary). Vol 5 consumes/extends (conflict-report.md C-03)
```

```
CONFLICT: RemediationEngine overlap
VOLUMES: 4 vs 5 vs 9
RESOLUTION: resolved — RemediationEngine → Vol 4 (conflict-report.md C-08)
```
