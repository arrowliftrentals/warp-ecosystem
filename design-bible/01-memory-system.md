# ATLAS Design Bible — Volume 1: Memory System

| Field | Value |
|---|---|
| **Doc ID** | `DB-V01-001` |
| **Name** | Volume 1: Memory System |
| **Purpose** | Design specification for the L1-L10 cognitive memory architecture — Atlas's primary competitive moat |
| **Owner** | Design Bible / Volume 1 |
| **Status** | `draft` (B.1-B.4 filled by distillation agent) |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / Distillation Agent V1 (Part B) |
| **Version** | v5 |
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
The Memory System is Atlas's foundational subsystem and primary competitive moat: a 10-layer cognitive memory architecture that stores and retrieves all conversational, factual, procedural, social, and semantic context. Per Volume 0 (R2), this subsystem must be rebuilt before other volumes because every major path depends on it.

The intended design is a layered, type-validated memory graph coordinated through a single facade (`MemoryManager`) rather than direct layer access. Layers are separated by temporal role and data shape:
- L1/L2: active and short-term conversation state
- L3/L4: episodic and declarative knowledge
- L5/L6: procedural execution + attention weighting
- L7/L8/L9: world state, goals, social/user profile
- L10: semantic retrieval via vector search

Non-negotiable rebuild constraints from system principles:
- P6: Memory is the foundation, not a feature
- P8: Pydantic validation at boundaries
- P3: No isolated layer shipping without integration
- R10: Data migration is opt-in, not default

### B.2 Architecture Overview
```
                         +-------------------------------+
                         |       Orchestrator (V2)       |
                         |      calls assemble_context    |
                         +---------------+---------------+
                                         |
                         +---------------v---------------+
                         |          MemoryManager         |
                         |  (single facade, lazy init)   |
                         +-+--+--+--+--+--+--+--+--+--+-+
                           |  |  |  |  |  |  |  |  |  |
                      +----v++v----++v----++v----++v----+
                      | L1  || L2  || L3  || L4  || L5  |
                      |Work ||Short||Epis ||Decl ||Proc |
                      +-----++-----++-----++-----++-----+
                      +----v++v----++v----++v----++v----+
                      | L6  || L7  || L8  || L9  || L10 |
                      |Attn ||World||Goals||Soc  ||Vec  |
                      +-----++-----++-----++-----++-----+
                                               |
                                        +------v------+
                                        | Embeddings  |
                                        | FAISS/Chroma|
                                        +-------------+

Infrastructure companions:
- connection_manager.py (SQLite pooling + WAL)
- consolidation.py (periodic L1->L2 consolidation)
- backup.py + database_health.py (safeguards, recovery, monitoring)
- cross_layer_queries.py (composed retrieval patterns)
```

Key design intent extracted from source:
1. **Facade + lazy initialization**: `MemoryManager` owns all layer lifecycles and initializes on-demand with thread guards.
2. **L1-first fallback strategy**: reads go L1 first (speed), then L2 fallback (durability).
3. **Cross-layer context assembly is core**: `assemble_context()` composes messages, facts, episodes, attention, goals, world-state, and profile.
4. **Operational safeguards are built-in**: periodic consolidation, backup scheduler, DB health monitor, and path guards for pytest isolation.
5. **Vector backend confusion exists**: both FAISS and Chroma paths are wired; rebuild must select one canonical implementation.

### B.3 Interface Contracts
#### B.3.1 Public Facade (`MemoryManager`)
Primary cross-volume interface; consumers should use this API instead of importing individual layers.

Core lifecycle and conversation methods:
- `start_conversation(conversation_id: str, device_id: str) -> ConversationState`
- `add_message(conversation_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None`
- `get_recent_messages(conversation_id: str, limit: int = 10) -> List[Dict[str, str]]`
- `get_messages(conversation_id: str, limit: int = 50) -> List[Dict[str, str]]`
- `update_context(conversation_id: str, key: str, value: Any) -> None`
- `get_context(conversation_id: str) -> Dict[str, Any]`
- `get_conversation(conversation_id: str) -> Optional[ConversationState]`
- `add_intent(conversation_id: str, intent_type: str) -> None`
- `end_conversation(conversation_id: str) -> None`
- `get_recent_conversations(hours: int = 24, limit: int = 10) -> List[Dict[str, Any]]`
- `cleanup_old(hours: int = 24) -> int`

Cross-layer retrieval and synthesis methods:
- `assemble_context(conversation_id: str, user_query: Optional[str] = None, max_messages: int = 10, max_facts: int = 5, max_episodes: int = 3, max_semantic: int = 5) -> Dict[str, Any]`
- `retrieve_with_attention(query: str, n_results: int = 5, conversation_filter: Optional[str] = None) -> List[Dict[str, Any]]`
- `inject_relevant_facts(query: str, max_facts: int = 5) -> List[Dict[str, Any]]`
- `search_similar_messages(query: str, n_results: int = 5, conversation_filter: Optional[str] = None) -> List[Dict[str, Any]]`
- `find_relevant_context(conversation_id: str, query: str, n_results: int = 3) -> List[Dict[str, Any]]`
- `get_stats() -> Dict[str, Any]`

Layer accessors and infra hooks:
- Properties `l1` ... `l10` expose lazy-loaded layer instances.
- `get_l10_collection_manager()` exposes advanced L10 collections path.
- `close()` tears down background threads/monitors.

#### B.3.2 Layer-Level Contracts (by responsibility)
- **L1 (`l1_working.py`)**: in-memory active conversation state and intent/context updates.
- **L2 (`l2_short_term.py`)**: short-term persisted conversation/message/context storage + cleanup.
- **L3 (`l3_episodic.py`)**: episodic event recording and temporal range retrieval.
- **L4 (`l4_declarative.py`)**: declarative fact storage and FTS5 retrieval (`search_facts`).
- **L5 (`l5_procedural.py`)**: skills, execution records, and procedural memory stats.
- **L6 (`l6_attention.py`)**: focus/attention state used to weight retrieval.
- **L7 (`l7_world_state.py`)**: world snapshots and latest-state read.
- **L8 (`l8_goals.py`)**: goals, plans, and lifecycle/status transitions.
- **L9 (`l9_social.py`)**: user profile/preferences and interaction history.
- **L10 (`l10_vector.py` / `l10_vector_faiss.py`)**: semantic indexing/search over message corpus.

#### B.3.3 Schema Contracts (`schemas.py`)
Core validated types used at memory boundaries:
- L1/L2 basics: `WorkingMemoryItem`, `Message`, `BufferedEvent`, `ConversationMetadata`
- L3/L4: `Episode`, `EventType`, `Fact`, `FactSource`, `FactRelation`, `FactEvidence`
- L5: `Skill`, `SkillExecution`, `SkillImprovement`, plus APEX prompt strategy family
- L6/L7/L8/L9: `FocusState`, `StateSnapshot`, `Goal`, `Plan`, `Progress`, `UserProfile`, `Interaction`
- Governance-related schema families currently present in this file:
  - Output governance (`GovernedOutput`, `ExtractedClaim`, `EvidenceItem`, `EvidenceContract`)
  - Voice governance (`ApprovedUtterance`, `AuthorityLevel`)
  - BERT classification, librarian, and meta-assessment families

Boundary decision for rebuild: keep only Volume 1 memory schemas in this module; move governance/learning/librarian/orchestrator-specific schema families to owning volumes.

#### B.3.4 Shared Infrastructure Contracts
- `connection_manager.py`: SQLite connection pooling and WAL behavior.
- `embedding_model.py`: embedding generation abstraction used by L10.
- `consolidation.py`: movement and summarization patterns between layers.
- `backup.py` + `database_health.py`: data safety, integrity checks, alerting/recovery.

### B.4 Scope Triage
Verdict applied to all 43 code files in A.2.

#### REBUILD (22)
- `src/memory/__init__.py`
- `src/memory/memory_manager.py`
- `src/memory/schemas.py` (memory schema subset retained; non-memory subsets split out)
- `src/memory/l1_working.py`
- `src/memory/l2_short_term.py`
- `src/memory/l3_episodic.py`
- `src/memory/l4_declarative.py`
- `src/memory/l5_procedural.py`
- `src/memory/l6_attention.py`
- `src/memory/l7_world_state.py`
- `src/memory/l8_goals.py`
- `src/memory/l9_social.py`
- `src/memory/l10_vector.py` (single canonical vector path required in rebuild)
- `src/memory/consolidation.py`
- `src/memory/connection_manager.py`
- `src/memory/cross_layer_queries.py`
- `src/memory/database_health.py`
- `src/memory/embedding_model.py`
- `src/memory/garbage_collection.py`
- `src/memory/goal_lifecycle.py`
- `src/memory/integrity.py`
- `src/memory/backup.py`

#### DEFER (5)
- `src/memory/l10_vector_faiss.py` (defer as alternate backend; avoid dual implementation in MVA)
- `src/memory/l10_bootstrap.py`
- `src/memory/l10_collections.py`
- `src/memory/relation_writer.py`
- `src/memory/schemas_semantic.py`

#### KILL (16)
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
- `src/memory/schemas_subsystem.py`
- `src/memory/schemas_training.py`

Scope notes:
- Output governance schema family in `schemas.py` belongs to Volume 9 in rebuild ownership terms.
- APEX prompt strategy schema family belongs to Volume 3/5 boundary.
- BERT classification schema belongs to Volume 2 boundary.
- Librarian schema family belongs to Volume 5 boundary.
- Meta-assessment schemas are kill candidates for this rebuild track.

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
| v5 | 2026-03-10 | Distillation Agent V1 | Phase 1 distillation: filled B.1-B.4 (purpose, architecture, interface contracts, and full 43-file scope triage) | Captured how memory works, what interfaces it exposes, and what to keep/defer/delete in rebuild |
