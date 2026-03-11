# Agent Communication — Volume 6: Voice & Multimodal
## Phase 2 Distillation Outputs

---

## Ownership Claims

```
CLAIM: VoiceController (controller.py) — core STT→Atlas→TTS pipeline orchestrator
OWNER: Volume 6
REASON: Central voice subsystem component. Consumes orchestrator, governance, memory. No other volume claims it.
CONTESTED: no
```

```
CLAIM: TTSEngine Protocol and PiperTTSEngine implementation (tts.py, piper_tts.py)
OWNER: Volume 6
REASON: Local ONNX TTS engine is voice-domain infrastructure. Piper model, espeak-ng phonemization, WAV synthesis all owned by Vol 6.
CONTESTED: no
```

```
CLAIM: STTEngine Protocol (stt.py)
OWNER: Volume 6
REASON: Speech-to-text interface definition. No default implementation in rebuild (STT is deferred). Vol 6 owns the protocol.
CONTESTED: no
```

```
CLAIM: TextNormalizer (text_normalizer.py)
OWNER: Volume 6
REASON: TTS-specific text preprocessing. Pure string transforms with no external dependencies. Consumed only by TTS engines.
CONTESTED: no
```

```
CLAIM: Voice Pydantic schemas (voice/schemas.py) — VoiceControllerConfig, VoiceSession, VoiceControllerStatus, VoiceSettings, VoiceQuery, STTResult, TTSMetadata, VoiceResponse, AudioMetadata, AudioFormat, VoiceInteractionEpisode, and all speaker verification schemas
OWNER: Volume 6
REASON: All schemas serve voice subsystem exclusively. Speaker verification schemas included for design completeness even though implementation is deferred.
CONTESTED: no
```

```
CLAIM: Voice API route definitions (/v1/voice/*)
OWNER: Volume 6 (definitions); Volume 8 (registration and hosting)
REASON: Vol 6 defines the route handlers and request/response contracts. Vol 8 registers the APIRouter into the FastAPI app. Per shared-contracts.md §2.8, Vol 6 calls Vol 2 via the same interface as Vol 8.
CONTESTED: no
```

```
CLAIM: VoiceTools (tools/voice.py) — speak(), transcribe(), get_voice_status()
OWNER: Volume 6 (implementation); Volume 10 (registration)
REASON: Vol 6 implements voice tool handlers. Vol 10 registers them in the ToolRegistry.
CONTESTED: no
```

---

## Dependency Declarations

```
DEPENDENCY: Volume 6 (Voice) needs OrchestratorEngine from Volume 2
STATUS: pending
INTERFACE: OrchestratorEngine.process_message(message: str, session_id: str, device_id: str) -> ConversationResponse
NOTE: B.3 §3.1 incorrectly uses `process_query(query, session_id)`. Must align with shared-contracts.md §2.8 which specifies `process_message(message, session_id, device_id) -> ConversationResponse`.
```

```
DEPENDENCY: Volume 6 (Voice) needs GovernedOutput and OutputGovernor from Volume 9
STATUS: pending
INTERFACE: OutputGovernor.govern(content: str, phase: OutputPhase, evidence_store: EvidenceStore) -> GovernedOutput
NOTE: Replaces Attempt 3's voice-specific ApprovedUtterance. Per C-14 (resolved).
```

```
DEPENDENCY: Volume 6 (Voice) needs DecisionValidator from Volume 9
STATUS: pending
INTERFACE: DecisionValidator.validate(command: str, bert_result) -> ValidationDecision
NOTE: Gates voice query safety before orchestrator processing.
```

```
DEPENDENCY: Volume 6 (Voice) needs MemoryManager.l3 from Volume 1
STATUS: pending
INTERFACE: MemoryManager.l3.record_episode(event_type: str, session_id: str, context: dict, outcome: str, importance: float) -> None
NOTE: Logs VoiceInteractionEpisode to L3 episodic memory. Non-blocking — failure does not crash pipeline.
```

```
DEPENDENCY: Volume 6 (Voice) needs AtlasError base class from shared/errors.py (Volume 8)
STATUS: pending
INTERFACE: class AtlasError(Exception) — base for VoiceSubsystemError hierarchy.
```

```
DEPENDENCY: Volume 6 (Voice) needs AtlasConfig from shared/config.py (Volume 8)
STATUS: pending
INTERFACE: AtlasConfig(BaseSettings) with env_prefix="ATLAS_". Voice reads ATLAS_ENABLE_VOICE, ATLAS_VOICE_TTS_ENGINE, ATLAS_VOICE_STT_ENGINE, ATLAS_VOICE_SPEAKER_VERIFY, ATLAS_VOICE_SPEAKER_THRESHOLD, ATLAS_VOICE_DEFAULT_SPEED, ATLAS_VOICE_SESSION_TIMEOUT, ATLAS_VOICE_VOICEPRINT_DIR.
```

```
DEPENDENCY: Volume 6 (Voice) needs structlog from shared/logging.py (cross-cutting)
STATUS: pending
INTERFACE: from atlas.shared.logging import get_logger -> structlog.BoundLogger
```

```
DEPENDENCY: Volume 6 (Voice) needs API route registration from Volume 8
STATUS: pending
INTERFACE: Vol 8 includes Vol 6's APIRouter via `app.include_router(voice_router)` during server factory.
```

```
DEPENDENCY: Volume 6 (Voice) needs tool registration from Volume 10
STATUS: pending
INTERFACE: ToolRegistry.register(tool_name, handler, schema) for speak, transcribe, get_voice_status.
```

---

## Conflict Flags

```
CONFLICT: B.3 §3.1 method name mismatch with shared-contracts.md §2.8
VOLUMES: 6 vs shared-contracts
DESCRIPTION: B.3 §3.1 specifies VoiceController consumes `OrchestratorEngine.process_query(query, session_id)` but shared-contracts.md §2.8 defines the canonical signature as `process_message(message, session_id, device_id) -> ConversationResponse`. The shared contract is binding per DISTILLATION_PROTOCOL §4.
RESOLUTION: Vol 6 must use `process_message` as specified in shared-contracts.md. This is a Phase 1 documentation error in B.3 that does not affect the design intent — VoiceController delegates to the orchestrator regardless of method name. Flagged here; correction should be applied when coding begins.
STATUS: acknowledged (Vol 6 conforms to shared contract)
```

```
CONFLICT ACKNOWLEDGEMENT: C-09 (TTS/STT Voice Logic in Console — Vol 6 vs Vol 7)
VOLUMES: 6 vs 7
DESCRIPTION: Vol 7 identified that ChatPanel.tsx inlines Cartesia/OpenAI TTS/STT logic that belongs to Vol 6. Vol 6 acknowledges this.
RESOLUTION: Vol 6 owns TTS/STT backend implementation. Vol 7 extracts inlined voice code from ChatPanel.tsx and consumes Vol 6's REST API (/v1/voice/tts/jarvis, /v1/voice/query). No client-side TTS/STT SDK needed — all voice processing is server-side via API. Cloud TTS proxies (/api/tts, /api/tts/cartesia) are DEFER'd in Vol 6 B.4; if Vol 7 needs them before Vol 6 rebuilds them, Vol 7 may implement them as thin API proxies under Vol 8's route registration.
STATUS: acknowledged
```

```
CONFLICT ACKNOWLEDGEMENT: C-14 (GovernedOutput supersedes ApprovedUtterance — Vol 6 vs Vol 9)
VOLUMES: 6 vs 9
DESCRIPTION: Already resolved. GovernedOutput is the single egress schema. Vol 6 KILLs governance.py and consumes Vol 9's GovernedOutput.
STATUS: resolved (no action needed)
```

---

## Discoveries for Other Volumes

**For Volume 0:**
- B.11.1: Voice governance pattern (create → hash → stamp → validate before output) should be promoted to a Volume 0 principle: **P12: All Egress Is Governed**. Every output channel (text, voice, tool execution, file write) should pass through a governance gate.
- B.11.2: Lazy-load pattern for heavy ML models (module-level singleton, async init, ThreadPoolExecutor) appears in Vol 1, Vol 3, Vol 5, and Vol 6. Should be standardized as a `LazyModelLoader` base class in `shared/`.
- B.11.3: Apple Silicon FAISS/PyTorch OpenMP thread-pool conflict (speaker_verifier.py:117-118) requires `OMP_NUM_THREADS=1` before PyTorch import. Any subsystem mixing FAISS and PyTorch must apply this guard.

**For Volume 2:**
- VoiceController calls `OrchestratorEngine.process_message(message, session_id, device_id)` per shared-contracts.md §2.8. The VoiceController passes the STT transcript as `message` and the voice session ID as `session_id`. Vol 2 should treat voice queries identically to text queries — voice is just a transport modality.

**For Volume 7:**
- Cloud TTS proxy endpoints (`/api/tts`, `/api/tts/cartesia`, `/api/stt/elevenlabs/*`) are DEFER'd in Vol 6. If Vol 7 console needs cloud TTS before Vol 6 rebuilds these, Vol 7 can implement them as thin backend proxies under Vol 8 route registration. The key requirement is keeping API keys server-side.

**For Volume 8:**
- `shared/errors.py` must define `AtlasError` base class before Vol 6 can build `VoiceSubsystemError` and its subtypes. This is a Tier 0 dependency.
- `shared/config.py` must define `AtlasConfig(BaseSettings)` with env_prefix support before Vol 6 can load its 8 configuration fields.
- Voice API routes are registered as `APIRouter(tags=["voice"])`. Vol 8 includes them via `app.include_router()` during server factory startup.

**For Volume 9:**
- Vol 6 consumes `GovernedOutput` from `governance/schemas.py` and `OutputGovernor.govern()` from `governance/output.py`. These must be available before voice can produce governed speech output.
- Vol 6 consumes `DecisionValidator.validate()` for query safety gating. Same interface as Vol 2.

**For Volume 10:**
- VoiceTools (`speak`, `transcribe`, `get_voice_status`) must be registered in ToolRegistry so the orchestrator's LLM function-calling can invoke them.

---

## Phase 2 B.4 Verdict Amendment

No B.4 verdict changes from Phase 1. All REBUILD/DEFER/KILL decisions remain as specified. Phase 2 source reading confirmed:
- `governance.py` KILL is correct — GovernedOutput supersedes ApprovedUtterance.
- `speaker_verifier.py` DEFER is correct — heavy dependencies, non-MVP, design preserved for later.
- `realtime_webrtc_signaling.py` DEFER is correct — external API dependency, not basic voice.
- `xtts_tts.py` DEFER is correct — requires external server, Piper is sufficient for MVP.

---

## Modification History

| Version | Date | Modified By | Summary |
|---|---|---|---|
| v1 | 2026-03-11 | Distillation Agent V6 (Phase 2) | Initial creation — 7 ownership claims, 9 dependency declarations, 3 conflict flags (1 new method-name mismatch, 2 acknowledgements), 6 cross-volume notifications, 0 B.4 amendments |
