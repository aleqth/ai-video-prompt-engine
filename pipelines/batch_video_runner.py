#!/usr/bin/env python3
"""
Batch Video Runner
Orchestrates video generation runs against prompt pools using Veo, Kling, or Hedra.
Includes dry-run mode for previewing prompt sequences without burning API credits.

Usage:
  # Dry-run test (prints prompt batch sequence and validation)
  python batch_video_runner.py --pool scary_vee --model dry-run --limit 3

  # Render batch using Google Veo
  python batch_video_runner.py --pool scary_vee --model veo --limit 2 --output-dir ./renders/

  # Render batch using Fal Kling
  python batch_video_runner.py --pool krea --model kling --limit 3 --output-dir ./renders/
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path

# Add generators to path to import pool loader
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "generators"))
from prompt_pool_builder import load_pool, extract_prompt_text

def run_batch(pool_name: str, model: str, limit: int = None, output_dir: str = "./batch_output"):
    items = load_pool(pool_name)
    if limit:
        items = items[:limit]

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    receipt_file = out_path / f"receipt_{pool_name}_{int(time.time())}.json"

    print(f"\n========================================================")
    print(f"BATCH VIDEO RUNNER: Pool='{pool_name}' | Model='{model}'")
    print(f"Target items: {len(items)} | Output Dir: {out_path}")
    print(f"========================================================\n")

    results = []

    for i, item in enumerate(items, 1):
        prompt = extract_prompt_text(item)
        item_id = item.get("id", f"item_{i}") if isinstance(item, dict) else f"item_{i}"
        aspect = item.get("aspect_ratio", "9:16") if isinstance(item, dict) else "9:16"
        dur = item.get("duration_seconds", 5) if isinstance(item, dict) else 5

        print(f"[{i}/{len(items)}] Processing '{item_id}'...")
        print(f"    Prompt: {prompt[:100]}...")

        if model == "dry-run":
            print(f"    [DRY-RUN] Validated prompt ({len(prompt)} chars). Skipping render.")
            results.append({
                "index": i,
                "id": item_id,
                "prompt": prompt,
                "status": "dry_run_validated",
                "aspect_ratio": aspect,
                "duration": dur
            })
            continue

        clip_dest = out_path / f"{item_id}_{model}.mp4"

        if model == "veo":
            from veo_video_generator import generate_veo_video
            try:
                res = generate_veo_video(
                    prompt=prompt,
                    aspect_ratio=aspect,
                    duration_seconds=dur,
                    output_path=clip_dest
                )
                results.append({"index": i, "id": item_id, "status": "success" if res else "failed", "file": str(clip_dest)})
            except Exception as e:
                print(f"    [!] Error: {e}")
                results.append({"index": i, "id": item_id, "status": "error", "error": str(e)})

        elif model == "kling":
            from fal_kling_video import generate_kling_video
            try:
                res = generate_kling_video(
                    prompt=prompt,
                    aspect_ratio=aspect,
                    duration=str(dur),
                    output_path=clip_dest
                )
                results.append({"index": i, "id": item_id, "status": "success" if res else "failed", "file": str(clip_dest)})
            except Exception as e:
                print(f"    [!] Error: {e}")
                results.append({"index": i, "id": item_id, "status": "error", "error": str(e)})
        else:
            raise ValueError(f"Unsupported model: {model}")

    # Save receipt
    with open(receipt_file, "w", encoding="utf-8") as f:
        json.dump({
            "pool": pool_name,
            "model": model,
            "total_items": len(items),
            "timestamp": time.time(),
            "results": results
        }, f, indent=2)

    print(f"\n[✓] Batch complete! Receipts recorded to: {receipt_file}\n")

def main():
    parser = argparse.ArgumentParser(description="Batch Video Generation Runner")
    parser.add_argument("--pool", required=True, help="Name of prompt pool (e.g. scary_vee, krea, web_batch)")
    parser.add_argument("--model", default="dry-run", choices=["dry-run", "veo", "kling"])
    parser.add_argument("--limit", type=int, default=None, help="Max items to process")
    parser.add_argument("--output-dir", default="./batch_output", help="Directory for rendered MP4s and receipts")

    args = parser.parse_args()
    run_batch(pool_name=args.pool, model=args.model, limit=args.limit, output_dir=args.output_dir)

if __name__ == "__main__":
    main()
