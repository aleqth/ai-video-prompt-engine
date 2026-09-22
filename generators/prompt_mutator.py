#!/usr/bin/env python3
"""
Prompt Mutator & Combinatoric Word Generator
Generates and mutates prompts using the structured lexicons, synonym maps, and seed pools.
Zero external dependencies (pure Python standard library).
"""

import sys
import json
import random
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WORDS_DIR = BASE_DIR / "words_and_lexicons"
PROMPTS_DIR = BASE_DIR / "prompts"

def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_combinatoric_prompt(lexicon, count=1, video_mode=False):
    prompts = []
    for _ in range(count):
        color = random.choice(lexicon.get("colors", ["chrome"]))
        mat = random.choice(lexicon.get("materials", ["glossy fiberglass"]))
        being = random.choice(lexicon.get("beings", ["humanoid"]))
        distortion = random.choice(lexicon.get("distortions", ["reversed elbows"]))
        obj = random.choice(lexicon.get("objects", ["dental rig"]))
        env = random.choice(lexicon.get("environments", ["in a white void gallery"]))
        photo = random.choice(lexicon.get("photo", ["Gagosian-style soft diffuse lighting"]))
        style = random.choice(lexicon.get("style", ["neo-pop energy"]))

        parts = [
            f"{mat} {being} in {color}",
            f"with {distortion}",
            f"fused with {obj}",
            env,
            photo,
            f"{style}"
        ]

        if video_mode:
            motion = random.choice(lexicon.get("motion_verbs", ["subtle breathing pulse"]))
            cam = random.choice(lexicon.get("camera_movements", ["slow cinematic dolly-in"]))
            parts.append(f"{cam}, {motion}")

        prompts.append(", ".join(parts))
    return prompts

def mutate_prompt(prompt_text, syn_map, swap_clusters, intensity=0.3):
    words = prompt_text.split()
    mutated = []
    for w in words:
        clean = w.strip(".,;:\"'").lower()
        if clean in syn_map and random.random() < intensity:
            repl = random.choice(syn_map[clean])
            mutated.append(repl)
        else:
            mutated.append(w)
    return " ".join(mutated)

def main():
    parser = argparse.ArgumentParser(description="Prompt Mutator & Combinatoric Generator")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # generate
    gen_p = subparsers.add_parser("generate", help="Generate novel prompts combinatorially from word banks")
    gen_p.add_argument("-n", "--count", type=int, default=5, help="Number of prompts to generate")
    gen_p.add_argument("--video", action="store_true", help="Append video camera movement and kinetic motion tags")
    gen_p.add_argument("-o", "--output", type=str, help="Save generated prompts to file (.txt or .json)")

    # mutate
    mut_p = subparsers.add_parser("mutate", help="Mutate a prompt or file of prompts using synonym maps")
    mut_p.add_argument("text", nargs="?", help="Prompt text to mutate")
    mut_p.add_argument("-f", "--file", type=str, help="Input prompt file to mutate (1 prompt per line)")
    mut_p.add_argument("-i", "--intensity", type=float, default=0.35, help="Mutation intensity 0.0 - 1.0")

    # sample
    sam_p = subparsers.add_parser("sample", help="Sample random prompts from an existing pool")
    sam_p.add_argument("-p", "--pool", type=str, default="midjourney_clean",
                        choices=["midjourney_clean", "midjourney_presets", "midjourney_seed", "editorial", "all"],
                        help="Which prompt pool to sample from")
    sam_p.add_argument("-n", "--count", type=int, default=3, help="Number of prompts to sample")

    args = parser.parse_args()

    lexicon = load_json(WORDS_DIR / "lexicon_word_banks.json")
    syn_map = load_json(WORDS_DIR / "synonym_maps.json")
    swaps = load_json(WORDS_DIR / "semantic_swaps.json")

    if args.command == "generate":
        prompts = generate_combinatoric_prompt(lexicon, count=args.count, video_mode=args.video)
        for i, p in enumerate(prompts, 1):
            print(f"[{i:02d}] {p}\n")
        if args.output:
            out_p = Path(args.output)
            if out_p.suffix == ".json":
                with open(out_p, "w", encoding="utf-8") as f:
                    json.dump([{"id": i+1, "prompt": p} for i, p in enumerate(prompts)], f, indent=2)
            else:
                with open(out_p, "w", encoding="utf-8") as f:
                    for p in prompts:
                        f.write(p + "\n")
            print(f"[OK] Saved {len(prompts)} prompts to {args.output}")

    elif args.command == "mutate":
        if args.text:
            mut = mutate_prompt(args.text, syn_map, swaps, intensity=args.intensity)
            print(f"Original: {args.text}")
            print(f"Mutated:  {mut}")
        elif args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]
            for l in lines:
                print(mutate_prompt(l, syn_map, swaps, intensity=args.intensity))

    elif args.command == "sample":
        filename_map = {
            "midjourney_clean": "midjourney_100_cooked_clean.txt",
            "midjourney_presets": "midjourney_100_cooked_presets.txt",
            "midjourney_seed": "midjourney_seed_bank_archive_394.txt",
            "editorial": "editorial_4k_campaign_100.txt",
            "all": "all_prompts_master_pool.txt"
        }
        target_file = PROMPTS_DIR / filename_map[args.pool]
        if not target_file.exists():
            print(f"File not found: {target_file}")
            return
        with open(target_file, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        sampled = random.sample(lines, min(args.count, len(lines)))
        for i, p in enumerate(sampled, 1):
            print(f"[{i:02d}] {p}\n")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
