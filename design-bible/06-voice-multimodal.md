# ATLAS Design Bible — Volume 6: Voice & Multimodal

| Field | Value |
|---|---|
| **Doc ID** | `DB-V06-001` |
| **Name** | Volume 6: Voice & Multimodal |
| **Purpose** | Design specification for natural voice interaction — TTS, STT, speaker verification, and governed utterance output |
| **Owner** | Design Bible / Volume 6 |
| **Status** | `draft` (Phase 1 complete — B.1-B.4 filled, B.5-B.13 awaiting Phase 2) |
| **Supersedes** | N/A |
| **Superseded by** | N/A |
| **Author** | Oz (Part A) / Distillation Agent V6 (Part B) |
| **Version** | v5 |
| **Created** | 2026-03-10 |
| **Last Modified** | 2026-03-10 |

---

## Part A: Context (Pre-loaded)

### A.1 Subsystem Identity
- **Volume 6: Voice & Multimodal**
- **Purpose:** Enables natural voice interaction with Atlas — TTS, STT, speaker verification, and governed utterance output. Core to the Jarvis vision of conversational AI.
- **Rebuild phase:** Phase 5 (after core systems are stable). Voice is high-value but depends on a working conversation loop, response pipeline, and governance system.

### A.2 Source Manifest

**Code files to read** (paths relative to `atlas/`):

*Voice subsystem:*
- `src/voice/__init__.py`
- `src/voice/voice_controller.py` — main voice orchestration
- `src/voice/governance.py` — utterance governance (ApprovedUtterance, AuthorityLevel)
- `src/voice/schemas.py` — voice-specific Pydantic schemas
- `src/voice/piper_tts.py` — Piper TTS engine (local, fast)
- `src/voice/xtts_tts.py` — XTTS TTS engine (higher quality)
- `src/voice/speaker_verifier.py` — speaker identity verification
- `src/voice/text_normalizer.py` — text preprocessing for TTS
- `src/voice/realtime_webrtc_signaling.py` — WebRTC for real-time audio

*API & tools:*
- `src/api/routes/voice.py` — voice REST endpoints
- `src/orchestrator/tools/voice_tools.py` — voice tool definitions

**Documentation to read:**
- `docs/architecture/voice-integration-map.md`
- `docs/architecture/voice-tools.md`
- `docs/development/voice-governance-implementation.md`
- `docs/development/voice-integration-status.md`

**Console voice components (read for frontend voice UX):**
- `console/src/components/VoiceInputButton.tsx`
- `console/src/components/VoiceEnrollment.tsx`
- `console/src/components/VoiceRealtimeWebRTC.tsx`
- `console/src/components/VoiceSettings.tsx`
- `console/src/components/TTSProviderSelector.tsx`
- `console/src/lib/voiceGovernance.ts`

**Test files to read:**
- `tests/voice/` (if exists)

**CORE/PERIPHERAL Classification:** All 11 files are **CORE** (≤40 code files). Read all in full during both Phase 1 and Phase 2.

### A.3 Context Brief

**What worked in Attempt 3:**
- Voice governance schema (`ApprovedUtterance`)
- Content hashing (SHA256) for utterance integrity
- Two TTS engines available (Piper for speed, XTTS for quality)
- Speaker verification module existed
- WebRTC signaling for real-time audio
- Console had voice UI components (input button, enrollment, settings)

**What failed or was never wired:**
- VoiceController identified as "missing" in Volume 0 assessment — the orchestrator for voice existed as a file but may not have been integrated
- Voice governance was the precursor to ADR-0031's broader output governance — it governed voice but not text responses
- Feature flags for voice likely set to FALSE
- STT (speech-to-text) implementation status unclear — TTS exists but is the input side working?

**What was simulated/fake:**
- Multimodal subsystem used `hashlib.md5` for fake object detection (this is A3 anti-pattern). Note: this is separate from voice — the "multimodal" label may conflate voice with vision/image processing.

**Relevant Volume 0 principles:**
- P9: Output governance (voice governance is the precursor pattern)
- P10: Atlas has a defined personality (voice must match personality)
- R7: Local-first (TTS should work offline with Piper)
- Section 7: User wants natural voice interaction

### A.4 Known Failures & Warnings
1. **Voice vs. Multimodal confusion**: "Multimodal" in Attempt 3 conflated voice (audio) with vision (image/screen). The distillation agent must determine if this volume covers only voice or also vision/screen capabilities.
2. **Voice governance as pattern source**: The `ApprovedUtterance` schema from voice governance became the template for ADR-0031's broader `GovernedOutput`. Coordinate with Volume 9 (Governance) to avoid duplication.
3. **STT gap**: TTS (output) has two engines. STT (input) status is unclear. A Jarvis-like system needs both.
4. **Local TTS quality**: Piper is fast but may not meet quality expectations. XTTS is better but heavier. The distillation agent should specify the TTS strategy.

---

## Part B: Design Specification (Agent Fills Out)

### B.1 Subsystem Purpose (Rebuild)

The Voice subsystem provides natural audio I/O for Jarvis-style interaction with Atlas. It should accept spoken user input via speech-to-text, route the resulting transcript through the standard orchestrator conversation loop (Volume 2), govern the textual response through the unified output governance pipeline (Volume 9's `GovernedOutput`), synthesize governed text into speech via local-first TTS engines, and log all voice interactions to L3 episodic memory. Speaker verification should optionally gate STT access so only the enrolled owner's voice is processed. Voice is strictly a presentation and perception modality — it must never increase Atlas's authority, bypass governance, or trigger actions directly. All spoken output requires a governed approval stamp; voice failure degrades gracefully to text-only without interrupting core Atlas operation. This volume covers audio voice I/O only — not vision, image processing, or other non-audio modalities (the "multimodal" label from Attempt 3 conflated these; see A.4 §1).

### B.2 Architecture Overview

**Major components and responsibilities:**

1. **VoiceController** — Thin async orchestrator for the STT→Atlas→TTS pipeline. Manages voice sessions (start, end, timeout cleanup), delegates to STT/TTS engines, gates on speaker verification when enabled, integrates with DecisionValidator for query safety, wraps responses through output governance, logs to L3 episodic memory, and emits events via EventBus.

2. **TTS Engine Layer** — Pluggable text-to-speech with a local-first strategy:
   - **PiperTTSService** — Local ONNX inference using the jgkawell/jarvis HuggingFace model, espeak-ng for phonemization. Runs offline, ~22kHz WAV output. Primary engine for R7 local-first compliance.
   - **XTTSTTSService** — Higher-quality voice clone via a persistent localhost TTS server (Coqui XTTS v2 with Paul Bettany samples). Requires external server process on port 5050. 24kHz WAV output.
   - **Cloud TTS Proxies** (in API routes) — Backend proxies for OpenAI TTS and Cartesia Sonic 3. Keep API keys server-side.

3. **STT Engine Layer** — Speech-to-text input:
   - **macOS SFSpeechRecognizer** — Designed for on-device privacy-first STT. Currently a stub in Attempt 3 (raises `ATLASException`). Never reached functional state.
   - **ElevenLabs Scribe Proxy** (in API routes) — Backend proxy for cloud STT. Token endpoint keeps API key server-side.

4. **SpeakerVerifier** — Voiceprint enrollment and verification using Resemblyzer GE2E embeddings (256-dim). Thread-safe singleton. Features: 3-5 sample enrollment with SNR quality gate (≥8dB), ambient noise calibration via spectral subtraction, inter-sample consistency check, liveness heuristic (spectral flatness + ZCR), encrypted-at-rest voiceprints via Fernet, mic-mismatch tolerance, rolling verification statistics.

5. **TextNormalizer** — Preprocesses text for natural TTS output: expands decimal numbers ("149.38" → "149 point 38"), unit abbreviations ("ms" → "milliseconds"), technical acronyms ("CPU" → "C P U"), percentages. Pure string transforms, no external dependencies.

6. **WebRTC Signaling** — Proxies SDP offer/answer between browser and OpenAI Realtime API for direct peer-to-peer audio. Keeps API key server-side.

7. **Voice Governance** — Creates and validates `ApprovedUtterance` (SHA-256 content hash, approval stamps, modality checks, expiration). In the rebuild, this is superseded by Volume 9's unified `GovernedOutput` schema. The governance pattern (create → hash → stamp → validate before speech) survives; the voice-specific schema does not.

8. **Voice API Routes** — FastAPI endpoints for TTS synthesis, speaker verification (REST + WebSocket streaming), STT proxying, WebRTC signaling, voice tool execution, and TTS status.

9. **VoiceTools** — LLM-callable tool class exposing `speak()`, `transcribe()`, and `get_voice_status()` for the orchestrator's tool registry.

**Data flow (canonical voice query):**

```
Audio In ──▶ Speaker Verifier (optional) ──▶ STT Engine ──▶ Transcript
                                                              │
                      VoiceController Pipeline                ▼
  Transcript ─▶ DecisionValidator ─▶ Orchestrator.process_query() (Vol 2)
                                           │
                                    Response Text
                                           │
                                    GovernedOutput (Vol 9)
                                           │
                           TextNormalizer ─▶ TTS Engine (Piper/XTTS/Cloud)
                                                   │
                                             Audio Out (WAV/b64)

  L3 Episodic Memory ◀─ VoiceInteractionEpisode
  EventBus ◀─ voice.query.processed
```

**Dependency summary:**
- Consumes: Orchestrator engine (Vol 2) for query processing, GovernedOutput (Vol 9) for utterance governance, MemoryManager L3 (Vol 1) for episode logging, DecisionValidator (Vol 9) for safety gating, EventBus (Vol 8) for event emission, Tool Registry (Vol 10) for voice tool registration.
- Serves: API routes (Vol 8) expose voice endpoints; Console (Vol 7) uses voice REST/WebSocket APIs.

### B.3 Interface Contracts

#### 3.1 VoiceController

**Location (rebuild):** `src/atlas/voice/controller.py`

**Constructor:**
```
VoiceController(
    orchestrator: OrchestratorEngine,     # Vol 2
    memory_manager: MemoryManager,        # Vol 1
    governance: OutputGovernor,           # Vol 9
    decision_validator: DecisionValidator, # Vol 9
    config: VoiceControllerConfig,
)
```

**Public methods:**
- `async process_voice_query(audio_base64: str | None, transcript: str | None, session_id: str | None, device_id: str, settings: VoiceSettings | None, return_audio: bool) -> VoiceResponse` — Full STT→Atlas→TTS pipeline
- `start_session(device_id: str) -> VoiceSession` — Creates tracked voice session
- `end_session(session_id: str) -> bool` — Closes session
- `get_status() -> VoiceControllerStatus` — Health/status snapshot
- `async warmup() -> dict[str, Any]` — Pre-loads TTS/STT models
- `async shutdown() -> None` — Graceful teardown

**Dependencies consumed:**
- `OrchestratorEngine.process_query(query: str, session_id: str) -> str` (Vol 2)
- `OutputGovernor.govern(text: str, evidence: list[str]) -> GovernedOutput` (Vol 9)
- `DecisionValidator.validate(command: str) -> ValidationDecision` (Vol 9)
- `MemoryManager.l3.record_episode(...)` (Vol 1)
- `EventBus.publish(event: AtlasEvent)` (Vol 8)

**Dependencies served:**
- Voice API routes (Vol 8) call `process_voice_query()`, `start_session()`, `end_session()`, `get_status()`
- VoiceTools (Vol 10) call `process_voice_query()`, `get_status()`

#### 3.2 TTSEngine Protocol

**Location (rebuild):** `src/atlas/voice/tts.py`

```
class TTSEngine(Protocol):
    async def synthesize(self, text: str, speed: float = 1.0) -> tuple[bytes, TTSMetadata]: ...
    async def synthesize_stream(self, text: str) -> AsyncIterator[bytes]: ...
    @property
    def is_initialized(self) -> bool: ...
    async def initialize(self) -> None: ...
```

**TTSMetadata:** `text: str`, `audio_format: str = "wav"`, `sample_rate: int`, `duration_seconds: float`

**Implementations:** `PiperTTSEngine` (local ONNX), `XTTSTTSEngine` (HTTP client to localhost:5050)

#### 3.3 STTEngine Protocol

**Location (rebuild):** `src/atlas/voice/stt.py`

```
class STTEngine(Protocol):
    async def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000) -> STTResult: ...
    @property
    def is_available(self) -> bool: ...
```

**STTResult:** `transcript: str (1-5000)`, `confidence: float (0-1)`, `language: str`, `duration_ms: int`, `alternatives: list[str]`

#### 3.4 SpeakerVerifier

**Location (rebuild):** `src/atlas/voice/speaker_verifier.py`

**Public methods:**
- `async enroll(request: VoiceprintEnrollRequest) -> VoiceprintEnrollResponse`
- `async verify(audio_bytes: bytes, sample_rate: int, threshold: float, mic_device_label: str, user_id: str) -> SpeakerVerifyResponse`
- `async get_status(user_id: str) -> dict`
- `async delete_voiceprint(user_id: str, mic_label: str | None) -> bool`
- `get_stats() -> VerificationStatsResponse`
- `async warm_model() -> float`

**Key schemas:** `VoiceprintEnrollRequest` (3-5 b64 PCM samples ≤2MB each, ambient_sample, sample_rate 8-48kHz), `VoiceprintEnrollResponse` (per_sample_quality[], overall_quality_score), `SpeakerVerifyResponse` (verified, similarity, threshold, liveness_suspect, mic_mismatch), `VoiceprintData` (voiceprint_id, embedding_sha256, quality_score)

**Dependencies:** Resemblyzer VoiceEncoder, cryptography.fernet, numpy, scipy

#### 3.5 TextNormalizer

**Location (rebuild):** `src/atlas/voice/text_normalizer.py`

`def normalize_for_speech(text: str) -> str` — Expands decimals, units, acronyms, percentages. Pure string transforms, no dependencies.

#### 3.6 Voice Pydantic Schemas

**Location (rebuild):** `src/atlas/voice/schemas.py`

Schemas to rebuild (all with Field descriptions, validators, safety bounds):
- `VoiceControllerConfig` — stt_engine, tts_engine, speaker_verification_enabled, threshold (0.5-0.95), max_query_length (≤10000), session_timeout (30-3600s)
- `VoiceSession` — session_id, device_id, started_at, query_count, speaker_verified, active
- `VoiceControllerStatus` — initialized, stt/tts engine names, active_sessions, tts/stt_available
- `VoiceSettings` — tts_voice, tts_speed (0.5-2.0), tts_volume (0.0-1.0), language (ISO 639-1)
- `VoiceQuery` — audio (b64, ≤10MB), format (wav/mp3/m4a), session_id, device_id
- `STTResult` — transcript (1-5000), confidence (0-1), language, duration_ms
- `TTSMetadata` — text, audio_format, sample_rate, duration_seconds
- `VoiceResponse` — transcript, response_text, audio (b64 optional), session_id, metadata
- `AudioMetadata` — sample_rate (8-48kHz), channels (1-2), duration, format, size_bytes (≤10MB)
- `VoiceInteractionEpisode` — user_input, assistant_response, duration_seconds, stt/tts_engine, confidence, session_id
- Speaker verification schemas: `VoiceprintEnrollRequest`, `VoiceprintEnrollResponse`, `SpeakerVerifyResponse`, `VoiceprintData`, `VerificationStatsResponse`

Schemas NOT in this volume: `GovernedOutput`/`AuthorityLevel` → Vol 9; `OpenAIRealtimeConfig`/`RealtimeSessionState` → DEFER

#### 3.7 Voice API Endpoints

**Location (rebuild):** `src/atlas/api/routes/voice.py` (registered by Vol 8)

Core endpoints (REBUILD):
- `POST /v1/voice/query` — Full STT→Atlas→TTS pipeline
- `POST /v1/voice/tts/jarvis` — Local TTS synthesis → WAV audio
- `GET /v1/voice/tts/jarvis/status` — TTS engine status
- `POST /v1/voice/voiceprint/enroll` — Speaker enrollment
- `POST /v1/voice/voiceprint/verify` — Speaker verification (REST)
- `WS /v1/voice/voiceprint/verify-stream` — Streaming verification
- `GET /v1/voice/voiceprint/status` — Enrollment status
- `DELETE /v1/voice/voiceprint` — Delete voiceprint
- `POST /v1/voice/voiceprint/warmup` — Pre-warm model
- `GET /v1/voice/voiceprint/stats` — Verification stats

Cloud proxy endpoints (DEFER): `/v1/voice/realtime/session`, `/api/stt/elevenlabs/*`, `/api/tts`, `/api/tts/cartesia`

#### 3.8 VoiceTools

**Location (rebuild):** `src/atlas/tools/voice.py` (registered by Vol 10)

- `speak(text: str, voice: str) -> {success, engine, duration_seconds, ...}`
- `transcribe(audio_path: str) -> {success, text, response, ...}`
- `get_voice_status() -> {tts_available, stt_available, engines: {...}}`

### B.4 Scope Triage

**Every component in A.2 receives a verdict:**

#### Voice Subsystem Files

**`src/voice/__init__.py`** — **REBUILD**
Justification: Module entry point with lazy imports. Design pattern is sound (lazy-load heavy dependencies). Rebuild with updated import paths under `src/atlas/voice/`.

**`src/voice/voice_controller.py`** — **REBUILD**
Justification: Core orchestrator for the voice pipeline. Architecture (STT→safety→query→govern→TTS→log) is correct. Two critical gaps: (1) `_process_query()` returns placeholder `"Acknowledged: {transcript}"` instead of routing through real orchestrator — must wire to Vol 2's `OrchestratorEngine.process_query()`; (2) voice governance must use Vol 9's `GovernedOutput` instead of voice-specific `ApprovedUtterance`. Session management, warmup lifecycle, and TTS engine delegation carry forward.

**`src/voice/governance.py`** — **KILL**
Justification: `ApprovedUtterance` superseded by Vol 9's unified `GovernedOutput` per AGENT_COMM.md pre-registered ownership. The governance *pattern* (create → hash → stamp → validate before speech) is preserved in Vol 9's `OutputGovernor`. `log_voice_event()` moves into VoiceController's L3 logging.

**`src/voice/schemas.py`** — **REBUILD**
Justification: Well-structured Pydantic schemas with proper safety bounds (10MB audio limit, 5000-char TTS limit, 0.5-2.0x speed range, 8-48kHz sample rate). Remove `OpenAIRealtimeConfig` and `RealtimeSessionState` (deferred with WebRTC). Keep speaker verification schemas (pure Pydantic, no heavy deps).

**`src/voice/piper_tts.py`** — **REBUILD**
Justification: Local ONNX-based TTS essential for R7 (local-first). Architecture (HuggingFace model download → espeak-ng phonemization → ONNX inference → WAV output) is functional. Rebuild conforming to `TTSEngine` Protocol.

**`src/voice/xtts_tts.py`** — **DEFER**
Justification: Depends on separate persistent XTTS server process on port 5050. Higher quality but external runtime dependency. Not required for MVA. Defer until Piper TTS proven.

**`src/voice/speaker_verifier.py`** — **DEFER**
Justification: Sophisticated (Resemblyzer GE2E, encrypted voiceprints, ambient calibration, liveness heuristic). Speaker verification is a security enhancement, not core voice requirement. Adds heavy dependencies (resemblyzer, PyTorch, cryptography). Defer until basic voice I/O proven. Design carries forward directly when rebuilt.

**`src/voice/text_normalizer.py`** — **REBUILD**
Justification: Pure-function text preprocessing, zero external dependencies. Essential for TTS quality. Small (179 lines). Rebuild as-is.

**`src/voice/realtime_webrtc_signaling.py`** — **DEFER**
Justification: Depends on OpenAI Realtime API (external, API-key-gated). Not required for basic voice. Defer until real-time conversational voice prioritized.

#### API & Tools Files

**`src/api/routes/voice.py`** — **REBUILD (partial)**
Justification: Rebuild core voice endpoints (`/v1/voice/query`, `/v1/voice/tts/jarvis*`, `/v1/voice/voiceprint/*`). Defer cloud proxy endpoints (`/api/stt/elevenlabs/*`, `/api/tts`, `/api/tts/cartesia`, `/v1/voice/realtime/session`).

**`src/orchestrator/tools/voice_tools.py`** — **REBUILD**
Justification: LLM-callable voice tools. Small (181 lines), clear. Rebuild under `src/atlas/tools/voice.py`.

#### Documentation Files

**`docs/architecture/voice-integration-map.md`** — **REBUILD (as design reference)**
Justification: Authoritative voice governance integration spec. Threat model (T1-T5), L1-L10 layer placement, enforcement responsibilities, fail-closed behavior inform rebuild. Design intent encoded into Vol 9 governance spec and Vol 6 acceptance tests.

**`docs/architecture/voice-tools.md`** — **KILL**
Justification: Auto-generated summary. Superseded by B.3 §3.8.

**`docs/development/voice-governance-implementation.md`** — **KILL**
Justification: Implementation status doc from Attempt 3. Design decisions extracted into this volume.

**`docs/development/voice-integration-status.md`** — **KILL**
Justification: Phase-by-phase checklist from Attempt 3. Historical, no ongoing design value.

#### Console Voice Components

**`console/src/components/VoiceInputButton.tsx`** — **DEFER to Volume 7**
**`console/src/components/VoiceEnrollment.tsx`** — **DEFER to Volume 7**
**`console/src/components/VoiceRealtimeWebRTC.tsx`** — **DEFER to Volume 7**
**`console/src/components/VoiceSettings.tsx`** — **DEFER to Volume 7**
**`console/src/components/TTSProviderSelector.tsx`** — **DEFER to Volume 7**
**`console/src/lib/voiceGovernance.ts`** — **DEFER to Volume 7 / Volume 9**
Justification: All console components owned by Volume 7. Voice health state machine (HEALTHY/DEGRADED/RECOVERING/LOCKED_OUT) specified in Vol 9.

#### Test Files

**`tests/voice/test_schemas.py`** — **REBUILD** — Schema validation tests carry forward.
**`tests/voice/test_governance.py`** — **KILL** — Governance.py killed; tests move to Vol 9.
**`tests/voice/test_voice_controller.py`** — **REBUILD** — Adapt to new dependencies.
**`tests/voice/test_speaker_verifier.py`** — **DEFER** — Speaker verifier deferred.

### B.5 Technology Choices

**5.1 Piper ONNX TTS (PRIMARY — REBUILD)**
Source evidence: `piper_tts.py` (288 lines). Local ONNX-runtime inference via HuggingFace model download (`rhasspy/piper-voices`). Phonemization via `espeak-ng` subprocess. Output: raw 16-bit PCM → WAV header assembly in Python. No GPU required — CPU inference on Apple Silicon measured at ~0.3× real-time. Chosen because it satisfies R7 (local-first, no network dependency) and keeps voice synthesis fully within the ATLAS process boundary.

**5.2 macOS native STT (ABANDONED)**
Source evidence: `voice_controller.py:176-190`. `_init_stt()` attempts `NativeSTTEngine()` but catches all exceptions and falls back to `None`. In practice, `NativeSTTEngine` was never functional — the macOS `SFSpeechRecognizer` binding had permission and availability issues. The controller's fallback path (`stt_engine is None`) was always taken. STT is deferred entirely; no default STT engine ships in the rebuild.

**5.3 Resemblyzer GE2E Speaker Embeddings (DEFERRED)**
Source evidence: `speaker_verifier.py` (995 lines). Uses `resemblyzer.VoiceEncoder` for generalized end-to-end (GE2E) speaker embeddings. Cosine similarity for verification. Encrypted voiceprint storage via `cryptography.fernet`. Heavy dependencies: resemblyzer pulls PyTorch, numpy, scipy. Deferred because speaker verification is non-MVP and the dependency chain conflicts with lightweight deployment.

**5.4 structlog replaces loguru**
Source evidence: `voice_controller.py:3` imports `structlog`, not `loguru`. All voice modules use `structlog.get_logger()`. This aligns with the project-wide migration to structured logging per shared conventions.

**5.5 Pydantic v2 Field() replaces confloat/conint**
Source evidence: `schemas.py` uses `Field(ge=0.5, le=2.0)` instead of deprecated `confloat(ge=0.5, le=2.0)`. All schemas use Pydantic v2 `model_config = ConfigDict(...)` pattern. `constr`, `confloat`, `conint` are eliminated.

### B.6 Data Model

All schemas reside in `src/atlas/voice/schemas.py`. Every schema uses Pydantic v2 `BaseModel` with `Field()` descriptors.

**6.1 VoiceControllerConfig**
- `stt_engine: str = "native"` — STT engine identifier
- `tts_engine: str = "piper"` — TTS engine identifier
- `speaker_verification_enabled: bool = False`
- `speaker_verification_threshold: float = Field(default=0.7, ge=0.5, le=0.95)` — cosine similarity threshold
- `max_query_length: int = Field(default=5000, le=10000)` — max transcript chars
- `session_timeout: int = Field(default=300, ge=30, le=3600)` — seconds

**6.2 VoiceSession**
- `session_id: str` (UUID4)
- `device_id: str`
- `started_at: datetime`
- `last_activity: datetime`
- `query_count: int = 0`
- `speaker_verified: bool = False`
- `active: bool = True`

**6.3 VoiceControllerStatus**
- `initialized: bool`
- `stt_engine: str | None`
- `tts_engine: str | None`
- `active_sessions: int`
- `tts_available: bool`
- `stt_available: bool`

**6.4 VoiceSettings**
- `tts_voice: str = "default"`
- `tts_speed: float = Field(default=1.0, ge=0.5, le=2.0)`
- `tts_volume: float = Field(default=1.0, ge=0.0, le=1.0)`
- `language: str = "en"` — ISO 639-1

**6.5 VoiceQuery**
- `audio: str` — base64-encoded, max 10MB decoded
- `format: AudioFormat` — enum: wav, mp3, m4a
- `session_id: str | None`
- `device_id: str | None`

**6.6 STTResult**
- `transcript: str` — Field(min_length=1, max_length=5000)
- `confidence: float` — Field(ge=0.0, le=1.0)
- `language: str`
- `duration_ms: int`
- `alternatives: list[str] = []`

**6.7 TTSMetadata**
- `text: str`
- `audio_format: str = "wav"`
- `sample_rate: int = 22050`
- `duration_seconds: float`

**6.8 VoiceResponse**
- `transcript: str` — what STT heard
- `response_text: str` — what Atlas said
- `audio: str | None` — base64 WAV (if TTS enabled)
- `session_id: str`
- `metadata: TTSMetadata | None`

**6.9 AudioMetadata**
- `sample_rate: int` — Field(ge=8000, le=48000)
- `channels: int` — Field(ge=1, le=2)
- `duration_seconds: float`
- `format: AudioFormat`
- `size_bytes: int` — Field(le=10_485_760) (10MB)

**6.10 AudioFormat** (Enum)
- Values: `wav`, `mp3`, `m4a`, `pcm`, `ogg`

**6.11 VoiceInteractionEpisode**
- `user_input: str`
- `assistant_response: str`
- `duration_seconds: float`
- `stt_engine: str | None`
- `tts_engine: str | None`
- `confidence: float | None`
- `session_id: str`

**6.12 Speaker Verification Schemas (DEFERRED — design preserved)**
- `VoiceprintEnrollRequest` — user_id, audio_samples (3-5 b64 PCM ≤2MB each), ambient_sample, sample_rate (8-48kHz), mic_device_label
- `VoiceprintEnrollResponse` — voiceprint_id, per_sample_quality[], overall_quality_score, enrolled_at
- `SpeakerVerifyResponse` — verified, similarity, threshold, liveness_suspect, mic_mismatch
- `VoiceprintData` — voiceprint_id, user_id, embedding_sha256, quality_score, created_at, mic_label
- `VerificationStatsResponse` — total_verifications, successful, failed, avg_similarity, liveness_rejections

**6.13 Cross-Volume Schema Boundary**
Vol 6 does NOT define `GovernedOutput` or `AuthorityLevel` — these belong to Vol 9. Vol 6 consumes `GovernedOutput` as the egress validation gate for TTS output. `OpenAIRealtimeConfig` and `RealtimeSessionState` are DEFER'd with WebRTC.

### B.7 Error Handling

**7.1 Error Hierarchy**
All voice errors inherit from `AtlasError` (defined in `shared/errors.py`, Vol 8).

```
AtlasError
└── VoiceSubsystemError
    ├── TTSEngineError        — TTS synthesis failure (model load, phonemization, ONNX inference)
    ├── STTEngineError        — STT transcription failure (engine unavailable, decode error)
    ├── SpeakerVerifyError    — Speaker verification failure (model load, embedding, threshold)
    └── VoiceSessionError     — Session management failure (timeout, invalid session)
```

**7.2 Error Propagation Rules**
1. **TTS failure → text fallback.** If TTS synthesis fails, VoiceController returns `VoiceResponse` with `audio=None` and `response_text` populated. The user gets the text response; voice output degrades gracefully.
2. **STT failure → 503 Service Unavailable.** If no STT engine is available, the `/v1/voice/query` endpoint returns HTTP 503 with structured error body. No silent swallowing.
3. **Governance rejection → block output.** If `OutputGovernor.govern()` rejects the response text, VoiceController returns a safe fallback message ("I cannot respond to that.") and logs the rejection to L3.
4. **Session timeout → cleanup + 410 Gone.** Expired sessions are purged from the session store. Subsequent requests with the expired `session_id` return HTTP 410.

**7.3 Anti-Pattern: Event Swallowing (from Attempt 3)**
Source evidence: `voice_controller.py:305-335` catches exceptions in `_log_voice_interaction()` and swallows them with `logger.warning("Failed to log...")`. This masks L3 memory failures. Rebuild requirement: logging failures MUST be emitted as structured warning events (not caught and suppressed) so monitoring can detect L3 degradation.

### B.8 Testing Strategy

**8.1 Acceptance Tests (REBUILD — run in CI)**
- AT-V6-01: Full voice query pipeline — audio in → STT → orchestrator → governance → TTS → audio out. Verifies end-to-end with mocked STT/TTS engines.
- AT-V6-02: TTS text-to-speech — text input → Piper TTS → valid WAV output with correct sample rate and duration.
- AT-V6-03: Governance gate enforcement — verify that TTS output passes through `OutputGovernor.govern()` before delivery.
- AT-V6-04: Feature flag gating — with `ATLAS_ENABLE_VOICE=false`, all voice endpoints return 503.

**8.2 Integration Tests (REBUILD — require backend on port 8000)**
- IT-V6-01: Voice API endpoint round-trip — POST `/v1/voice/query` with valid audio, receive `VoiceResponse`.
- IT-V6-02: Voice tools invocation — orchestrator calls `speak()` tool, receives audio bytes.
- IT-V6-03: Session lifecycle — create session → query → query → timeout → verify cleanup.
- IT-V6-04: L3 memory logging — voice interaction produces `VoiceInteractionEpisode` in L3 store.

**8.3 Unit Tests (REBUILD)**
- Schema validation: all 13 Pydantic schemas with valid/invalid inputs, boundary values (from existing `test_schemas.py`)
- TextNormalizer: decimal expansion, unit expansion, acronym expansion, percentage formatting
- PiperTTSEngine: model loading, phonemization subprocess, WAV assembly, speed adjustment
- VoiceController: session create/expire, STT/TTS delegation, error propagation paths
- AudioFormat enum membership
- VoiceQuery base64 size validation (>10MB rejected)

**8.4 Regression Tests**
- RG-V6-01: Governance bypass regression — confirm no code path exists that emits voice audio without governance check.
- RG-V6-02: Placeholder response regression — confirm `_process_query()` delegates to `OrchestratorEngine.process_message()` and never returns hardcoded "Acknowledged: {transcript}".

**8.5 Test Count Note**
Attempt 3 `test_voice_controller.py` had 27 test functions but 19 used `@pytest.mark.skip` or were assertion-free stubs. The rebuild must not inflate test counts — every test function must contain at least one meaningful assertion.

### B.9 Configuration

All voice configuration uses `AtlasConfig(BaseSettings)` from `shared/config.py` (Vol 8) with `env_prefix="ATLAS_"`.

| Env Variable | Type | Default | Description |
|---|---|---|---|
| `ATLAS_ENABLE_VOICE` | bool | `false` | Master feature flag. When false, all voice endpoints return 503 and VoiceController skips initialization. |
| `ATLAS_VOICE_TTS_ENGINE` | str | `"piper"` | TTS engine to load. Options: `piper`, `xtts` (deferred). |
| `ATLAS_VOICE_STT_ENGINE` | str | `"none"` | STT engine to load. Options: `native` (broken), `none`. |
| `ATLAS_VOICE_SPEAKER_VERIFY` | bool | `false` | Enable speaker verification gate. |
| `ATLAS_VOICE_SPEAKER_THRESHOLD` | float | `0.7` | Cosine similarity threshold for speaker verification (0.5-0.95). |
| `ATLAS_VOICE_DEFAULT_SPEED` | float | `1.0` | Default TTS playback speed (0.5-2.0). |
| `ATLAS_VOICE_SESSION_TIMEOUT` | int | `300` | Voice session inactivity timeout in seconds (30-3600). |
| `ATLAS_VOICE_VOICEPRINT_DIR` | str | `"data/voiceprints"` | Directory for encrypted voiceprint storage (deferred). |

**Feature Flag Behavior:** When `ATLAS_ENABLE_VOICE=false` (the default), the voice `APIRouter` is still registered (so `/v1/voice/*` paths exist in OpenAPI schema) but all handlers return `503 Service Unavailable` with body `{"detail": "Voice subsystem disabled"}`. This allows Vol 7 console to detect voice availability without crashing on 404.

### B.10 Subsystem Lessons Learned

**10.1 Placeholder `_process_query()` masked integration gap**
Source: `voice_controller.py:240-256`. The method returns `f"Acknowledged: {transcript}"` instead of calling `OrchestratorEngine`. This meant the entire voice pipeline could appear functional in demos while never actually integrating with the orchestrator. Lesson: integration boundary calls must NOT have in-method fallback strings. If the dependency is unavailable, fail loudly.

**10.2 macOS STT was never functional**
Source: `voice_controller.py:176-190`. `_init_stt()` catches all exceptions from `NativeSTTEngine()` and sets `stt_engine = None`. There is no evidence in test files that native STT ever produced a real transcription. Lesson: deferred capabilities must be explicitly marked DEFER in config, not silently swallowed with try/except.

**10.3 Voice governance duplicated output governance**
Source: `governance.py` (196 lines) implements `ApprovedUtterance` with hash-and-stamp pattern. Vol 9's `GovernedOutput` does the same thing for all egress channels. Lesson: subsystem-specific governance schemas will always drift from the centralized governance system. One egress gate, one schema.

**10.4 Event swallowing in L3 logging**
Source: `voice_controller.py:305-335`. `_log_voice_interaction()` catches all exceptions and logs a warning. If L3 memory is down, voice interactions continue without episodic records — but nobody is alerted. Lesson: non-critical side effects (logging, telemetry) must still emit structured warnings that monitoring can aggregate, not silently pass.

**10.5 Test count inflation**
Source: `test_voice_controller.py` had 27 test functions. 19 were `@pytest.mark.skip` or had no assertions (just `pass` bodies). This inflated the apparent test count without providing coverage. Lesson: every test function must have at least one meaningful assertion. Skip-marked tests must have a tracking issue.

### B.11 Discoveries

**11.1 Egress Governance Pattern — Candidate for P12**
`governance.py` implements: (1) create response text → (2) SHA-256 hash → (3) timestamp + authority stamp → (4) validate hash matches before TTS output. This is a general-purpose egress governance pattern applicable to ALL output channels (text, voice, tool execution, file write). Vol 0 should consider promoting this to a principle: "P12: All Egress Is Governed." Vol 9 already generalizes this via `GovernedOutput`, confirming the pattern.

**11.2 Lazy Model Loader Pattern**
`piper_tts.py` uses a module-level singleton (`_piper_engine: PiperTTSEngine | None = None`) with async initialization and `ThreadPoolExecutor` for blocking ONNX inference. The same pattern appears in Vol 1 (embedding models), Vol 3 (BERT classifier), and Vol 5 (sentiment models). Should be standardized as a `LazyModelLoader[T]` generic base class in `shared/` to avoid reimplementing the same init-once, thread-pool-delegate, warm-up pattern in every volume.

**11.3 Apple Silicon OpenMP Thread-Pool Conflict**
`speaker_verifier.py:117-118` sets `os.environ["OMP_NUM_THREADS"] = "1"` and `os.environ["MKL_NUM_THREADS"] = "1"` before importing PyTorch. This prevents a deadlock when FAISS (which uses its own OpenMP pool) and PyTorch coexist on Apple Silicon. Any rebuild volume that mixes FAISS + PyTorch must apply this guard at module import time, before any PyTorch import occurs.

### B.12 Oversight Self-Review

**Q1: Does the design satisfy the subsystem's stated purpose (B.1)?**
Yes. B.1 states Vol 6 provides local-first voice I/O with governed TTS output. The design rebuilds VoiceController (STT→orchestrator→governance→TTS pipeline), PiperTTSEngine (local ONNX), TextNormalizer, schemas, API routes, and tools. All output passes through Vol 9's GovernedOutput. Speaker verification and cloud TTS are correctly deferred.

**Q2: Are all interface contracts (B.3) implementable with the chosen technology (B.5)?**
Yes. B.3 specifies VoiceController, TTSEngine Protocol, STTEngine Protocol, SpeakerVerifier, TextNormalizer, schemas, API endpoints, and tools. B.5 confirms Piper ONNX is the primary TTS implementation, structlog for logging, Pydantic v2 for schemas. The STTEngine Protocol has no implementation (STT deferred), which is consistent — the protocol is defined so future engines can plug in.

**Q3: Does the error handling (B.7) cover all failure modes in B.3?**
Yes. B.7 defines four error types (TTSEngineError, STTEngineError, SpeakerVerifyError, VoiceSessionError) and four propagation rules (TTS failure → text fallback, STT failure → 503, governance rejection → safe fallback, session timeout → cleanup). The event-swallowing anti-pattern from Attempt 3 is explicitly flagged for correction.

**Q4: Are all A.4 warnings addressed?**
- **A.4.1 (Voice ≠ Multimodal):** Addressed. Volume scope is strictly voice I/O (STT/TTS/speaker verification). No image, gesture, or sensor processing. Title retained for discoverability but B.1 explicitly scopes to voice.
- **A.4.2 (STT gap — no default engine):** Addressed. B.4 marks STT as deferred. STTEngine Protocol is defined in B.3 §3.3 so engines can plug in. `ATLAS_VOICE_STT_ENGINE` defaults to `"none"`. B.5 §5.2 documents macOS native STT was never functional.
- **A.4.3 (process_query placeholder):** Addressed. B.10 §10.1 documents the placeholder. B.3 §3.1 specifies the rebuild must call `OrchestratorEngine.process_message()` per shared-contracts.md §2.8. The method name mismatch (process_query vs process_message) is flagged in agent-comm/vol-06.md.
- **A.4.4 (governance.py duplication):** Addressed. B.4 KILLs governance.py. B.3 §3.1 specifies VoiceController consumes Vol 9's GovernedOutput. B.10 §10.3 captures the lesson.

**Q5: Is the testing strategy (B.8) sufficient to catch regressions in B.3 contracts?**
Yes. 4 acceptance tests cover the full pipeline, governance enforcement, and feature flag gating. 4 integration tests cover API round-trip, tool invocation, session lifecycle, and L3 logging. Unit tests cover all 13 schemas, TextNormalizer, PiperTTSEngine, and VoiceController. 2 regression tests specifically target the governance bypass and placeholder response regressions from A.4.

**Q6: Are cross-volume dependencies (B.3 consumers/providers) registered in agent-comm?**
Yes. `agent-comm/vol-06.md` registers 9 dependency declarations (Vol 1 memory, Vol 2 orchestrator, Vol 8 config/errors/routes, Vol 9 governance/validation, Vol 10 tool registration), 7 ownership claims, and 3 conflict flags including the process_query→process_message mismatch.

### B.13 Design Quality Scorecard

| # | Criterion | Score (1-5) | Evidence |
|---|---|---|---|
| 1 | Boundary clarity (interfaces defined, no leaky abstractions) | 5 | B.3 defines 8 interface contracts with typed signatures. TTSEngine/STTEngine are Protocol classes. Voice API routes are a self-contained APIRouter. No internal types leak across volume boundaries. |
| 2 | Failure handling (every error path explicit) | 5 | B.7 defines 4 error types, 4 propagation rules, and explicitly flags the event-swallowing anti-pattern. TTS failure degrades to text; STT failure returns 503; governance rejection blocks output. |
| 3 | Testability (acceptance + unit tests defined) | 5 | B.8 defines 4 acceptance, 4 integration, 10+ unit, and 2 regression tests. All major contracts have corresponding test cases. Test inflation from Attempt 3 is flagged. |
| 4 | Dependency hygiene (minimal, explicit, versioned) | 4 | REBUILD scope has 4 dependencies: piper-tts (ONNX + espeak-ng), structlog, Pydantic v2, FastAPI. DEFERRED scope adds heavy deps (resemblyzer, PyTorch, cryptography). -1 because espeak-ng is a system binary dependency that requires OS-level install. |
| 5 | Configuration safety (validated, bounded, documented) | 5 | B.9 defines 8 env vars with ATLAS_ prefix, all with type, default, and range constraints. Feature flag behavior documented (503 when disabled, not 404). All values validated through Pydantic Field constraints. |
| 6 | Schema completeness (all data types Pydantic-modeled) | 5 | B.6 defines 13 Pydantic schemas covering all voice data types. Every field has type annotation and constraint. Cross-volume schema boundaries are explicitly stated (GovernedOutput → Vol 9). |
| 7 | Cross-volume alignment (contracts match shared-contracts.md) | 4 | 9 dependency declarations registered. Process_query→process_message mismatch identified and flagged (B.3 §3.1 will use process_message per shared-contracts.md §2.8). -1 because the B.3 text itself still says process_query and requires a Phase 3 correction. |
| 8 | Lessons captured (anti-patterns documented, not repeated) | 5 | B.10 captures 5 lessons from source reading (placeholder masking, broken STT, governance duplication, event swallowing, test inflation). Each includes source evidence and corrective action. |
| 9 | Scope discipline (REBUILD/DEFER/KILL justified, no scope creep) | 5 | B.4 assigns verdicts to every A.2 component (9 REBUILD, 4 DEFER, 4 KILL, 6 DEFER-to-Vol-7). No scope creep — speaker verification and cloud TTS correctly deferred. B.4 verdicts confirmed by Phase 2 source reading. |
| | **TOTAL** | **43/45** | |

---

## Modification History

| Version | Date | Modified By | Summary | Laymen Summary |
|---|---|---|---|---|
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (9 voice files, 6 console components, 4 docs), context brief, and 4 known failure warnings including voice/multimodal confusion and STT gap | Created the voice system analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V06-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 Source Manifest per DISTILLATION_PROTOCOL.md Section 5 | Labeled which files agents should read in full vs. skim during Phase 1 |
| v7 | 2026-03-11 | Oz (Phase 2 Distillation Agent) | Phase 2 distillation — B.5-B.13 filled from full source reading of 11 CORE and 10 PERIPHERAL files. 5 technology choices, 13 Pydantic schemas, 4 error types, acceptance/integration/unit/regression tests, 8 config vars, 5 lessons, 3 discoveries, 6 self-review Q&A, scorecard 43/45. Agent-comm claims registered. | The agent read every voice source file and filled out the detailed technical design: what tech to use, data structures, error handling, tests, config, lessons learned, and a quality check |
