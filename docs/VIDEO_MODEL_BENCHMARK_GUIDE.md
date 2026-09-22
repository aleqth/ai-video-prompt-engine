# AI Video Models & Prompting Benchmark Guide

This guide compares prompting behaviors and strengths across the primary video generation backends supported in this engine.

---

## 1. Google Veo (Veo 3.1 & Veo 2.0)

- **Best for:** Natural character speech, complex multi-action choreography, environmental physics, and vertical 9:16 reels.
- **Key Capabilities:**
  - **Native Starting Frame Conditioning:** Exceptional consistency when passed an initial portrait or character still.
  - **Facial Articulation:** Mouth, lips, jaw, and brow move naturally to speech cadence without needing a separate lip-syncing pass.
  - **Synchronized Audio & Ambience:** When prompted with dialogue and sound cues, Veo 3.1 generates matching Foley, ambient acoustics, and creature voices.
- **Prompting Pattern:**
  ```text
  Cinematic vertical video close-up of [Character/Subject] actively speaking and shouting directly into camera.
  [Facial/Mouth action: mouth opens wide, lips articulate words, eyes blink and express intensity].
  [Secondary physical motion: slime drips, fur rustles, wind whips hair].
  [Camera movement: slow deliberate push-in, lock eye contact].
  [Audio cues: character shouts "LINE", ambient rain on metal roof, humming fluorescent bulbs].
  ```

---

## 2. Fal Kling Video (Kling 1.6 Pro & Kling 3.0)

- **Best for:** Cinematic performance art, fluid dynamics, sculptural elegance, slow camera tracks, and 16:9 widescreen or 9:16 vertical motion.
- **Key Capabilities:**
  - **High Temporal Stability:** Resists warping and flickering across 5s and 10s durations.
  - **Complex Camera Control:** Excels at crane shots, orbital pans, and tracking shots through architectural environments.
- **Prompting Pattern:**
  ```text
  Slow deliberate performance art movement, [Subject] tilts [Object] as [Material/Liquid] gently spills onto [Ground],
  camera slowly tracks forward through [Environment], subtle fabric fluttering in the wind, 4k cinematic photorealism.
  ```

---

## 3. Seedance 2.0 / Fast

- **Best for:** Material breakdowns, anime combat dynamics, metamorphic transformations, and rapid mascot/object deformation.
- **Key Capabilities:**
  - Fast execution speed.
  - Handles extreme non-human anatomy, melting rubber, dissolving geometry, and explosive energy effects without crashing or rejecting prompt physics.
- **Prompting Pattern:**
  ```text
  The silhouette reads like a corrupted mascot relic laughing, melting fingers and rubber surface breaking apart,
  high-velocity combat dynamics, neon shockwave particle FX, erratic kinetic twitch.
  ```

---

## 4. Runway Gen-4.5

- **Best for:** Subtle human and metamorphic emotional shifts, photorealistic lens flares, and theatrical narrative blocking.
- **Key Capabilities:**
  - Nuanced emotional transitions (e.g. moving from neutral to laughter to tears across 4–6 seconds).
  - High fidelity in hair, skin pores, and soft-focus backgrounds.

---

## 5. Facial Animation & Audio Lip-Sync (Hedra & LatentSync)

When you already have a finalized audio voiceover track (`.wav`) and want frame-accurate lip-syncing:
- **Hedra Character-2 (`fal-ai/hedra/character-2`):**
  - Input: 1 Character Still Image + 1 Audio File.
  - Output: Fully animated talking head with head tilts, natural blinks, and synced mouth.
- **LatentSync (`fal-ai/latentsync`):**
  - Input: 1 Existing Video File + 1 Audio File.
  - Output: Replaces or warps the mouth movements in the video to match the new audio track while preserving all original body and camera motion.
