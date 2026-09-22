# COLLABORATOR HANDOFF: WORDS, PROMPT POOLS & MIDJOURNEY ARCHIVE

**Target Audience:** Creative Collaborators, AI Video Creators, Computational Directors  
**Core Deliverables:** Complete structured prompt pools, lexical word banks, 1-per-line prompt files for batch workflows, and the entire Midjourney Cooked & Seed Bank Suite.

---

## 1. Quick Orientation: How This Repo Works

If you make AI-generated video or images using prompt pools, this repo gives you:
1. **The Exact Prompts:** Over 1,450+ curated, production-tested prompts in both structured `.json` and ready-to-copy `.txt` (1 prompt per line).
2. **The Midjourney Cooked Suite:** Both parameter-rich Midjourney versions (`--ar 4:5 --v 6.1 --chaos 100 --stylize 650`) and **clean plain-text versions** stripped of flags so they can be dropped straight into video models (Kling, Veo, Runway, Luma, Sora).
3. **The Raw Seed Bank:** 394 authentic seed prompts directly from Alex's generative archive.
4. **All the Words:** Complete dictionaries and word banks (`beings`, `materials`, `distortions`, `objects`, `environments`, `lighting`, `motion_verbs`, `camera_movements`) so you can combinatorially generate or mutate your own endless variations.
5. **Interactive UI & CLI:** Open `generators/prompt_machine.html` in your browser for the full interactive visual mutator with sliders and seed banks, or use `generators/prompt_mutator.py` in your terminal.

---

## 2. Directory Breakdown

```text
ai-video-prompt-engine/
├── HANDOFF.md                                # This collaborator guide
├── README.md                                 # Quickstart & file index
│
├── prompts/                                  # 1-per-line .txt files + .json datasets
│   ├── midjourney_100_cooked_presets.txt     # 100 Midjourney prompts with full parameters & preset flags
│   ├── midjourney_100_cooked_clean.txt       # 100 prompts CLEAN (pure visual text, zero flags—for video models)
│   ├── midjourney_seed_bank_archive_394.txt  # 394 raw seed bank prompts from Alex's archive
│   ├── midjourney_seed_bank_archive_394.json # 394 seed bank prompts in structured JSON
│   ├── midjourney_v3_cooked_100.json         # 100 cooked prompts with anatomy/material/lighting metadata
│   ├── all_prompts_master_pool.txt           # 1,456 unique prompts compiled across all archives
│   ├── editorial_4k_campaign_100.txt         # 100 high-fashion L0–L3 editorial prompts
│   ├── krea_video_motion_prompts.txt         # Kinetic video action and camera movement prompts
│   ├── scary_vee_dialogue_and_scenes.txt     # Character scene prompts with voiceover lines
│   ├── web_batch_surreal_sculptures.txt      # 80 pop-surrealist installation and kinetic art prompts
│   └── sonic_arcade_8bit_prompts.txt         # 2,100+ retro cyber arcade & pixel art prompts
│
├── words_and_lexicons/                       # Word banks, modifiers, and substitution trees
│   ├── LEXICON_DICTIONARY.md                 # Full markdown vocabulary guide & prompt formula
│   ├── lexicon_word_banks.json               # JSON dictionary of all word categories
│   ├── synonym_maps.json                     # Lexical replacement map for prompt mutation
│   ├── semantic_swaps.json                   # Thematic replacement clusters
│   └── visual_families.json                  # 14 aesthetic universe definitions
│
├── generators/                               # Tools for generating and mutating prompts
│   ├── prompt_machine.html                   # Interactive browser UI (500KB with 394 seeds built-in)
│   └── prompt_mutator.py                     # Zero-dependency Python CLI generator/mutator/sampler
│
└── docs/                                     # Creative background and frameworks
    ├── PROMPT_ARCHITECTURE_L0_L3.md          # 4-layer physical prompt framework
    ├── SCARY_VEE_MULTIVERSE_BIBLE.md         # Multiverse characters and vocal DNA
    └── VIDEO_MODEL_BENCHMARK_GUIDE.md        # Prompting behaviors across video models
```

---

## 3. How to Use the Midjourney Prompts

### A. For Midjourney & Still Generation
Use `prompts/midjourney_100_cooked_presets.txt`:
- These contain Alex's signature preset flags (`--ar 4:5 --v 6.1` and `--chaos 100 --stylize 650 --profile...`).
- Focuses on sculptural neo-pop figures, reversed anatomy, glossy fiberglass, and institutional gallery documentation.

### B. For AI Video Models (Kling, Veo, Sora, Runway, Luma)
Use `prompts/midjourney_100_cooked_clean.txt`:
- All Midjourney parameter flags (`--ar`, `--v`, `--chaos`) have been stripped away.
- What remains is the pure, evocative physical description—ideal as starting prompts for text-to-video or as descriptive prompts for image-to-video keyframe animation.

### C. The 394-Prompt Seed Bank
Use `prompts/midjourney_seed_bank_archive_394.txt`:
- Raw, authentic prompts from Alex's personal generative history.
- High variance, strange reaches, experimental pairings, and visual textures.

---

## 4. The Words & Lexicons: Building Endless Prompts

All words are categorized in `words_and_lexicons/lexicon_word_banks.json` and documented in `words_and_lexicons/LEXICON_DICTIONARY.md`:

- **Beings:** `humanoid`, `pseudo-figure`, `mascot cadaver`, `hybrid sculpture`, `robot body`...
- **Distortions:** `reversed elbows`, `head turned backwards 180°`, `arms on opposite sides`, `wall-like torso`...
- **Materials:** `pale silicone`, `glossy fiberglass`, `wet-look lilac lacquer`, `inflatable vinyl`, `chrome-plated skin`...
- **Colors:** `candy-apple red`, `flesh-toned`, `SpongeBob yellow`, `matte black`, `Ronald McDonald red/white stripe`...
- **Objects:** `dental rig`, `mechanical whisk`, `red scissors`, `balloon dog mask`, `chrome dental jaw`...
- **Environments:** `cavernous brutalist gallery`, `white void studio`, `cyclorama background`, `polished aggregate floors`...
- **Lighting & Documentation:** `Gagosian soft diffuse`, `cool museum halogen spots`, `35mm film`, `Sigmar Polke residue`...
- **Video Motion Verbs:** `subtle breathing pulse`, `horizontal glitch jitter`, `surface tension rupture`, `continuous 360 rotation`...
- **Camera Movements:** `slow cinematic dolly-in`, `low floor-level tilt-up`, `macro probe lens through cavity`...

---

## 5. Instant Tools

### 1. Browser Web App (`generators/prompt_machine.html`)
Double-click to open in any browser. It contains all 394 seeds loaded in memory, with mutation sliders, presets (`v1` classic, `v2` alex voice, `v3` cooked, `v4` chaos), and instant clipboard copy.

### 2. Python CLI (`generators/prompt_mutator.py`)
No `pip install` required—runs with Python standard library:
```bash
# Generate 5 fresh prompts with video camera movement & kinetic motion
python generators/prompt_mutator.py generate -n 5 --video

# Sample 3 random clean prompts from the Midjourney pool
python generators/prompt_mutator.py sample -p midjourney_clean -n 3

# Sample from the 1,456-prompt master pool
python generators/prompt_mutator.py sample -p all -n 5

# Mutate any prompt using lexical synonyms
python generators/prompt_mutator.py mutate "pale silicone humanoid with reversed elbows in gallery"
```
