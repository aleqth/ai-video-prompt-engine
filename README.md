# AI Video Prompt Engine & Generation Lab

A modular production toolkit and dataset repository for generating, mutating, and executing high-velocity AI video content from pools of structured prompts and creative data.

Designed for AI video creators, directors, and collaborators working across **Google Veo 3.1**, **Fal Kling 1.6/3.0**, **Seedance 2.0**, **Runway Gen-4.5**, and **Hedra / LatentSync** audio-reactive lip sync.

---

## Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Keys
```bash
cp .env.example .env
# Edit .env and paste your GOOGLE_API_KEY and FAL_KEY
```

### 3. Run the Verification Demo
```bash
./examples/run_demo.sh
```

### 4. Launch the Interactive Prompt Machine
Open `generators/prompt_machine.html` in any web browser. It is a completely self-contained single-page application with zero runtime dependencies.

---

## Repository Map

```text
ai-video-prompt-engine/
├── HANDOFF.md                                # Comprehensive collaborator onboarding & pipeline guide
├── README.md                                 # This quickstart & reference sheet
├── .env.example                              # API key configuration template
├── requirements.txt                          # Python package dependencies
│
├── generators/                               # Prompt generation & mutation engines
│   ├── prompt_machine.html                   # Offline interactive browser app with visual controls
│   ├── prompt_machine.py                     # Python CLI prompt mutation machine
│   ├── prompt_pool_builder.py                # CLI tool to list, sample, filter, and export pools
│   ├── dada_object.py                        # L0-L3 physical ontology & prompt synthesizer
│   └── rules.py                              # Lexicon structures, token rules, and styles
│
├── pools/                                    # Curated prompt datasets & pools
│   ├── midjourney_v3_cooked_100_prompts.json # 100 structured sculptural/neo-pop prompts with anatomy tags
│   ├── midjourney_v3_cooked_100_prompts.txt  # Plain-text line-delimited prompt pool
│   ├── hermes_editorial_4k_campaign_plan.jsonl # 100 production-ready L0-L3 editorial prompts
│   ├── krea_video_prompts_archive.json       # Kling, Seedance, Runway, Wan prompt sessions
│   ├── scary_vee_video_prompts.json          # Multi-episode monster parody prompts & dialogue
│   ├── web_batch_prompts.json                # 82 kinetic sculpture & surreal animation prompts
│   ├── web_batch_new_families.json           # 14 thematic visual families
│   ├── web_batch_semantic_swaps.json         # Combinatorial substitution dictionary
│   └── mj_riffs.json                         # Visual variations and riffs
│
├── pipelines/                                # Video execution & post-production scripts
│   ├── veo_video_generator.py                # Google Veo 3.1 & Veo 2.0 video generator
│   ├── fal_kling_video.py                    # Fal AI Kling 1.6 / 3.0 Pro video animator
│   ├── fal_character_lipsync.py              # Hedra Character-2 & LatentSync lip-sync pipeline
│   └── batch_video_runner.py                 # Multi-model batch runner reading from prompt pools
│
├── docs/                                     # Creative guides, bibles & prompt frameworks
│   ├── SCARY_VEE_MULTIVERSE_BIBLE.md         # Series bible, vocal DNA & 9:16 vertical specs
│   ├── PROMPT_ARCHITECTURE_L0_L3.md          # 4-layer prompt theory (L0 World, L1 Subject, L2 Event, L3 Receipt)
│   └── VIDEO_MODEL_BENCHMARK_GUIDE.md        # Video model benchmark (Veo vs Kling vs Seedance vs Runway)
│
└── examples/
    └── run_demo.sh                           # 1-command verification script
```

---

## Core Workflows

### Query & Sample Prompt Pools
```bash
# List all prompt pools and count
python generators/prompt_pool_builder.py list

# Sample 3 random prompts from the Midjourney cooked suite
python generators/prompt_pool_builder.py sample --pool midjourney --count 3

# Search all pools for a keyword
python generators/prompt_pool_builder.py search "subway"

# Export a sliced batch to JSON
python generators/prompt_pool_builder.py export --pool scary_vee --output my_batch.json
```

### Generate Mutated Prompts via CLI
```bash
python generators/prompt_machine.py 10
```

### Generate Video via Google Veo 3.1
```bash
python pipelines/veo_video_generator.py \
  --prompt "A neon cyborg shouting passionately, 8k cinematic motion, mouth moving" \
  --aspect-ratio 9:16 \
  --duration 5 \
  --output ./renders/cyborg.mp4
```

### Animate Image via Fal Kling Pro
```bash
python pipelines/fal_kling_video.py \
  --image keyframe.png \
  --prompt "Deliberate performance art movement, slow camera push-in" \
  --output ./renders/kling_scene.mp4
```

### Lip-Sync Voice Audio onto Character Still
```bash
python pipelines/fal_character_lipsync.py \
  --image character.png \
  --audio voiceover.wav \
  --model hedra \
  --output ./renders/synced_character.mp4
```

### Run Batch Video Generation
```bash
# Dry-run validation (no API credits used)
python pipelines/batch_video_runner.py --pool scary_vee --model dry-run

# Render batch with Google Veo
python pipelines/batch_video_runner.py --pool scary_vee --model veo --limit 3 --output-dir ./renders/
```
