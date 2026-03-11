# ATLAS Design Bible — Volume 5: Intelligence Pipeline

| Field | Value |
|---|---|
| **Doc ID** | `DB-V05-001` |
| **Name** | Volume 5: Intelligence Pipeline |
| **Purpose** | Design specification for intellectual amplification — analogical reasoning, hypothesis generation, Socratic challenge, and growth tracking |
| **Owner** | Design Bible / Volume 5 |
| **Status** | `phase-2-complete` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / Oz Phase 1 Distillation Agent (Part B, B.1-B.4) / Oz Phase 2 Distillation Agent (Part B, B.5-B.13) |
| **Version** | v6 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-11 |

---

## Part A: Context (Pre-loaded)

### A.1 Subsystem Identity
- **Volume 5: Intelligence Pipeline**
- **Purpose:** Intellectual amplification — cross-domain analogical reasoning, hypothesis generation, Socratic challenge, and growth tracking. Makes Atlas not just a retriever but a thinking partner.
- **Rebuild phase:** Phase 4 (after memory + learning + self-modification). Intelligence builds on knowledge stored by the learning system.

### A.2 Source Manifest

**Code files to read** (paths relative to `atlas/`):

*Intelligence core:*
- `src/intelligence/coordinator.py` — unified interface for all amplification
- `src/intelligence/analogical_reasoner.py` — cross-domain structural mapping
- `src/intelligence/hypothesis_generator.py` — gap identification + hypothesis creation
- `src/intelligence/socratic_challenger.py` — constructive reasoning challenges
- `src/intelligence/growth_tracker.py` — user intellectual development tracking
- `src/intelligence/causal_inference.py` — causal reasoning
- `src/intelligence/operational_diagnostics.py` — system self-diagnostics

*Acquisition:*
- `src/acquisition/coordinator.py` — orchestrates content sources
- `src/acquisition/arxiv_fetcher.py` — arXiv paper fetching
- `src/acquisition/local_watcher.py` — filesystem monitoring for new content
- `src/acquisition/content_queue.py` — priority processing queue

**Documentation to read:**
- `docs/architecture/intelligence-system.md` — comprehensive architecture doc
- `docs/architecture/atlas-intelligence-architecture.md`
- `docs/architecture/intelligence-integration-audit-2026-02-19.md`
- `docs/plans/intelligence-system-part-a.md` through `part-e.md`
- `docs/guides/intelligence-pipeline-manual.md`

**Test files to read:**
- `tests/intelligence/` (if exists)
- `tests/acquisition/` (if exists)

**CORE/PERIPHERAL Classification:** All 11 files are **CORE** (≤40 code files). Read all in full during both Phase 1 and Phase 2.

### A.3 Context Brief

**What worked in Attempt 3:**
- IntelligenceCoordinator orchestrates
- AnalogicalReasoner has pre-validated canonical analogies (thermal↔electrical, etc.) and novel discovery via embeddings
- HypothesisGenerator identifies 4 gap types (contradictory, incomplete, outdated, unexplored)
- SocraticChallenger detects 4 challenge types with severity levels
- GrowthTracker maintains per-user intellectual profiles with domain mastery levels
- Content acquisition from arXiv + local directory monitoring
- ContentQueue with priority ordering and persistence

**What failed or was never wired:**
- Integration with orchestrator unclear — `intelligence_integration.py` exists in orchestrator but status unknown
- Intent routing for intelligence queries (e.g., "how is X like Y") designed but unclear if connected
- Feature flags for acquisition likely set to FALSE
- Overlap with knowledge pipeline in `src/learning/` — boundaries unclear

**What was simulated/fake:**
- No specific evidence of simulated intelligence capabilities

**Relevant Volume 0 principles:**
- P1: ML advises, symbolic core decides (intelligence uses embeddings but validates symbolically)
- P3: Nothing ships without integration
- P6: Memory is the foundation (intelligence queries memory)
- Section 3.3: Learning system + memory is a strong differentiator

### A.4 Known Failures & Warnings
1. **Boundary with Volume 3 (Learning)**: Knowledge pipeline components (content_ingester, domain_classifier, knowledge_synthesizer) live in `src/learning/` but are consumed by the intelligence system. The distillation agent must coordinate with Volume 3 on ownership boundaries.
2. **Acquisition may be premature**: arXiv fetching and local watching are useful but may be DEFER candidates if the core conversation loop doesn't work yet.
3. **User is a mechanical engineer PhD**: The analogical reasoner's cross-domain capabilities (e.g., thermal↔electrical, mechanical↔electrical analogies) are directly relevant to the user's domain. These have high personal value.

---

## Part B: Design Specification (Agent Fills Out)

### B.1 Subsystem Purpose (Rebuild)

The Intelligence Pipeline should transform Atlas from a passive retrieval system into an active thinking partner. It consumes `RefinedKnowledge` produced by the Learning subsystem (Volume 3) and applies four amplification capabilities: (1) cross-domain analogical reasoning that identifies structural isomorphisms between fields (e.g., thermal↔electrical, mechanical↔electrical) to enable knowledge transfer; (2) hypothesis generation that analyzes the knowledge base for contradictions, incompleteness, staleness, and unexplored parameter spaces, then produces testable hypotheses with falsification criteria and provenance chains; (3) Socratic challenging that constructively identifies flaws in user reasoning—contradictions with known facts, unstated assumptions, missing evidence, and scope overgeneralization—and tracks resolution patterns for adaptive challenge calibration; and (4) intellectual growth tracking that maintains per-user domain mastery profiles, identifies recurring blind spots, and generates personalized learning recommendations. A separate acquisition layer feeds the pipeline by fetching content from arXiv and monitoring local directories, queueing it for ingestion by Volume 3's ContentIngester. Every output carries provenance and calibrated confidence scores. The subsystem depends on the memory system (L4 declarative, L9 social, L10 vector) and produces outputs consumed by the orchestrator (Volume 2) to enrich user-facing responses.

### B.2 Architecture Overview

The intelligence subsystem has two layers: **Acquisition** (content sourcing) and **Amplification** (intellectual reasoning). They are connected through the Learning subsystem (Volume 3), not directly coupled.

```
                     ACQUISITION LAYER
  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐
  │ ArXivFetcher │  │LocalWatcher │  │ Manual API   │
  └──────┬───────┘  └──────┬──────┘  └──────┬───────┘
         └─────────────────┼─────────────────┘
                           ▼
                  ┌────────────────┐
                  │  ContentQueue  │   (priority heap, persistent)
                  └───────┬────────┘
                          ▼
              ┌───────────────────────┐
              │ AcquisitionCoordinator│ ──► Vol 3 ContentIngester
              └───────────────────────┘     (ingestion + extraction)
                                                    │
                                                    ▼
                                           RefinedKnowledge
                                                    │
           ─────────────────────────────────────────┤
                                                    │
                     AMPLIFICATION LAYER            ▼
              ┌─────────────────────────────────────────┐
              │        IntelligenceCoordinator           │
              │  (unified facade, query amplification)   │
              ├────────┬───────────┬────────┬────────────┤
              │Analog. │Hypothesis │Socratic│  Growth    │
              │Reasoner│Generator  │Challgr │  Tracker   │
              └───┬────┴─────┬────┴───┬────┴─────┬──────┘
                  │          │        │          │
                  ▼          ▼        ▼          ▼
               L4/L10      L4/L10     L4       L9/L3
              (memory)    (memory)  (memory)  (memory)
```

**Component responsibilities:**

- **IntelligenceCoordinator**: Facade that exposes high-level methods (`amplify_query`, `cross_domain_insight`, `challenge_and_refine`, `generate_research_agenda`, `get_intellectual_summary`). Composes the four amplification components. Serves as the single entry point for Volume 2 (Orchestrator) to invoke intelligence capabilities.
- **AnalogicalReasoner**: Maintains a registry of canonical structural analogies (thermal↔electrical, mechanical↔electrical, evolution↔optimization, quantum↔computing). Supports novel analogy discovery via L10 semantic search. Provides `find_analogies()` and `transfer_knowledge()` with provenance chains.
- **HypothesisGenerator**: Scans L4 declarative memory to identify four gap types: contradictory facts, incomplete concept clusters, outdated knowledge, and unexplored combinations. Generates `Hypothesis` objects with mandatory falsification criteria and calibrated confidence.
- **SocraticChallenger**: Analyzes user claims against L4 facts for contradiction, assumption, missing evidence, and scope issues. Maintains active challenge state. Records resolutions to L3 episodic for pattern learning. Adapts challenge frequency based on user's dismiss-vs-address ratio.
- **GrowthTracker**: Maintains `IntellectualProfile` per user in L9 social memory. Tracks domain mastery progression, concept graduation (introduced→developing→mastered), blind spots, and growth trajectory. Generates personalized recommendations based on gaps.
- **CausalInferenceEngine**: Lightweight temporal correlation analyzer. Consumes event timestamps from PatternLearner and AwarenessCache. Identifies event pairs where A consistently precedes B within a time window. Not part of the core amplification loop.
- **OperationalDiagnostician + RemediationEngine + InvariantEvaluator**: System self-diagnostics. Rules-based root-cause analysis for operational anomalies (sync I/O in async, event loop blocking, health truthfulness, data flow orphans). Produces `OperationalDiagnosis` with ranked hypotheses and optional `RemediationPatch`. These are internal infrastructure, not user-facing intelligence.
- **AcquisitionCoordinator**: Orchestrates ArXivFetcher and LocalWatcher. Feeds ContentQueue. Forwards ingested content to KnowledgeEngine (Volume 3). Manages start/stop lifecycle for background tasks.
- **ArXivFetcher**: Scheduled arXiv API queries with category subscriptions. Rate-limited per arXiv ToS (3s between calls). Downloads PDFs. Produces `ArXivPaper` metadata validated via Pydantic.
- **LocalWatcher**: Monitors configured directories via watchdog (real-time) or polling fallback. Deduplicates by SHA256 hash. Respects `.atlasignore` files.
- **ContentQueue**: Priority heap with Pydantic-validated `QueueItem`. Persistent to JSON. Deduplicates by `source_type:source_id`. Supports retry with priority demotion.

### B.3 Interface Contracts

#### IntelligenceCoordinator

**Dependencies consumed:**
- `MemoryManager` from Volume 1 (L4, L9, L10 access)
- `RefinedKnowledge` schema from Volume 3 (Learning) — consumed indirectly via memory queries

**Dependencies served:**
- Volume 2 (Orchestrator) calls `amplify_query()`, `cross_domain_insight()`, `challenge_and_refine()` during response generation

**Public methods:**

```
async amplify_query(
    query: str,
    user_id: str,
    domain: str | None = None,
) -> AmplificationResult
```
Input: user query string, user ID, optional domain hint.
Output schema `AmplificationResult`:
- `analogies: list[StructuralAnalogy]` (max 3)
- `challenges: list[SocraticChallenge]` (max 2)
- `related_gaps: list[ResearchGap]` (max 3)
- `recommendations: dict[str, list[str]]`

```
async cross_domain_insight(
    concept: str,
    source_domain: str,
    target_domain: str,
    user_id: str,
) -> CrossDomainResult
```
Output schema `CrossDomainResult`:
- `success: bool`
- `original: str`
- `transferred: str`
- `analogy: StructuralAnalogy`
- `confidence: CalibratedConfidence`
- `provenance: ProvenanceChain`
- `caveats: list[str]`

```
async challenge_and_refine(
    claim: str,
    user_id: str,
    context: str | None = None,
) -> ChallengeResult
```
Output schema `ChallengeResult`:
- `claim: str`
- `challenges: list[SocraticChallenge]`
- `challenge_count: int`
- `user_challenge_history: dict[str, int]`

```
async generate_research_agenda(
    user_id: str,
    domain: str,
    focus_area: str | None = None,
) -> ResearchAgenda
```
Output schema `ResearchAgenda`:
- `domain: str`
- `user_mastery: float`
- `gaps: list[ResearchGap]`
- `hypotheses: list[Hypothesis]`
- `suggested_next_steps: list[str]`

```
async get_intellectual_summary(
    user_id: str,
    days: int = 30,
) -> IntellectualSummary
```
Output schema `IntellectualSummary`:
- `profile: IntellectualProfile`
- `growth_summary: dict`
- `recommendations: dict[str, list[str]]`
- `active_challenges: int`

#### AnalogicalReasoner

**Dependencies consumed:** `MemoryManager` (L4 `query_facts`, L10 `search_similar`)

**Public methods:**

```
async find_analogies(
    concept: str,
    source_domain: str,
    target_domains: list[str] | None = None,
) -> list[StructuralAnalogy]
```

```
async transfer_knowledge(
    analogy: StructuralAnalogy,
    knowledge_item: str,
) -> tuple[str, CalibratedConfidence, ProvenanceChain]
```

```
get_canonical_analogies(source_domain: str) -> list[StructuralAnalogy]
```

#### HypothesisGenerator

**Dependencies consumed:** `MemoryManager` (L4 `query_facts`)

**Public methods:**

```
async identify_gaps(
    domain: str | None = None,
    limit: int = 10,
) -> list[ResearchGap]
```

```
async generate_hypotheses(
    gaps: list[ResearchGap] | None = None,
    domain: str | None = None,
    limit: int = 5,
) -> list[Hypothesis]
```

#### SocraticChallenger

**Dependencies consumed:** `MemoryManager` (L4 `query_facts`, L3 `store_episode`)

**Public methods:**

```
async analyze_claim(
    claim: str,
    context: str | None = None,
) -> list[SocraticChallenge]
```

```
async resolve_challenge(
    challenge_id: str,
    response: str,
    resolution: str,  # "addressed" | "dismissed" | "deferred"
) -> None
```

```
get_active_challenges() -> list[SocraticChallenge]
```

#### GrowthTracker

**Dependencies consumed:** `MemoryManager` (L9 `get_profile`, `update_profile`)

**Public methods:**

```
async get_profile(user_id: str) -> IntellectualProfile
```

```
async record_interaction(
    user_id: str,
    concepts_used: list[str],
    domain: str,
    interaction_type: str,  # "query" | "hypothesis" | "challenge_response"
    success: bool,
) -> IntellectualProfile
```

```
async get_recommendations(
    user_id: str,
    limit: int = 5,
) -> dict[str, list[str]]
```

```
async get_growth_summary(
    user_id: str,
    days: int = 30,
) -> dict
```

#### AcquisitionCoordinator

**Dependencies consumed:**
- `ContentIngester` from Volume 3 (Learning)
- `KnowledgeEngine` from Volume 3 (Learning) — for forwarding

**Public methods:**

```
async start() -> None
async stop() -> None
async manual_ingest(file_path: str, priority: int = 1, metadata: dict | None = None) -> str
get_stats() -> dict
```

#### Pydantic Schemas Required (defined by Volume 1 Memory or Volume 5 Intelligence)

The following schemas are referenced across the intelligence pipeline. Schemas that cross subsystem boundaries are defined by Volume 1 (Memory) per AGENT_COMM.md pre-registered ownership. Volume 5 may request new fields via dependency declarations.

- `StructuralAnalogy`: source/target domain, concept, mappings `list[dict[str,str]]`, similarity_type, similarity_score (0-1), valid_for, breaks_when
- `Hypothesis`: statement, domain, derived_from, knowledge_gap_addressed, is_testable, test_methodology, predictions, falsification_criteria, prior_probability, confidence (`CalibratedConfidence`), provenance (`ProvenanceChain`)
- `ResearchGap`: description, domain, gap_type (`contradictory`|`incomplete`|`outdated`|`unexplored`), evidence, missing_knowledge, unanswered_questions, importance_score, importance_rationale
- `SocraticChallenge`: user_claim, challenge_type (`contradiction`|`assumption`|`missing_evidence`|`scope`), challenge_statement, severity, resolution_options, contradicting_sources, user_response, resolution_status
- `IntellectualProfile`: user_id, domain_mastery `dict[str,float]`, concepts_introduced/developing/mastered `list[str]`, recurring_blind_spots, questions_asked, hypotheses_generated, challenges_addressed/dismissed, growth_trajectory, recommended_topics, recommended_readings, last_updated
- `CalibratedConfidence`: overall (0-1), epistemic, model_uncertainty, source_weights, calibration_method
- `ProvenanceChain`: conclusion, conclusion_confidence, steps `list[ProvenanceStep]`, assumptions
- `ProvenanceStep`: step_number, source_type, source_id, source_content, source_quality (`SourceQuality` enum), derivation_type, derived_claim, step_confidence, reasoning
- `ArXivQuery`: search_query, categories, max_results, date_from/to, schedule, priority (Pydantic, defined in acquisition)
- `ArXivPaper`: arxiv_id, title, authors, abstract, categories, published, pdf_url, is_downloaded, local_path (Pydantic, defined in acquisition)
- `QueueItem`: source_type, source_id, content_path, metadata, priority, queued_at, attempts, status (Pydantic, defined in acquisition)
- `WatchedDirectory`: path, recursive, file_patterns, ignore_patterns, priority, domain_hint (Pydantic, defined in acquisition)

#### OperationalDiagnostician

**Dependencies consumed:**
- `DiagnosticRule`, `OperationalDiagnosis`, `RankedHypothesis`, `RemediationPatch` schemas from Volume 1 Memory
- `DiagnosticReportV2`, `HealthTruthfulnessFinding`, `DataFlowFinding` from `schemas_diagnostics`
- `SelfModel` from introspection (Volume 4 Self-Modification or Volume 8 Infrastructure)
- Telemetry port from `src.shared.ports.telemetry`

**Public methods:**

```
diagnose(anomaly_context: dict[str, Any]) -> OperationalDiagnosis
add_rule(rule: DiagnosticRule) -> None
diagnose_health_truthfulness(health_reports: list[tuple[str, bool]], ...) -> list[HealthTruthfulnessFinding]
diagnose_data_flows(emit_map: dict | None, subscribe_map: dict | None) -> list[DataFlowFinding]
```

#### CausalInferenceEngine

**Dependencies consumed:**
- `PatternLearner` from Volume 3 (Learning) — `command_history`, `interaction_history`
- `AwarenessCache` (optional, from orchestrator or infrastructure)

**Public methods:**

```
async analyze_correlations(window_hours: int = 24) -> list[CausalChain]
get_causal_predictions(trigger_event: str) -> list[dict[str, Any]]
get_known_chains() -> list[CausalChain]
```

### B.4 Scope Triage

**Intelligence Core:**

| Component | File | Verdict | Justification |
|---|---|---|---|
| IntelligenceCoordinator | `src/intelligence/coordinator.py` | **REBUILD** | Core facade for amplification. Design intent is sound: composing four reasoning components behind a unified async API. Rebuild with proper Pydantic output schemas (current returns raw dicts), eliminate singleton pattern in favor of DI, and wire into orchestrator. High value—directly serves the "thinking partner" vision. |
| AnalogicalReasoner | `src/intelligence/analogical_reasoner.py` | **REBUILD** | Canonical analogies (thermal↔electrical, mechanical↔electrical) are directly valuable to the user's mechanical engineering PhD background. Novel analogy discovery via L10 embeddings is architecturally sound. Rebuild with cleaner separation between canonical lookup and semantic discovery, and replace string-replacement knowledge transfer with structured mapping. |
| HypothesisGenerator | `src/intelligence/hypothesis_generator.py` | **REBUILD** | Four gap-identification strategies (contradictions, incomplete, outdated, unexplored) are well-conceived. Hypothesis templates with mandatory falsification criteria enforce scientific rigor. Rebuild with stronger semantic similarity (current fallback is Jaccard word-overlap) and eliminate `Any` type annotations. |
| SocraticChallenger | `src/intelligence/socratic_challenger.py` | **REBUILD** | Four challenge types (contradiction, assumption, missing evidence, scope) with severity levels and resolution tracking are well-designed. Adaptive behavior (filtering based on dismiss ratio) is valuable. Rebuild with improved contradiction detection (current keyword matching is brittle) and proper L3 episode storage. |
| GrowthTracker | `src/intelligence/growth_tracker.py` | **REBUILD** | Per-user intellectual profiles with domain mastery, concept progression, blind spots, and growth trajectory are unique and valuable. Rebuild with cleaner L9 integration (current nests profile in metadata dict—should be first-class schema) and bounded growth_trajectory (current truncation is ad-hoc). |
| CausalInferenceEngine | `src/intelligence/causal_inference.py` | **DEFER** | Temporal correlation analysis is useful for anticipatory intelligence but depends on PatternLearner and AwarenessCache that are in early build tiers. Uses dataclasses instead of Pydantic (violates P8). Defer until Learning (Volume 3) and core infrastructure are stable. Rebuild in later tier. |
| OperationalDiagnostician | `src/intelligence/operational_diagnostics.py` | **DEFER** | System self-diagnostics (health truthfulness, data flow analysis) is infrastructure, not user-facing intelligence. Depends on SelfModel, telemetry, and diagnostic schemas not yet established. The InvariantEvaluator (safe mini-DSL) is well-designed but premature. The RemediationEngine is useful but depends on the self-modification pipeline (Volume 4). Defer until Tier 6+ when self-modification and full observability are in place. |

**Acquisition:**

| Component | File | Verdict | Justification |
|---|---|---|---|
| AcquisitionCoordinator | `src/acquisition/coordinator.py` | **DEFER** | Well-structured orchestrator that wires ArXivFetcher + LocalWatcher → ContentQueue → ContentIngester → KnowledgeEngine. Design is sound but depends on Volume 3's ContentIngester and KnowledgeEngine. Per Volume 0 build order, intelligence is Tier 6+ (depends on Tier 3 Memory + Tier 5 Learning). Defer until learning pipeline is wired. |
| ArXivFetcher | `src/acquisition/arxiv_fetcher.py` | **DEFER** | Clean implementation with Pydantic schemas (ArXivQuery, ArXivPaper), rate limiting per arXiv ToS, and scheduled queries. However, A.4 warning #2 applies: acquisition is premature if the conversation loop doesn't work. External dependency on `arxiv` library. Defer until MVA-1 through MVA-4 pass. |
| LocalWatcher | `src/acquisition/local_watcher.py` | **DEFER** | Filesystem monitoring with watchdog + polling fallback, SHA256 dedup, .atlasignore support. Useful but not needed until the knowledge pipeline is functional end-to-end. External dependency on `watchdog`. Defer alongside AcquisitionCoordinator. |
|| ContentQueue | `src/acquisition/content_queue.py` | **DEFER** | Priority heap with Pydantic validation, persistence, dedup, retry. Well-designed utility. However, it only serves the acquisition layer which is itself deferred. Defer alongside acquisition. |

**Cross-cutting rebuild notes (from oversight self-review):**

1. **P5 violation — silent error swallowing**: All REBUILD components use `except Exception as e: logger.debug(...)` throughout (coordinator lines 108-145, reasoner lines 344-345, generator lines 166-167, challenger lines 136-137). This silently degrades to empty results rather than classifying and routing errors per Volume 0 P5. The rebuild must replace these with specific exception types from the shared error hierarchy and log at `warning` or `error` level.
2. **P9 — output governance integration**: Intelligence amplification results flow into the orchestrator's response pipeline. The rebuild must ensure that factual claims in amplification outputs (e.g., analogy explanations, hypothesis statements) pass through Volume 9's output governance gate before reaching the user. Intelligence does not self-govern — it produces candidate enrichments that the orchestrator governs.
3. **Singleton anti-pattern**: Every component (all 11 files) uses a module-global singleton with `get_*()` factory and `reset_*()` for testing. The rebuild must use constructor-based dependency injection with MemoryManager passed at initialization, not lazily acquired via global state. This eliminates hidden coupling and makes testing explicit.
4. **R6 strength — model independence**: The amplification layer is entirely symbolic + memory-based with zero direct LLM dependency. Canonical analogies, gap identification, and growth tracking work without any LLM API call. This is architecturally correct per Volume 0 R6 and must be preserved in the rebuild. LLM may enhance novel analogy discovery but must not be required.
5. **`Any` type annotations**: coordinator.py lines 93 and hypothesis_generator.py lines 145, 230, 343 use `Any` type: ignore annotations. The rebuild must use proper typed dicts or Pydantic models.

### B.5 Technology Choices

#### Language & Runtime
- **Python 3.11+** — required by PROJECT_CONVENTIONS.md. Modern union type syntax (`X | None`), `asyncio` for all coordinator and amplification methods.

#### Libraries (REBUILD components only)
- **Pydantic v2** — all intelligence schemas (StructuralAnalogy, Hypothesis, ResearchGap, SocraticChallenge, IntellectualProfile, CalibratedConfidence, ProvenanceChain, ProvenanceStep). Per P8, every datum crossing a subsystem boundary or entering memory must be Pydantic-validated.
- **structlog** — replaces Attempt 3’s `loguru`. Per PROJECT_CONVENTIONS.md Section 7, all logging uses `structlog.get_logger()` with structured JSON output.
- **No direct LLM dependency** — the amplification layer is entirely symbolic + memory-based. Canonical analogies, gap identification, Socratic challenges, and growth tracking operate without any LLM API call (R6 model independence). LLM enhancement is optional and gated behind the LLMProvider Protocol from `shared/llm.py` if used for novel analogy narratives in future tiers.
- **No ML model dependency** — unlike Volume 2 (BERT classifiers) or Volume 3 (domain classifiers), the intelligence pipeline uses L10 FAISS vector search for semantic similarity (provided by Volume 1), not its own embedding model. This keeps the subsystem lightweight.

#### Libraries (DEFER components — noted for future reference)
- **arxiv** (PyPI) — ArXivFetcher dependency. Optional; `_check_arxiv_available()` gates usage. Defer until Tier 6+.
- **watchdog** — LocalWatcher dependency for real-time filesystem monitoring. Optional; polling fallback exists. Defer until Tier 6+.

#### Departures from Attempt 3
- `loguru` → `structlog`: Mandated by PROJECT_CONVENTIONS.md.
- `dataclass` → Pydantic: CausalInferenceEngine’s `CausalChain` used `@dataclass`. Rebuild uses Pydantic for P8 compliance (DEFER scope, but noted).
- Singleton pattern → constructor-based DI: All 11 files in Attempt 3 use module-global singletons with `get_*()` / `reset_*()`. Rebuild passes `MemoryManager` as a constructor argument. No global state. Testing becomes explicit.

### B.6 Data Model

#### Schema Ownership (per C-03 resolution)
Per conflict resolution C-03, Volume 1 (Memory) defines the Pydantic data schemas because they cross the memory boundary (stored in L4/L9). Volume 5 consumes them. If Volume 5 needs intelligence-specific fields not relevant to storage, Volume 5 defines extension schemas that compose Volume 1 base schemas.

#### Schemas Consumed from Volume 1 (`atlas/memory/schemas.py`)

**StructuralAnalogy** — `analogy_id: str` (UUID, auto-generated), `source_domain: str`, `target_domain: str`, `source_concept: str`, `target_concept: str`, `mappings: list[dict[str, str]]` (term-to-term structural mappings), `similarity_type: str` (one of `mathematical`, `functional`, `structural`, `semantic`), `similarity_score: float` (ge=0.0, le=1.0), `similarity_explanation: str`, `valid_for: list[str]`, `breaks_when: list[str]`. Frozen: no (target_concept may be refined).

**Hypothesis** — `hypothesis_id: str` (UUID), `statement: str`, `domain: str`, `derived_from: list[str]`, `knowledge_gap_addressed: str`, `is_testable: bool`, `test_methodology: str`, `predictions: list[str]`, `falsification_criteria: list[str]` (min_length=1 — mandatory), `prior_probability: float` (ge=0.0, le=1.0), `confidence: CalibratedConfidence | None`, `provenance: ProvenanceChain | None`, `required_resources: list[str]`, `estimated_effort: str | None`. Frozen: yes.

**ResearchGap** — `gap_id: str` (UUID), `description: str`, `domain: str`, `gap_type: str` (one of `contradictory`, `incomplete`, `outdated`, `unexplored`), `evidence: list[str]`, `missing_knowledge: list[str]`, `unanswered_questions: list[str]`, `importance_score: float` (ge=0.0, le=1.0), `importance_rationale: str`. Frozen: yes.

**SocraticChallenge** — `challenge_id: str` (UUID), `user_claim: str`, `challenge_type: str` (one of `contradiction`, `assumption`, `missing_evidence`, `scope`), `challenge_statement: str`, `severity: str` (one of `critical`, `significant`, `minor`, `clarification`), `resolution_options: list[str]`, `contradicting_sources: list[str]`, `user_response: str | None`, `resolution_status: str` (one of `open`, `addressed`, `dismissed`, `deferred`, default `open`). Frozen: no (resolution status updates).

**IntellectualProfile** — `user_id: str`, `domain_mastery: dict[str, float]` (values ge=0.0, le=1.0), `concepts_introduced: list[str]`, `concepts_developing: list[str]`, `concepts_mastered: list[str]`, `recurring_blind_spots: list[str]`, `questions_asked: int` (default 0), `hypotheses_generated: int` (default 0), `challenges_addressed: int` (default 0), `challenges_dismissed: int` (default 0), `growth_trajectory: list[dict]` (bounded: max 1000, truncate to 500), `recommended_topics: list[str]`, `recommended_readings: list[str]`, `last_updated: datetime`. Frozen: no.

**CalibratedConfidence** — `overall: float` (ge=0.0, le=1.0), `epistemic: float` (default 0.0), `model_uncertainty: float` (default 0.0), `source_weights: dict[str, float]`, `calibration_method: str` (default `weighted_source`). Frozen: yes.

**ProvenanceChain** — `chain_id: str` (UUID), `conclusion: str`, `conclusion_confidence: CalibratedConfidence`, `steps: list[ProvenanceStep]` (min_length=1), `assumptions: list[str]`, `is_validated: bool` (default False). Frozen: yes.

**ProvenanceStep** — `step_id: str` (UUID), `step_number: int` (ge=1), `source_type: str`, `source_id: str`, `source_content: str`, `source_quality: SourceQuality` (enum: PEER_REVIEWED, PREPRINT, TEXTBOOK, USER_STATED, INFERRED, WEB, UNKNOWN), `derivation_type: str`, `derived_claim: str`, `step_confidence: float` (ge=0.0, le=1.0), `reasoning: str`. Frozen: yes.

#### Schemas Owned by Volume 5 (Amplification Response Types)
These are intelligence-specific result containers that compose Vol 1 base schemas. They live in `atlas/intelligence/schemas.py`.

**AmplificationResult** — `analogies: list[StructuralAnalogy]` (max 3), `challenges: list[SocraticChallenge]` (max 2), `related_gaps: list[ResearchGap]` (max 3), `recommendations: dict[str, list[str]]`. Frozen: yes.

**CrossDomainResult** — `success: bool`, `original: str`, `transferred: str`, `analogy: StructuralAnalogy | None`, `confidence: CalibratedConfidence | None`, `provenance: ProvenanceChain | None`, `caveats: list[str]`, `message: str | None` (error message when success=False). Frozen: yes.

**ChallengeResult** — `claim: str`, `challenges: list[SocraticChallenge]`, `challenge_count: int`, `user_challenge_history: dict[str, int]`. Frozen: yes.

**ResearchAgenda** — `domain: str`, `user_mastery: float`, `gaps: list[ResearchGap]`, `hypotheses: list[Hypothesis]`, `suggested_next_steps: list[str]`. Frozen: yes.

**IntellectualSummary** — `profile: IntellectualProfile`, `growth_summary: dict`, `recommendations: dict[str, list[str]]`, `active_challenges: int`. Frozen: yes.

#### Canonical Analogies Data
The 4 canonical analogies (thermal↔electrical, mechanical↔electrical, evolution↔optimization, quantum↔computing) are embedded as static data in the AnalogicalReasoner module. In the rebuild, store these as a `CANONICAL_ANALOGIES: list[StructuralAnalogy]` module constant — fully-validated Pydantic instances, not raw dicts as in Attempt 3. Reverse mappings are computed at initialization.

### B.7 Error Handling

#### Error Types (from `atlas/shared/errors.py`)
The intelligence subsystem uses the shared error hierarchy. No subsystem-specific error subclass is needed because failures in intelligence are non-critical (amplification enriches responses but is not required for the conversation loop).

- **`AtlasError`** — base class.
- **`MemoryLayerError`** — raised when L4/L9/L10 queries fail. Intelligence catches this and degrades gracefully.
- **`ValidationError`** — raised when Pydantic schema validation fails.

#### Error Propagation Rules
1. **Amplification failures do not crash the conversation loop.** If `amplify_query()` fails, the orchestrator receives an empty `AmplificationResult`.
2. **Individual component failures are isolated.** If AnalogicalReasoner fails during `amplify_query()`, HypothesisGenerator and SocraticChallenger still execute.
3. **No silent swallowing.** Attempt 3 used `except Exception as e: logger.debug(...)` throughout (coordinator.py lines 108-145, reasoner.py lines 344-345, generator.py lines 166-167, challenger.py lines 136-137). In the rebuild, all exception handlers must: log at `warning` minimum with structured context, classify the error (`MemoryLayerError` vs. `ValidationError` vs. unexpected), and route to the learning system via `OutcomeSignal` with `outcome_type=ERROR`.
4. **Memory unavailability is expected.** Intelligence components must function without memory (return empty results, not raise).
5. **L10 semantic search fallback.** If L10 is unavailable, fall back to L4 fact search. If L4 is unavailable, return empty results. This two-tier fallback from Attempt 3 is preserved.

#### Recovery Patterns
- **Coordinator-level recovery:** Each component is wrapped in try/except. On failure, that component’s slot is empty; others continue.
- **Growth tracker persistence:** If L9 write fails, in-memory cache retains the profile. Next successful write persists accumulated changes.
- **Active challenges in-memory:** SocraticChallenger’s `active_challenges` are lost on restart. Acceptable for rebuild; persistent tracking is Tier 6+.

### B.8 Testing Strategy

#### Acceptance Tests (Mandatory — gate deployment)

**AT-INT-01: Amplification enriches a domain query** — Running server with L4 facts about thermodynamics. `POST /v1/atlas/chat` with `{"query": "How is heat transfer similar to electrical circuits?"}`. Verify response metadata contains non-empty `analogies` with thermal↔electrical mapping. Fails if intelligence subsystem deleted.

**AT-INT-02: Socratic challenge detects overgeneralization** — Running server. `POST /v1/atlas/chat` with `{"query": "All metals always conduct electricity perfectly"}`. Verify response includes challenge of type `scope` or `assumption`. Fails if SocraticChallenger stubbed.

**AT-INT-03: Growth tracking persists across sessions** — Session 1: send 3 thermodynamics queries. Session 2: ask "What topics should I study next?" Verify response references thermodynamics mastery. Fails if GrowthTracker doesn’t persist to L9.

#### Integration Tests (Real components, no boundary mocks)

**IT-INT-01: IntelligenceCoordinator → MemoryManager round-trip** — Test SQLite DB. Store facts in L4, profile in L9. Call `amplify_query()`, verify real fact retrieval. Call `get_intellectual_summary()`, verify real profile.

**IT-INT-02: AnalogicalReasoner canonical + novel discovery** — Populate L10 with embeddings. Verify canonical thermal↔electrical returned. Verify L10 search called for novel discovery. Verify L4 fallback when L10 empty.

**IT-INT-03: HypothesisGenerator gap identification** — Store contradictory facts in L4. Verify `contradictory` gap found. Verify each hypothesis has `falsification_criteria` (len >= 1).

**IT-INT-04: SocraticChallenger → L3 episode storage** — Analyze claim with "always". Verify challenge type. Resolve challenge. Verify Episode stored in L3 with `event_type=USER_FEEDBACK`.

**IT-INT-05: GrowthTracker mastery progression** — Record success interaction, verify mastery increased. Record failure, verify blind spot populated. Verify recommendations reference blind spots.

#### Unit Tests (Isolated, mocks allowed)

**UT-INT-01**: Canonical analogy lookup (4 analogies loaded, reverse mappings exist). **UT-INT-02**: Knowledge transfer (string mapping, provenance chain 3 steps, confidence derived). **UT-INT-03**: Gap type strategies (4 types, mandatory falsification_criteria, varying prior_probability). **UT-INT-04**: Assumption trigger detection (8 triggers, max 2 challenges). **UT-INT-05**: Contradiction detection two-layer (negation heuristic, polarity markers, semantic path). **UT-INT-06**: Growth trajectory truncation (1001→500). **UT-INT-07**: Mastery decay ((1-0.01)^30). **UT-INT-08**: Distance-to-similarity conversion (0→1.0, 1→0.5). **UT-INT-09**: Jaccard fallback (identical→1.0, disjoint→0.0).

#### Regression Tests (from A.4 Known Failures)

**RT-INT-01: Silent exception swallowing** — Inject `MemoryLayerError` into L4. Verify logged at `warning` (not `debug`). Verify empty results returned.

**RT-INT-02: `Any` type annotations eliminated** — mypy --strict reports zero `Any` in intelligence modules.

### B.9 Configuration

All intelligence configuration uses the `ATLAS_` env prefix per PROJECT_CONVENTIONS.md Section 8.

- `ATLAS_ENABLE_INTELLIGENCE` (`bool`, default `False`) — Feature flag. When False, coordinator returns empty results. When True, subsystem must pass AT-INT-01.
- `ATLAS_INTELLIGENCE_MIN_SIMILARITY` (`float`, default `0.6`, range 0.0-1.0) — Minimum similarity for analogy discovery.
- `ATLAS_INTELLIGENCE_CHALLENGE_THRESHOLD` (`float`, default `0.6`, range 0.0-1.0) — Minimum confidence to raise Socratic challenge.
- `ATLAS_INTELLIGENCE_GROWTH_DECAY_RATE` (`float`, default `0.01`, range 0.0-0.1) — Daily mastery decay rate.
- `ATLAS_INTELLIGENCE_MAX_ANALOGIES` (`int`, default `3`, range 1-10) — Max analogies per amplification.
- `ATLAS_INTELLIGENCE_MAX_CHALLENGES` (`int`, default `2`, range 1-5) — Max Socratic challenges per amplification.
- `ATLAS_INTELLIGENCE_MAX_GAPS` (`int`, default `3`, range 1-10) — Max research gaps per amplification.
- `ATLAS_INTELLIGENCE_TRAJECTORY_MAX` (`int`, default `1000`) — Max growth trajectory entries before truncation.
- `ATLAS_INTELLIGENCE_TRAJECTORY_KEEP` (`int`, default `500`) — Entries kept after truncation.

All fields defined on `AtlasConfig(BaseSettings)` with `env_prefix="ATLAS_"`. Out-of-range values raise `ConfigurationError` immediately.

### B.10 Subsystem Lessons Learned

**L-INT-01: Raw dict returns defeated Pydantic’s purpose.** All coordinator methods return `Dict` (coordinator.py lines 77, 154, 207, 264, 300). Inside, Pydantic objects are `.model_dump()`ed back to dicts. The orchestrator received untyped dicts with no compile-time guarantees. Rebuild must return typed Pydantic result schemas directly.

**L-INT-02: Singleton pattern created hidden test coupling.** All 11 files use module-global singletons with `get_*()` / `reset_*()`. Tests relied on `reset_*()` in fixtures (test_intelligence_module.py lines 63-76). Forgotten resets caused cross-test contamination. Rebuild eliminates singletons — constructor DI.

**L-INT-03: String-replacement knowledge transfer is fragile.** `transfer_knowledge()` (analogical_reasoner.py lines 468-471) uses `.replace()` for term substitution. Breaks on substring matches, case sensitivity, multi-word terms, overlapping mappings. Rebuild uses whole-word, case-insensitive, longest-match-first replacement or structured indexed mapping.

**L-INT-04: Keyword-based contradiction detection has low precision.** SocraticChallenger._is_contradicting() (socratic_challenger.py lines 141-165) checks word pairs with topic-overlap≥3. False positives on shared common words. Rebuild should use HypothesisGenerator’s two-layer detection (negation heuristic + L10 semantic + polarity markers) as the standard across both components.

**L-INT-05: GrowthTracker nests profile in L9 metadata dict.** `_save_profile()` stores IntellectualProfile in `user_profile.metadata['intellectual_profile']` (growth_tracker.py lines 99-109). Fragile: untyped dict, magic key, manual deserialization. Rebuild should make IntellectualProfile a first-class field on L9 `UserProfile` schema.

**L-INT-06: No memory → synthetic placeholders silently returned.** `_find_incomplete_clusters()` (hypothesis_generator.py lines 306-314) and `_find_unexplored_combinations()` (lines 377-384) return hardcoded synthetic examples when memory is unavailable. Indistinguishable from real results, violating P4/P9. Rebuild returns empty list or marks results `synthetic: bool`.

### B.11 Discoveries

**D-INT-01: Amplification layer is the purest R6 implementation.** Zero direct LLM dependency. Every operation is symbolic + memory-based. This is the strongest R6 (model independence) implementation across all 10 volumes. Recommend as gold standard for subsystems that can function without LLM.

**D-INT-02: Two-layer contradiction detection pattern is reusable.** HypothesisGenerator._are_contradictory() (hypothesis_generator.py lines 171-209) uses cheap heuristic → expensive semantic check. Applicable to Vol 9 (claim verification), Vol 3 (contradictory learned facts), Vol 2 (query-context contradictions). Recommend promoting to `atlas/shared/text.py`.

**D-INT-03: Growth trajectory unbounded accumulation risk.** Truncation at 1000→500 drops oldest entries without summarization, permanently losing early growth data. Rebuild should consolidate dropped periods into per-domain summary entries. Same pattern applicable to Vol 1 L3 episodic consolidation.

**D-INT-04: OperationalDiagnostician belongs to Governance, not Intelligence.** OperationalDiagnostician, InvariantEvaluator, RemediationEngine (operational_diagnostics.py, 960 lines) are infrastructure/governance tools. Per C-08: move diagnostician + evaluator to Vol 9 (Governance), remediation engine to Vol 4 (Self-Modification). Confirmed by source: imports from `src.memory.schemas_diagnostics` and `src.introspection.self_model`.

**D-INT-05: Acquisition layer is a clean handoff to Volume 3.** The 4 acquisition files form a self-contained pipeline feeding Volume 3’s ContentIngester. Boundary is clean: `QueueItem` → `ContentIngester.ingest()` → `RefinedKnowledge`. No intelligence-specific logic in acquisition. Confirms DEFER verdicts.

### B.12 Oversight Self-Review

**Q1: Does every A.4 Known Failure have a corresponding design decision in B.1-B.10?**

- **A.4 #1 (Boundary with Volume 3):** Addressed in B.2 architecture diagram (acquisition → Vol 3 → amplification), B.4 (defer acquisition), B.6 (schema ownership per C-02/C-03), B.11 D-INT-05.
- **A.4 #2 (Acquisition may be premature):** Addressed in B.4 (all 4 acquisition DEFER), B.5 (arxiv/watchdog as DEFER deps), B.9 (feature flag defaults False).
- **A.4 #3 (User is mechanical engineer PhD):** Addressed in B.4 REBUILD for AnalogicalReasoner (notes mechanical engineering relevance), B.6 (canonical analogies include thermal↔electrical, mechanical↔electrical).

**Q2: Does B.7 error handling comply with Volume 0 P5?**
Yes. B.7 mandates `warning` minimum logging, error classification, learning system routing via OutcomeSignal. Calls out Attempt 3 violation. RT-INT-01 regression test verifies.

**Q3: Does B.6 data model comply with P8?**
Yes. All 12+ schemas are Pydantic. CausalChain dataclass violation noted as DEFER. B.10 L-INT-01 documents Attempt 3’s `.model_dump()` anti-pattern; rebuild returns typed models.

**Q4: Are B.3 interface contracts consistent with shared-contracts.md?**
Verified: Section 1.5 intelligence schemas ✓, Section 2.6 orchestrator calls ✓, Section 3 memory access ✓. Gap: `generate_research_agenda`/`get_intellectual_summary` not in Section 2.6 (secondary methods, not orchestrator-invoked). Not a conflict.

**Q5: Does B.4 cover every A.2 file?**
All 11 files covered: 5 REBUILD, 6 DEFER, 0 KILL. ✓

**Q6: Does B.8 include acceptance tests per P11?**
Yes. 3 acceptance tests (AT-INT-01 through AT-INT-03) hit running server with real requests. All fail if implementation deleted (R10). ✓

### B.13 Design Quality Scorecard

| # | Criterion | Score (1-5) | Justification |
|---|---|---|---|
| 1 | Volume 0 compliance | 5 | All 11 principles addressed. P1, P5, P8, P9, P11, R6 explicitly designed for. |
| 2 | Interface contract precision | 4 | All 5 REBUILD interfaces specified with signatures, types, deps. Shared contracts match. Minor gap: secondary methods not in shared-contracts 2.6. |
| 3 | Scope triage completeness | 5 | All 11 files triaged. 5 REBUILD, 6 DEFER, 0 KILL. Every verdict justified. 5 cross-cutting notes. |
| 4 | Error handling specificity | 4 | Error types, propagation, recovery documented. Regression test for silent swallowing. Minor gap: no custom IntelligenceError. |
| 5 | Testing coverage | 5 | 3 acceptance, 5 integration, 9 unit, 2 regression tests. All acceptance fail if implementation deleted. P11 tiered. |
| 6 | Data model precision | 5 | All schemas documented with fields, types, constraints, frozen status. C-03 ownership respected. Extension schemas defined. |
| 7 | Configuration clarity | 4 | 9 config fields with env vars, types, defaults, ranges. Feature flag documented. Minor: no acquisition config (DEFER). |
| 8 | Lessons learned specificity | 5 | 6 concrete lessons citing file:line. Raw dicts, singletons, string-replace, keyword detection, metadata nesting, synthetic placeholders. |
| 9 | Cross-volume consistency | 4 | C-03, C-08 addressed. Shared contracts verified. Dependencies declared. Minor: IntellectualProfile L9 field needs Vol 1 change. |

**Total: 41/45** (passing threshold: 30/45)

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (7 intelligence + 4 acquisition files, 5+ docs), context brief, and 3 known failure warnings including boundary overlap with Volume 3 | Created the intelligence pipeline analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V05-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
|| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 source manifest per DISTILLATION_PROTOCOL.md Section 5 | Tagged files as essential vs. nice-to-have for the rebuild analysis |
|| v5 | 2026-03-10 | Oz Phase 1 Agent | Phase 1 distillation: filled B.1 (purpose), B.2 (architecture with ASCII diagram, 11 component responsibilities), B.3 (interface contracts for all 11 components with exact method signatures, schemas, and dependency maps), B.4 (scope triage: 5 REBUILD, 6 DEFER, 0 KILL), plus 5 cross-cutting rebuild notes from oversight self-review. Registered 9 ownership claims, 6 dependency declarations, and 2 conflict flags in AGENT_COMM.md. | Completed the first analysis pass: defined what the intelligence system should do, how it should be structured, its exact interfaces, and which parts to rebuild vs. delay |
| v6 | 2026-03-11 | Oz Phase 2 Agent | Phase 2 distillation: filled B.5 (technology — Pydantic v2, structlog, no LLM/ML dep, DI replaces singletons), B.6 (data model — 8 consumed + 5 owned schemas, canonical analogies as Pydantic constants), B.7 (error handling — 3 types, 5 propagation rules, 3 recovery patterns), B.8 (testing — 3 acceptance, 5 integration, 9 unit, 2 regression), B.9 (9 config fields with feature flag), B.10 (6 lessons with file:line citations), B.11 (5 discoveries including R6 gold standard), B.12 (6-question self-review, all A.4 items addressed), B.13 (scorecard 41/45). Created agent-comm/vol-05.md. | Completed the deep-dive: specified exactly how to build the intelligence system including schemas, errors, tests, config, and lessons |
