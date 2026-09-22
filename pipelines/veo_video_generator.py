#!/usr/bin/env python3
"""
Google Veo Video Generator (Veo 3.1 & Veo 2.0)
Generates AI video clips from text prompts or starting image keyframes.

Usage:
  # Text-to-Video
  python veo_video_generator.py --prompt "A cybernetic entity surfing through a neon transit tunnel, 4k cinematic motion" --output tunnel.mp4

  # Image-to-Video
  python veo_video_generator.py --image keyframe.png --prompt "The creature begins talking passionately, eyes darting, mouth moving" --aspect-ratio 9:16 --duration 5 --output out.mp4
"""

import os
import sys
import time
import argparse
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def get_api_key():
    key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        env_file = Path(".env")
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.strip().split("=", 1)
                    if k.strip() in ("GOOGLE_API_KEY", "GEMINI_API_KEY"):
                        return v.strip().strip("'\"")
    return key

def generate_veo_video(prompt: str, image_path: Path = None, model: str = "veo-3.1-generate-preview",
                        aspect_ratio: str = "9:16", duration_seconds: int = 5, output_path: Path = None):
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("[!] Error: 'google-genai' library not installed. Run: pip install google-genai")
        sys.exit(1)

    api_key = get_api_key()
    if not api_key:
        print("[!] Error: No GOOGLE_API_KEY or GEMINI_API_KEY found in environment or .env file.")
        print("    Set it in .env or run: export GOOGLE_API_KEY='your-key'")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    print(f"[*] Initializing Veo generation...")
    print(f"    Model: {model}")
    print(f"    Aspect Ratio: {aspect_ratio}")
    print(f"    Duration: {duration_seconds}s")
    print(f"    Prompt: {prompt[:120]}...")

    image_arg = None
    if image_path:
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Input image not found: {image_path}")
        print(f"[*] Attaching starting image: {image_path}")
        with open(image_path, "rb") as f:
            img_bytes = f.read()
        mime_type = "image/png" if image_path.suffix.lower() == ".png" else "image/jpeg"
        image_arg = types.Image(image_bytes=img_bytes, mime_type=mime_type)

    config = types.GenerateVideosConfig(
        aspect_ratio=aspect_ratio,
        duration_seconds=duration_seconds,
        number_of_videos=1,
    )

    print("[*] Submitting video generation operation...")
    kwargs = {"model": model, "prompt": prompt, "config": config}
    if image_arg:
        kwargs["image"] = image_arg

    operation = client.models.generate_videos(**kwargs)
    print(f"[*] Operation started: {operation.name}. Waiting for render...")

    start_time = time.time()
    while not operation.done:
        elapsed = int(time.time() - start_time)
        print(f"    Rendering in progress... ({elapsed}s elapsed)")
        time.sleep(10)
        operation = client.operations.get(operation)

    print("[✓] Operation finished!")
    if hasattr(operation.response, "rai_media_filtered_reasons") and operation.response.rai_media_filtered_reasons:
        print(f"[!] Warning: RAI Filter triggered: {operation.response.rai_media_filtered_reasons}")

    if operation.response and operation.response.generated_videos:
        vid_item = operation.response.generated_videos[0]
        file_uri = vid_item.video.uri
        if not output_path:
            output_path = Path(f"veo_output_{int(time.time())}.mp4")
        else:
            output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"[*] Downloading MP4 from Google Storage ({file_uri})...")
        client.files.download(file=file_uri, path=str(output_path))
        size_bytes = output_path.stat().st_size
        print(f"[✓] Successfully saved video to: {output_path} ({size_bytes:,} bytes)")
        return str(output_path)
    else:
        print("[!] No video generated in response.")
        return None

def main():
    parser = argparse.ArgumentParser(description="Google Veo 3.1 & 2.0 Video Generator")
    parser.add_argument("--prompt", required=True, help="Video prompt description")
    parser.add_argument("--image", default=None, help="Optional starting frame image path")
    parser.add_argument("--model", default="veo-3.1-generate-preview",
                        choices=["veo-3.1-generate-preview", "veo-3.1-fast-generate-preview", "veo-2.0-generate-001"])
    parser.add_argument("--aspect-ratio", default="9:16", choices=["9:16", "16:9", "1:1"])
    parser.add_argument("--duration", type=int, default=5, choices=[4, 5, 8])
    parser.add_argument("--output", default=None, help="Output MP4 file path")

    args = parser.parse_args()
    generate_veo_video(
        prompt=args.prompt,
        image_path=args.image,
        model=args.model,
        aspect_ratio=args.aspect_ratio,
        duration_seconds=args.duration,
        output_path=args.output
    )

if __name__ == "__main__":
    main()
