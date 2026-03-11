# Agent Communication — Volume 1: Memory System
## Phase 2 Distillation Outputs

---

## Ownership Claims

```
CLAIM: MemoryManager facade (memory_manager.py) — single entry point for all memory operations
OWNER: Volume 1
REASON: Core memory subsystem facade. Exposes start_conversation, add_message, assemble_context, end_conversation. No other volume claims it.
CONTESTED: no
```

```
CLAIM: L1 Working Memory (l1_working.py) — ephemeral conversation state
OWNER: Volume 1
REASON: In-memory message buffer, working context, event queue. Purely memory-domain.
CONTESTED: no
```

```
CLAIM: L2 Conversation Memory (l2_conversation.py) — persistent conversation storage
OWNER: Volume 1
REASON: SQLite-backed conversation and message persistence. Core memory layer.
CONTESTED: no
```

```
CLAIM: L3 Episodic Memory (l3_episodic.py) — interaction episodes
OWNER: Volume 1
REASON: Episode recording, retrieval, importance-weighted queries. Memory-domain.
CONTESTED: no
```

```
CLAIM: L4 Declarative Memory (l4_declarative.py) — facts, relations, evidence with FTS5
OWNER: Volume 1
REASON: Fact storage, full-text search, relation graph. Core knowledge persistence.
CONTESTED: no
```

```
CLAIM: L5–L9 Memory Layers (l5_procedural.py, l6_attention.py, l7_world.py, l8_goals.py, l9_social.py)
OWNER: Volume 1
REASON: All 10 memory layers are owned by Vol 1. Each is a self-contained SQLite-backed store.
CONTESTED: no
```

```
CLAIM: L10 Vector/Semantic Memory (l10_vector.py) — FAISS-based semantic search
OWNER: Volume 1
REASON: Embedding generation, FAISS indexing, similarity search. FAISS is the sole vector backend.
CONTESTED: no
```

```
CLAIM: Memory Pydantic schemas (schemas.py) — all schemas listed in B.6.1–B.6.9
OWNER: Volume 1
REASON: Message, Episode, Fact, Skill, FocusState, StateSnapshot, Goal, Plan, Progress, UserProfile, Interaction, PreferenceRule, OutcomeSignal, CommandEvidence, ValidationClaim. Memory-domain schemas only.
CONTESTED: no
```

```
CLAIM: Memory infrastructure (connection_manager.py, consolidator.py, backup_scheduler.py, health_monitor.py, integrity_checker.py, garbage_collection.py, embedding_model.py, cross_layer_query.py)
OWNER: Volume 1
REASON: SQLite connection management, L1→L2 consolidation, backup scheduling, health monitoring, integrity checking, garbage collection, embedding model singleton, cross-layer query engine. All memory infrastructure.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 1 (Memory) needs AtlasError base class from shared/errors.py (Volume 8)
STATUS: pending
INTERFACE: class AtlasError(Exception) — base for MemoryLayerError hierarchy.
NOTE: Tier 0 dependency. Must exist before Vol 1 can define DatabaseCorruptionError, SchemaValidationError, etc.
```

```
DEPENDENCY: Volume 1 (Memory) needs AtlasConfig from shared/config.py (Volume 8)
STATUS: pending
INTERFACE: AtlasConfig(BaseSettings) with env_prefix="ATLAS_". Memory reads ATLAS_MEMORY_DIR, ATLAS_MEMORY_READONLY, ATLAS_USE_FAISS, ATLAS_VECTOR_DIR, ATLAS_EMBEDDING_MODEL, ATLAS_EMBEDDING_PROVIDER, ATLAS_EMBEDDING_DIM, ATLAS_CONSOLIDATION_INTERVAL, ATLAS_MAX_L1_MESSAGES, ATLAS_L10_IVF_THRESHOLD, ATLAS_BACKUP_ENABLED, ATLAS_BACKUP_INTERVAL_HOURS.
```

```
DEPENDENCY: Volume 1 (Memory) needs structlog from shared/logging.py (cross-cutting)
STATUS: pending
INTERFACE: from atlas.shared.logging import get_logger -> structlog.BoundLogger
NOTE: Replaces loguru and hard-wired telemetry coupling. All memory subsystem logging via structlog.
```

```
DEPENDENCY: Volume 1 (Memory) needs NLP/LLM strategy from Volume 3 for MemoryConsolidator._extract_facts_from_messages()
STATUS: pending
INTERFACE: A callable that takes List[Message] and returns List[Fact] — exact interface TBD by Vol 3.
NOTE: Non-blocking for MVA. Consolidator can use rule-based extraction as fallback until Vol 3 provides LLM-based extraction.
```

---

## Conflict Flags

No new conflicts identified. All cross-volume schema ownership resolved per shared-contracts.md §1:
- Governance schemas → Vol 9 (not Vol 1)
- BERT classification schemas → Vol 2 (not Vol 1)
- Librarian schemas → Vol 5 (not Vol 1)
- APEX/prompt schemas → Vol 3/5 (not Vol 1)

---

## Discoveries for Other Volumes

**For Volume 0:**
- B.11.1: Singleton guard pattern for background threads (`_global_safeguards_started` + `threading.Lock`) should be promoted to Volume 0 as a standard for any subsystem spawning background workers.
- B.11.3: Pytest isolation guard (`"pytest" in sys.modules` → redirect DB paths to temp dirs) should be standardized system-wide as a Volume 0 testing principle.
- B.11.4: `BEGIN IMMEDIATE` transaction pattern for SQLite write-heavy operations prevents `SQLITE_BUSY` errors. Should be a Volume 0 recommendation for all SQLite-using subsystems.

**For Volume 2:**
- `MemoryManager.assemble_context(conversation_id, user_query)` returns a flat dict with keys: `messages`, `facts`, `episodes`, `attention`, `goals`, `world_state`, `profile`, `semantic_results`. Vol 2's orchestrator consumes this dict to build LLM context. No ranking/merging across layers — the orchestrator decides how to weight and use assembled context.

**For Volume 3:**
- `MemoryConsolidator._extract_facts_from_messages()` needs an NLP/LLM strategy to extract declarative facts from conversation messages. Vol 3 should provide a callable interface. Until available, Vol 1 uses rule-based extraction as fallback.
- `OutcomeSignal` schema (B.6.9) is owned by Vol 1, consumed by Vol 3 for learning pipeline feedback signals.

**For Volume 4:**
- `CommandEvidence`, `ValidationClaim`, `ValidationClaimType` schemas (B.6.9) are owned by Vol 1 as data-at-rest schemas, consumed by Vol 4 per C-07. Stored in L4 declarative memory.

**For Volume 8:**
- `shared/errors.py` must define `AtlasError` base class before Vol 1 can build `MemoryLayerError` and its 8 subtypes. This is a Tier 0 dependency.
- `shared/config.py` must define `AtlasConfig(BaseSettings)` with env_prefix support before Vol 1 can load its 12 configuration fields.

**For Volume 9:**
- Governance schemas that were in Attempt 3's `src/memory/schemas.py` are relocated to Vol 9. Vol 1 does not import or define any governance types.

---

## Phase 2 B.4 Verdict Amendment

One amendment from Phase 1:
- `schemas_governance.py` was listed as KILL in Phase 1 B.4 (correct). Phase 2 confirms: governance schemas relocate to Vol 9, not deleted from the system — just deleted from `src/memory/`. No B.4 verdict changes for the 43 files. 22 REBUILD + 5 DEFER + 16 KILL = 43 total.

---

## Modification History

| Version | Date | Modified By | Summary |
|---|---|---|---|
| v1 | 2026-03-11 | Distillation Agent V1-P2 | Initial creation — 9 ownership claims, 4 dependency declarations, 0 new conflicts, 7 cross-volume notifications, 1 B.4 amendment |
