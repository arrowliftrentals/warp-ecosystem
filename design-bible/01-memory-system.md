# ATLAS Design Bible — Volume 1: Memory System

| Field | Value |
|---|---|
| **Doc ID** | `DB-V01-001` |
| **Name** | Volume 1: Memory System |
| **Purpose** | Design specification for the L1-L10 cognitive memory architecture — Atlas's primary competitive moat |
| **Owner** | Design Bible / Volume 1 |
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
- **Volume 1: Memory System (L1-L10)**
- **Purpose:** Provides all persistent and ephemeral context storage for Atlas — the 10-layer cognitive memory architecture that is the system's primary competitive moat.
- **Rebuild phase:** Phase 1 (immediately after conversation loop skeleton). Memory is the foundation — everything else depends on it. See Volume 0 R2.

### A.2 Source Manifest

**Code files to read** (paths relative to `atlas/`):
- `src/memory/__init__.py`
- `src/memory/memory_manager.py` — central coordinator for all layers
- `src/memory/schemas.py` — core Pydantic schemas for memory data
- `src/memory/schemas_analysis.py`
- `src/memory/schemas_awareness.py`
- `src/memory/schemas_demo.py`
- `src/memory/schemas_diagnostics.py`
- `src/memory/schemas_execution.py`
- `src/memory/schemas_learning.py`
- `src/memory/schemas_monitoring.py`
- `src/memory/schemas_multimodal.py`
- `src/memory/schemas_patterns.py`
- `src/memory/schemas_personality.py`
- `src/memory/schemas_plugin.py`
- `src/memory/schemas_printer.py`
- `src/memory/schemas_reasoning.py`
- `src/memory/schemas_research.py`
- `src/memory/schemas_semantic.py`
- `src/memory/schemas_subsystem.py`
- `src/memory/schemas_training.py`
- `src/memory/l1_working.py` — L1 Working Memory (ephemeral, in-memory)
- `src/memory/l2_short_term.py` — L2 Short-term (SQLite, hours-to-days)
- `src/memory/l3_episodic.py` — L3 Episodic (interactions + temporal queries)
- `src/memory/l4_declarative.py` — L4 Declarative (facts + FTS5 search)
- `src/memory/l5_procedural.py` — L5 Procedural (skills + execution tracking)
- `src/memory/l6_attention.py` — L6 Attention (focus tracking)
- `src/memory/l7_world_state.py` — L7 World State (environment snapshots)
- `src/memory/l8_goals.py` — L8 Goals (planning, hierarchies)
- `src/memory/l9_social.py` — L9 Social (user profiles, interaction patterns)
- `src/memory/l10_vector.py` — L10 Vector (semantic retrieval, ChromaDB)
- `src/memory/l10_vector_faiss.py` — L10 alternative FAISS implementation
- `src/memory/l10_bootstrap.py` — L10 bootstrap/initialization
- `src/memory/l10_collections.py` — L10 collection management
- `src/memory/consolidation.py` — memory consolidation across layers
- `src/memory/connection_manager.py` — SQLite connection pooling
- `src/memory/cross_layer_queries.py` — queries spanning multiple layers
- `src/memory/database_health.py` — DB health monitoring
- `src/memory/embedding_model.py` — embedding generation for L10
- `src/memory/garbage_collection.py` — memory cleanup
- `src/memory/goal_lifecycle.py` — goal state transitions (L8)
- `src/memory/integrity.py` — data integrity checks
- `src/memory/relation_writer.py` — inter-entity relations
- `src/memory/backup.py` — memory backup utilities

**Documentation to read:**
- `docs/architecture/memory-manager.md`
- `docs/architecture/memory-context.md`
- `docs/architecture/memory-tools.md`
- `docs/architecture/memory-extended-tools.md`
- `docs/guides/memory-layers-verification.md`
- `docs/guides/memory-fixes-verification.md`
- `docs/architecture/exhaustive-cognitive-architecture-analysis.md` (memory sections)

**Test files to read:**
- `tests/memory/` (entire directory)

**CORE/PERIPHERAL Classification** (per `DISTILLATION_PROTOCOL.md` Section 5):
- **CORE** (17 files): `__init__.py`, `memory_manager.py`, `schemas.py`, all 10 layer implementations (`l1_working.py` through `l10_vector.py`), `consolidation.py`, `connection_manager.py`, `cross_layer_queries.py`, `embedding_model.py`
- **PERIPHERAL** (26 files): All `schemas_*.py` variants (17 files), `l10_vector_faiss.py`, `l10_bootstrap.py`, `l10_collections.py`, `database_health.py`, `garbage_collection.py`, `goal_lifecycle.py`, `integrity.py`, `relation_writer.py`, `backup.py`

### A.3 Context Brief

**What worked in Attempt 3:**
- All 10 memory layers were implemented with SQLite/FAISS backing
- Pydantic schemas existed for L3-L9
- MemoryManager coordinated access across layers
- Cross-layer queries functioned
- FTS5 search on L4 declarative memory worked
- Memory consolidation pipeline existed

**What failed or was never wired:**
- L1, L2, L10 lacked Pydantic validation (data could enter without schema checks)
- Four separate vector store implementations with confused import paths (L10 vector, L10 vector FAISS, ChromaDB, and a storage/ Protocol hierarchy)
- Schema proliferation: 15+ schema files with unclear ownership boundaries
- Consolidation pipeline existed but unclear if it ran automatically or was manual-only
- Garbage collection existed but unclear if it was ever triggered

**What was simulated/fake:**
- No evidence of simulated capabilities in memory system specifically (memory was one of the more real subsystems)

**Relevant Volume 0 principles:**
- P6: Memory is the foundation, not a feature
- P8: Pydantic schemas at every boundary
- P3: Nothing ships without integration
- R2: Memory first — built before any other subsystem
- R10: Data migration is opt-in, not default

### A.4 Known Failures & Warnings
1. **Vector store confusion**: Four implementations exist. The distillation agent must decide which approach the rebuild uses and KILL the rest. Do not carry forward the confusion.
2. **Schema sprawl**: 15+ schema files suggest the schema surface area grew without governance. Determine which schemas are actually needed vs. which were speculative.
3. **L1/L2/L10 validation gap**: These layers lacked Pydantic validation. The rebuild must close this gap per P8.
4. **Connection management**: SQLite connection pooling was implemented but may have concurrency issues under async workloads. Investigate.

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
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (43 code files, 7 docs), context brief, and 4 known failure warnings | Created the memory system analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V01-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 Source Manifest per DISTILLATION_PROTOCOL.md Section 5 | Labeled which files agents should read in full vs. skim during Phase 1 |
