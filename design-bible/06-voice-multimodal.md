# ATLAS Design Bible — Volume 6: Voice & Multimodal

| Field | Value |
|---|---|
| **Doc ID** | `DB-V06-001` |
| **Name** | Volume 6: Voice & Multimodal |
| **Purpose** | Design specification for natural voice interaction — TTS, STT, speaker verification, and governed utterance output |
| **Owner** | Design Bible / Volume 6 |
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
| v1 | 2026-03-10 | Oz | Initial scaffold — Part A pre-loaded with source manifest (9 voice files, 6 console components, 4 docs), context brief, and 4 known failure warnings including voice/multimodal confusion and STT gap | Created the voice system analysis document with file lists and known problems for the analysis agent to investigate |
| v2 | 2026-03-10 | Oz | Added documentation standard header/footer per PROJECT_CONVENTIONS.md Section 9 | Added tracking metadata so we know who changed what and when |
| v3 | 2026-03-10 | Oz | Added Doc ID field (`DB-V06-001`) per PROJECT_CONVENTIONS.md Section 9.4 | Added unique document number for machine searching |
| v4 | 2026-03-10 | Oz | Added CORE/PERIPHERAL classification to A.2 Source Manifest per DISTILLATION_PROTOCOL.md Section 5 | Labeled which files agents should read in full vs. skim during Phase 1 |
