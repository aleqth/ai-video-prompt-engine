#!/usr/bin/env bash
# Quick Demo Script for ai-video-prompt-engine
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

echo "=== 1. Listing Available Prompt Pools ==="
python3 generators/prompt_pool_builder.py list

echo ""
echo "=== 2. Sampling 2 Prompts from Midjourney Cooked Suite ==="
python3 generators/prompt_pool_builder.py sample --pool midjourney --count 2

echo ""
echo "=== 3. Testing 5 Mutated Prompts from Python Mutation Machine ==="
python3 generators/prompt_machine.py 5

echo ""
echo "=== 4. Running Dry-Run Batch against Scary Vee Video Pool ==="
python3 pipelines/batch_video_runner.py --pool scary_vee --model dry-run --limit 2

echo ""
echo "[✓] Demo complete! Interactive UI available at: generators/prompt_machine.html"
