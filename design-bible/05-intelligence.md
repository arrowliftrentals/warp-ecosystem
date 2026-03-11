# ATLAS Design Bible — Volume 5: Intelligence Pipeline

| Field | Value |
|---|---|
| **Doc ID** | `DB-V05-001` |
| **Name** | Volume 5: Intelligence Pipeline |
| **Purpose** | Design specification for intellectual amplification — analogical reasoning, hypothesis generation, Socratic challenge, and growth tracking |
| **Owner** | Design Bible / Volume 5 |
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
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (7 intelligence + 4 acquisition files, 5+ docs), context brief, and 3 known failure warnings including boundary overlap with Volume 3 | Created the intelligence pipeline analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V05-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 source manifest per DISTILLATION_PROTOCOL.md Section 5 | Tagged files as essential vs. nice-to-have for the rebuild analysis |
