# AI Prompt Engine: Words, Pools & Midjourney Archive

A production toolkit of structured prompt pools, lexical word banks, combinatoric generators, and the complete **Midjourney Cooked & Seed Bank Suite**.

Designed for AI video creators and computational artists who work with pools of prompts, word data, and automated generation queues.

---

## What’s In This Repository

### 1. `prompts/` — Ready-to-Use Prompt Pools (1,450+ Prompts)
Every prompt pool is provided as a clean `.txt` file (**1 prompt per line**—ready to copy-paste directly into Midjourney, ComfyUI, Kling, Runway, Pika, Sora, or batch automation spreadsheets), along with structured `.json` datasets:

* **`midjourney_100_cooked_presets.txt`**: 100 curated sculptural neo-pop & institutional gallery prompts formatted with Midjourney presets (`--ar 4:5 --v 6.1` / `--chaos 100 --stylize 650 --profile ...`).
* **`midjourney_100_cooked_clean.txt`**: The exact same 100 prompts stripped of all Midjourney flags—pure, evocative physical descriptions ready for **video models** (Kling, Veo, Runway, Luma, Sora).
* **`midjourney_seed_bank_archive_394.txt`**: 394 authentic, raw seed bank prompts extracted directly from Alex's generative archive.
* **`midjourney_v3_cooked_100.json`**: Structured JSON containing all 100 cooked prompts with tags, anatomical distortions, lighting profiles, and camera finishes.
* **`all_prompts_master_pool.txt`**: **1,456 unique prompts** compiled and deduplicated across all archives into a single master pool.
* **`editorial_4k_campaign_100.txt`**: 100 high-fashion L0–L3 editorial prompts with museum-grade lighting and camera receipts.
* **`krea_video_motion_prompts.txt`**: Dynamic video generation prompts designed for fluid camera motion and physical transformations.
* **`web_batch_surreal_sculptures.txt`**: 80 kinetic sculpture, pop-surrealist installation, and tactile art prompts.
* **`sonic_arcade_8bit_prompts.txt`**: 2,100+ cyber-retro arcade, pixel art, and digital nostalgia prompts.
* **`scary_vee_dialogue_and_scenes.txt`**: Scene prompts paired with voiceover dialogue scripts.

---

### 2. `words_and_lexicons/` — The Complete Word & Modifier Banks
The core vocabulary engine that generates high-tension, physical art prompts:

* **`LEXICON_DICTIONARY.md`**: Human-readable dictionary of all word categories, modifiers, and compositional formulas.
* **`lexicon_word_banks.json`**: Machine-readable JSON dictionary categorizing hundreds of words:
  * `[beings]`: *humanoid, pseudo-figure, mascot cadaver, hybrid sculpture, creature...*
  * `[distortions]`: *reversed elbows, lumbar twist 180°, wall-like torso, backward wrists, melting fingers...*
  * `[materials]`: *pale silicone, glossy fiberglass, wet-look lilac lacquer, inflatable vinyl, chrome-plated skin...*
  * `[colors]`: *candy-apple red, SpongeBob yellow, flesh-toned, matte black, Ronald McDonald stripe...*
  * `[objects]`: *dental rig, mechanical whisk, red scissors, audio harness, balloon dog mask...*
  * `[environments]`: *cavernous brutalist gallery, pristine white void studio, blank showroom...*
  * `[photo & lighting]`: *Gagosian soft diffuse, cool museum halogen spots, 35mm film, Sigmar Polke residue...*
  * `[motion_verbs]`: *subtle breathing pulse, horizontal glitch jitter, surface tension rupture, continuous 360 rotation...*
  * `[camera_movements]`: *slow cinematic dolly-in, low floor-level tilt-up, macro probe lens through cavity...*
* **`synonym_maps.json`**: Substitution trees for mutating prompts while keeping their physical charge.
* **`semantic_swaps.json`**: Thematic word swap clusters.
* **`visual_families.json`**: 14 distinct visual and aesthetic universes.

---

### 3. `generators/` — Tools for Generating & Mutating Prompts

* **`prompt_machine.html`**: Zero-dependency browser web app. Double-click to open in any browser:
  * Contains the full **394-prompt seed bank** built right in.
  * Interactive sliders for Mutation, Structure, Chaos, Novelty, and Fragmentation.
  * Version presets: `v1` (clean classic), `v2` (alex voice), `v3` (cooked), `v4` (chaos).
  * 1-click prompt mutation, randomize grammar, and instant clipboard copy.
* **`prompt_mutator.py`**: Zero-dependency Python CLI tool:
  * **Generate new prompts from word banks:**
    ```bash
    python generators/prompt_mutator.py generate -n 5 --video
    ```
  * **Sample random prompts from any pool:**
    ```bash
    python generators/prompt_mutator.py sample -p midjourney_clean -n 3
    python generators/prompt_mutator.py sample -p all -n 5
    ```
  * **Mutate an existing prompt using lexical synonyms:**
    ```bash
    python generators/prompt_mutator.py mutate "pale silicone humanoid with reversed elbows in gallery"
    ```
