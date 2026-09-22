# COLLABORATOR HANDOFF: AI VIDEO & PROMPT GENERATION ENGINE

**Target Audience:** Creative Collaborators, AI Video Directors, Computational Artists  
**Core Purpose:** Generating high-impact AI video content using structured prompt pools, programmatic prompt mutation machines, and multi-model video generation pipelines (Google Veo, Fal Kling, Seedance, Runway, Hedra).

---

## 1. Executive Summary & Creative DNA

This repository bridges **structured prompt generation data** with **high-velocity AI video execution**. Rather than prompting models with vague adjectives ("cinematic, hyper-detailed, masterpiece"), the system is built on:

1. **The 4-Layer Physical Ontology (L0–L3):**
   - **L0 Environment:** Mundane, specific real-world space with social use and tangible lighting.
   - **L1 Configuration:** Exact physical staging of structural bodies, subjects, and objects in tension.
   - **L2 Material Event:** Exactly **one** contained physical or kinetic impossibility (melting, folding, dripping, levitating).
   - **L3 Optical Receipt:** Camera distance, lens focal length, lighting bounce, and photographic finish.
2. **Seed Prompt Banks & Mutation Machines:** An extensive library of curated seed prompts that can be algorithmically mutated against lexicons of body parts, materials, distortions, animals, and pop-cultural residues.
3. **Multi-Model Video Pipeline:** Direct integrations with Google Veo 3.1 / 2.0 (for vertical reels, native speech, and physical motion) and Fal Kling 1.6 / 3.0 Pro (for cinematic camera paths and fluid dynamics).

---

## 2. Tour of the Prompt Pools (`pools/`)

The repository includes several distinct, high-quality prompt datasets ready for video production:

| Pool File | Count | Focus & Description |
|---|---|---|
| `pools/scary_vee_video_prompts.json` | 5 Episodes | **Vertical 9:16 reels** with motion prompts, voiceover scripts, camera moves, and lighting notes. |
| `pools/midjourney_v3_cooked_100_prompts.json` | 100 Prompts | Curated sculptural neo-pop & kinetic character prompts with structural tags (`Anatomical Mutation -> Material Tension -> Gallery Light`). |
| `pools/hermes_editorial_4k_campaign_plan.jsonl` | 100 Prompts | Production-ready L0–L3 editorial prompts featuring discovered real-world situations, material tension, and unglamorous crops. |
| `pools/krea_video_prompts_archive.json` | 7 Workflows | Multi-model video prompts extracted across Kling 2.6/3.0, Seedance 2.0, Runway Gen-4.5, and Wan 2.1. |
| `pools/web_batch_prompts.json` | 80 Prompts | Kinetic sculpture and physical object prompts blending classical art references with modern materials. |
| `pools/web_batch_new_families.json` | 14 Families | Taxonomical grouping of themes, visual palettes, and artistic lineages. |
| `pools/web_batch_semantic_swaps.json` | Dictionary | Structured synonym map for combinatorial replacement of subjects, armatures, and materials. |

---

## 3. The Prompt Generation Engines (`generators/`)

### A. `prompt_machine.html` (Interactive Web App)
- **Zero-dependency, single-file HTML/JS app.**
- Double-click to open in Chrome/Brave/Safari.
- Features: Seed bank viewer, mutation sliders (mutation rate, structure depth, chaos), preset selectors, one-click prompt copying, and batch export.

### B. `prompt_machine.py` (CLI Mutation Engine)
- Python port of the mutation engine.
- Takes Alex's core voice corpus and mutates against lexicons (`colors`, `beings`, `animals`, `distortions`, `materials`, `actions`, `environments`, `photo`, `style`).
- Run `python generators/prompt_machine.py 10` to immediately generate 10 new prompts in terminal.

### C. `prompt_pool_builder.py` (Pool Query & Slice Tool)
- Command-line utility to query, sample, search, and export slices from across the prompt pools.
- Examples:
  - `python generators/prompt_pool_builder.py list`
  - `python generators/prompt_pool_builder.py sample --pool midjourney --count 5`
  - `python generators/prompt_pool_builder.py search "subway"`
  - `python generators/prompt_pool_builder.py export --pool scary_vee --output batch.json`

---

## 4. Video Generation & Animation Pipelines (`pipelines/`)

### A. Google Veo Generator (`pipelines/veo_video_generator.py`)
- Drives Google Veo 3.1 (`veo-3.1-generate-preview`) and Veo 2.0.
- Supports both **Text-to-Video** and **Image-to-Video** (using an initial character still as frame 0).
- Aspect ratios: `9:16` (vertical mobile), `16:9` (widescreen), `1:1` (square).
- Durations: 4s, 5s, 8s.

### B. Fal Kling Generator (`pipelines/fal_kling_video.py`)
- Drives Kling 1.6 Pro / Kling 3.0 via Fal AI.
- Automatically uploads local starting images to Fal S3, triggers generation, polls the job, and downloads the finalized MP4.

### C. Character Lip-Sync Pipeline (`pipelines/fal_character_lipsync.py`)
- **Hedra Character-2:** Input 1 Character Still + 1 Voiceover Audio file (`.wav`/`.mp3`) -> Fully articulated talking video.
- **LatentSync:** Input 1 Existing Video + 1 Voiceover Audio file -> Warps facial mouth movements in the video to match audio.

### D. Master Batch Runner (`pipelines/batch_video_runner.py`)
- Iterates over any prompt pool and generates video clips into an output folder.
- Supports `--model dry-run` to preview and validate prompt syntax without burning API credits.
- Automatically outputs a `receipt_<timestamp>.json` logging every prompt, model response, and output file path.

---

## 5. Recommended Production Workflow

```text
[Step 1: Ideation & Mutation]
  prompt_machine.html  OR  prompt_machine.py  OR  pools/*.json
            │
            ▼
[Step 2: Pool Slicing & Validation]
  prompt_pool_builder.py export --pool scary_vee --output my_run.json
  batch_video_runner.py --pool my_run --model dry-run
            │
            ▼
[Step 3: Keyframe Stills (Optional)]
  Generate initial high-res character still (Gemini / Midjourney / Krea)
            │
            ▼
[Step 4: AI Video Motion Generation]
  veo_video_generator.py  OR  fal_kling_video.py  OR  batch_video_runner.py
            │
            ▼
[Step 5: Voiceover & Lip Sync (Optional)]
  fal_character_lipsync.py (Hedra / LatentSync)
            │
            ▼
[Step 6: Final Reel Assembly]
  Subtitles, caption burns, sound design, and export.
```

---

## 6. Setup & Getting Started

1. Clone or copy the `ai-video-prompt-engine` folder to your workspace.
2. Install requirements: `pip install -r requirements.txt`
3. Configure your API keys in `.env` (copy from `.env.example`).
4. Test everything in 5 seconds with `./examples/run_demo.sh`.
