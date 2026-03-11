# Agent Communication — Volume 6: Voice & Multimodal
## Phase 2 Distillation Outputs

---

## Ownership Claims

CLAIM: VoiceController — OWNER: Vol 6 — core STT→Atlas→TTS pipeline orchestrator
CLAIM: TTSEngine/PiperTTSEngine — OWNER: Vol 6 — local ONNX TTS infrastructure
CLAIM: STTEngine Protocol — OWNER: Vol 6 — interface definition (no impl in rebuild)
CLAIM: TextNormalizer — OWNER: Vol 6 — TTS text preprocessing
CLAIM: Voice Pydantic schemas — OWNER: Vol 6 — all 13 schemas serve voice exclusively
CLAIM: Voice API routes (/v1/voice/*) — OWNER: Vol 6 (defs); Vol 8 (registration)
CLAIM: VoiceTools — OWNER: Vol 6 (impl); Vol 10 (registration)

---

## Dependency Declarations

DEP: Vol 6 → Vol 2: OrchestratorEngine.process_message(message, session_id, device_id) → ConversationResponse [pending]
DEP: Vol 6 → Vol 9: GovernedOutput + OutputGovernor.govern() [pending]
DEP: Vol 6 → Vol 9: DecisionValidator.validate() for query safety gating [pending]
DEP: Vol 6 → Vol 1: MemoryManager.l3.record_episode() for VoiceInteractionEpisode [pending]
DEP: Vol 6 → Vol 8: AtlasError base class from shared/errors.py [pending]
DEP: Vol 6 → Vol 8: AtlasConfig from shared/config.py [pending]
DEP: Vol 6 → shared: structlog from shared/logging.py [pending]
DEP: Vol 6 → Vol 8: API route registration via app.include_router() [pending]
DEP: Vol 6 → Vol 10: Tool registration in ToolRegistry [pending]

---

## Conflict Flags

CONFLICT: B.3 §3.1 uses process_query but shared-contracts.md §2.8 defines process_message. Vol 6 conforms to shared contract. STATUS: acknowledged.

CONFLICT ACK: C-09 — TTS/STT logic inlined in ChatPanel.tsx belongs to Vol 6. Vol 7 extracts and consumes REST API. STATUS: acknowledged.

CONFLICT ACK: C-14 — GovernedOutput supersedes ApprovedUtterance. Vol 6 KILLs governance.py. STATUS: resolved.

---

## Discoveries for Other Volumes

Vol 0: Egress governance pattern → P12 candidate. Lazy model loader standardization. Apple Silicon OpenMP guard.
Vol 2: VoiceController calls process_message per shared-contracts.md §2.8. Voice = text transport modality.
Vol 7: Cloud TTS proxies DEFER'd. Vol 7 may implement thin proxies if needed before Vol 6 rebuild.
Vol 8: AtlasError (Tier 0 dep). AtlasConfig needed. Voice routes as APIRouter.
Vol 9: GovernedOutput + DecisionValidator consumed.
Vol 10: VoiceTools (speak, transcribe, get_voice_status) need ToolRegistry registration.

---

## Phase 2 B.4 Verdict Amendment

No changes. All REBUILD/DEFER/KILL decisions confirmed by Phase 2 source reading.

---

## Modification History

| Version | Date | Modified By | Summary |
|---|---|---|---|
| v1 | 2026-03-11 | Distillation Agent V6 (Phase 2) | Initial — 7 claims, 9 deps, 3 conflicts, 6 cross-vol notifications |
