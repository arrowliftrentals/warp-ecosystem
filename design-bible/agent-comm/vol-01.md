# Agent Communication — Volume 1: Memory System

> **Rules:** Append new claims/dependencies/conflicts using the formats defined in `AGENT_COMM.md`.
> This file is the ONLY place Vol 1 agents register changes. Do NOT edit `AGENT_COMM.md` directly.

---

## Ownership Claims

```
CLAIM: 10-layer memory architecture (L1-L10), MemoryManager facade, per-layer implementations
OWNER: Volume 1
REASON: Pre-registered boundary — all Pydantic schemas for data entering/leaving memory layers are defined by Volume 1.
CONTESTED: no
```

### Schema Migration Declarations (Vol 1 → other volumes)

These schemas currently live in `src/memory/schemas.py` but belong to other volumes in the rebuild:

```
MIGRATION: Governance schemas (GovernedOutput, ExtractedClaim, EvidenceItem, EvidenceContract, ApprovedUtterance, AuthorityLevel, OutputPhase, ClaimType, ClaimStatus)
FROM: Volume 1 (src/memory/schemas.py)
TO: Volume 9 (governance/schemas.py)
REASON: Output/voice governance schemas owned by Volume 9 per pre-registered boundary.
```

```
MIGRATION: APEX schemas (PromptStrategy, PromptMetrics, TaskOutcome, TurnAnalysis, PromptStrategyStatus)
FROM: Volume 1 (src/memory/schemas.py)
TO: Volume 3/5 boundary
REASON: Prompt optimization schemas belong to the learning/intelligence boundary, not memory.
```

```
MIGRATION: BERT classification schema (BertClassificationResult)
FROM: Volume 1 (src/memory/schemas.py)
TO: Volume 2 (orchestrator pipeline)
REASON: Intent classification belongs to the orchestrator pipeline, not memory.
```

```
MIGRATION: Librarian schemas (LibrarianResponse, APIDefinition, SchemaDefinition, CodeReference, IndexResult, CoverageStats, DriftReport, ImpactReport)
FROM: Volume 1 (src/memory/schemas.py)
TO: Volume 5 (intelligence subsystem)
REASON: Knowledge librarian is an intelligence subsystem; schemas belong with it.
```

```
MIGRATION: Meta-assessment schemas (JarvisBenchmark, Scorecard, BenchmarkEntry, RepoStats, MarketData, ComparativeAnalysis, etc.)
FROM: Volume 1 (src/memory/schemas.py)
TO: KILL — not part of rebuild MVA
REASON: Meta-assessment/benchmarking schemas have no consumer in the rebuild pipeline.
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 1 (Memory) needs shared infrastructure (shared/errors.py, shared/config.py, shared/logging.py) from cross-cutting infra
STATUS: pending
INTERFACE: Error hierarchy from shared/errors.py; config object from shared/config.py; structured logging from shared/logging.py
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
RESOLUTION: resolved — learning-pipeline schemas → Vol 3. Shared schemas (Fact, OutcomeSignal) stay Vol 1 (conflict-report.md C-02)
```

```
CONFLICT: memory_guard.py — governance or memory concern
VOLUMES: 3 vs 1 vs 9
RESOLUTION: resolved — Vol 1 owns memory_guard (conflict-report.md C-06, overridden from gate recommendation)
```

```
CONFLICT: Verification schemas ownership
VOLUMES: 1 vs 4
RESOLUTION: resolved — Vol 1 owns schemas (data at rest). Vol 4 owns behavioral interface (conflict-report.md C-07)
```

```
CONFLICT: Governance schema location
VOLUMES: 1 vs 9
RESOLUTION: resolved — Vol 9 owns governance schemas in rebuild. Vol 1 retains memory-layer schemas (conflict-report.md C-01)
```

```
CONFLICT: Intelligence schemas ownership (StructuralAnalogy, Hypothesis, etc.)
VOLUMES: 1 vs 5
RESOLUTION: resolved — Vol 1 owns base schemas (cross memory boundary). Vol 5 consumes/extends (conflict-report.md C-03)
```
