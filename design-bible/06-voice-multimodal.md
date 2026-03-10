# ATLAS Design Bible — Volume 6: Voice & Multimodal

| Field | Value |
|---|---|
| **Doc ID** | `DB-V06-001` |
| **Name** | Volume 6: Voice & Multimodal |
| **Purpose** | Design specification for natural voice interaction — TTS, STT, speaker verification, and governed utterance output |
| **Owner** | Design Bible / Volume 6 |
| **Status** | `phase-1-complete` |
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
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (9 voice files, 6 console components, 4 docs), context brief, and 4 known failure warnings including voice/multimodal confusion and STT gap | Created the voice system analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V06-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 Source Manifest per DISTILLATION_PROTOCOL.md Section 5 | Labeled which files agents should read in full vs. skim during Phase 1 |
| v5 | 2026-03-10 | Distillation Agent V6 | Phase 1: Filled B.1-B.4. B.1 defines voice subsystem (TTS, STT, VoiceController, governance integration). B.2 has 9-component architecture with canonical data flow. B.3 has 8 interface contracts (VoiceController, TTSEngine, STTEngine, SpeakerVerifier, TextNormalizer, VoiceSchemas, VoiceRoutes, VoiceTools). B.4 triages all files (5 REBUILD, 4 DEFER, 4 KILL plus console components deferred to Vol 7). Registered 7 ownership claims, 6 dependency declarations, 2 conflict acknowledgements in agent-comm/vol-06.md. | The voice agent analyzed all voice files, kept 5 essential ones for the rebuild, deferred speaker verification and cloud engines, and documented what it needs from other systems |
