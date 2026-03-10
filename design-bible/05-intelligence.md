# ATLAS Design Bible — Volume 5: Intelligence Pipeline

| Field | Value |
|---|---|
| **Doc ID** | `DB-V05-001` |
| **Name** | Volume 5: Intelligence Pipeline |
| **Purpose** | Design specification for intellectual amplification — analogical reasoning, hypothesis generation, Socratic challenge, and growth tracking |
| **Owner** | Design Bible / Volume 5 |
| **Status** | `phase-1-complete` |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / Oz Phase 1 Distillation Agent (Part B) |
| **Version** | v5 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

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
| ContentQueue | `src/acquisition/content_queue.py` | **DEFER** | Priority heap with Pydantic validation, persistence, dedup, retry. Well-designed utility. However, it only serves the acquisition layer which is itself deferred. Defer alongside acquisition. |

**Cross-cutting rebuild notes (from oversight self-review):**

1. **P5 violation — silent error swallowing**: All REBUILD components use `except Exception as e: logger.debug(...)` throughout (coordinator lines 108-145, reasoner lines 344-345, generator lines 166-167, challenger lines 136-137). This silently degrades to empty results rather than classifying and routing errors per Volume 0 P5. The rebuild must replace these with specific exception types from the shared error hierarchy and log at `warning` or `error` level.
2. **P9 — output governance integration**: Intelligence amplification results flow into the orchestrator's response pipeline. The rebuild must ensure that factual claims in amplification outputs (e.g., analogy explanations, hypothesis statements) pass through Volume 9's output governance gate before reaching the user. Intelligence does not self-govern — it produces candidate enrichments that the orchestrator governs.
3. **Singleton anti-pattern**: Every component (all 11 files) uses a module-global singleton with `get_*()` factory and `reset_*()` for testing. The rebuild must use constructor-based dependency injection with MemoryManager passed at initialization, not lazily acquired via global state. This eliminates hidden coupling and makes testing explicit.
4. **R6 strength — model independence**: The amplification layer is entirely symbolic + memory-based with zero direct LLM dependency. Canonical analogies, gap identification, and growth tracking work without any LLM API call. This is architecturally correct per Volume 0 R6 and must be preserved in the rebuild. LLM may enhance novel analogy discovery but must not be required.
5. **`Any` type annotations**: coordinator.py lines 93 and hypothesis_generator.py lines 145, 230, 343 use `Any` type: ignore annotations. The rebuild must use proper typed dicts or Pydantic models.

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
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (7 intelligence + 4 acquisition files, 5+ docs), context brief, and 3 known failure warnings including boundary overlap with Volume 3 | Created the intelligence pipeline analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V05-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 source manifest per DISTILLATION_PROTOCOL.md Section 5 | Tagged files as essential vs. nice-to-have for the rebuild analysis |
| v5 | 2026-03-10 | Oz Phase 1 Agent | Phase 1 distillation: filled B.1 (purpose), B.2 (architecture with ASCII diagram, 11 component responsibilities), B.3 (interface contracts for all 11 components with exact method signatures, schemas, and dependency maps), B.4 (scope triage: 5 REBUILD, 6 DEFER, 0 KILL), plus 5 cross-cutting rebuild notes from oversight self-review. Registered 9 ownership claims, 6 dependency declarations, and 2 conflict flags in AGENT_COMM.md. | Completed the first analysis pass: defined what the intelligence system should do, how it should be structured, its exact interfaces, and which parts to rebuild vs. delay |
