#!/usr/bin/env python3
"""
Prompt Pool Builder & Manager CLI
Utility to query, sample, mutate, filter, and export batches of video & image prompts
from across the curated prompt pools.

Usage:
  python prompt_pool_builder.py list
  python prompt_pool_builder.py sample --pool midjourney --count 5
  python prompt_pool_builder.py sample --pool veo --format json
  python prompt_pool_builder.py search "slime"
  python prompt_pool_builder.py export --pool editorial --output batch.json --limit 10
"""

import sys
import json
import argparse
import random
from pathlib import Path

POOLS_DIR = Path(__file__).resolve().parent.parent / "pools"

POOL_MAP = {
    "midjourney": POOLS_DIR / "midjourney_v3_cooked_100_prompts.json",
    "editorial": POOLS_DIR / "hermes_editorial_4k_campaign_plan.jsonl",
    "krea": POOLS_DIR / "krea_video_prompts_archive.json",
    "scary_vee": POOLS_DIR / "scary_vee_video_prompts.json",
    "web_batch": POOLS_DIR / "web_batch_prompts.json",
    "families": POOLS_DIR / "web_batch_new_families.json",
    "riffs": POOLS_DIR / "mj_riffs.json",
}

def load_pool(pool_name: str) -> list:
    path = POOL_MAP.get(pool_name.lower())
    if not path or not path.exists():
        raise FileNotFoundError(f"Pool '{pool_name}' not found. Available: {list(POOL_MAP.keys())}")

    if path.suffix == ".jsonl":
        items = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    items.append(json.loads(line))
        return items
    elif path.suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                # Try finding list under keys like "prompts", "sessions", etc.
                for k in ["prompts", "sessions", "items", "data"]:
                    if k in data and isinstance(data[k], list):
                        return data[k]
                return [data]
    return []

def extract_prompt_text(item) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        for k in ["prompt", "motion_prompt", "exact_prompt", "description", "text"]:
            if k in item and isinstance(item[k], str):
                return item[k]
        if "prompts" in item and isinstance(item["prompts"], list) and item["prompts"]:
            first = item["prompts"][0]
            if isinstance(first, dict):
                return first.get("prompt", str(first))
            return str(first)
    return str(item)

def cmd_list(args):
    print("\n--- Available Prompt Pools in ai-video-prompt-engine ---")
    for name, path in POOL_MAP.items():
        if path.exists():
            try:
                items = load_pool(name)
                print(f"  • {name:<12} : {len(items):>4} items ({path.name})")
            except Exception as e:
                print(f"  • {name:<12} : Error loading ({e})")
        else:
            print(f"  • {name:<12} : [Missing: {path.name}]")
    print()

def cmd_sample(args):
    items = load_pool(args.pool)
    count = min(args.count, len(items))
    sampled = random.sample(items, count) if count < len(items) else items

    if args.format == "json":
        print(json.dumps(sampled, indent=2))
    else:
        print(f"\n--- Random Sample of {count} from pool '{args.pool}' ---\n")
        for i, item in enumerate(sampled, 1):
            txt = extract_prompt_text(item)
            meta = f" [ID: {item.get('id', i)}]" if isinstance(item, dict) and 'id' in item else ""
            print(f"[{i}]{meta}\n{txt}\n")

def cmd_search(args):
    query = args.query.lower()
    print(f"\nSearching for '{query}' across all pools...\n")
    matches = 0
    for name in POOL_MAP.keys():
        try:
            items = load_pool(name)
            for i, it in enumerate(items, 1):
                txt = extract_prompt_text(it)
                if query in txt.lower():
                    matches += 1
                    print(f"[{name.upper()} #{i}] {txt[:160]}...")
        except Exception:
            continue
    print(f"\nFound {matches} matches.\n")

def cmd_export(args):
    items = load_pool(args.pool)
    if args.limit:
        items = items[:args.limit]
    out_path = Path(args.output)
    if out_path.suffix == ".txt":
        with open(out_path, "w", encoding="utf-8") as f:
            for it in items:
                f.write(extract_prompt_text(it).strip() + "\n")
    else:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2)
    print(f"Exported {len(items)} items from '{args.pool}' to {out_path}")

def main():
    parser = argparse.ArgumentParser(description="Prompt Pool Builder & Query Tool")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List all pools and stats")

    p_sample = sub.add_parser("sample", help="Sample prompts from a pool")
    p_sample.add_argument("--pool", default="midjourney", choices=list(POOL_MAP.keys()))
    p_sample.add_argument("--count", type=int, default=3)
    p_sample.add_argument("--format", default="text", choices=["text", "json"])

    p_search = sub.add_parser("search", help="Search text across all pools")
    p_search.add_argument("query", type=str)

    p_export = sub.add_parser("export", help="Export a pool to file")
    p_export.add_argument("--pool", required=True, choices=list(POOL_MAP.keys()))
    p_export.add_argument("--output", required=True, help="Destination filename (.json or .txt)")
    p_export.add_argument("--limit", type=int, default=None)

    args = parser.parse_args()
    if args.cmd == "list":
        cmd_list(args)
    elif args.cmd == "sample":
        cmd_sample(args)
    elif args.cmd == "search":
        cmd_search(args)
    elif args.cmd == "export":
        cmd_export(args)

if __name__ == "__main__":
    main()
