#!/usr/bin/env python3
"""
Fal AI Kling Video Generator (Kling 1.6 Pro & Kling 3.0)
Generates high-fidelity AI video clips from text prompts or starting image keyframes.

Usage:
  # Image-to-Video
  python fal_kling_video.py --image still.png --prompt "Deliberate cinematic motion, figure tilts bowl, liquid spills" --output out.mp4

  # Text-to-Video
  python fal_kling_video.py --prompt "Arms dangling from a cloud at sunset, cinematic lighting, 4k" --aspect-ratio 16:9 --output out.mp4
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def get_fal_key():
    key = os.environ.get("FAL_KEY")
    if not key:
        env_file = Path(".env")
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.strip().split("=", 1)
                    if k.strip() == "FAL_KEY":
                        return v.strip().strip("'\"")
    return key

def generate_kling_video(prompt: str, image_path: Path = None, model_endpoint: str = "fal-ai/kling-video/v1.6/pro/image-to-video",
                         duration: str = "5", aspect_ratio: str = "9:16", output_path: Path = None):
    try:
        import fal_client
        import requests
    except ImportError:
        print("[!] Error: 'fal-client' or 'requests' not installed. Run: pip install fal-client requests")
        sys.exit(1)

    fal_key = get_fal_key()
    if not fal_key:
        print("[!] Error: No FAL_KEY found in environment or .env file.")
        print("    Set it in .env or run: export FAL_KEY='your-key'")
        sys.exit(1)

    os.environ["FAL_KEY"] = fal_key

    arguments = {
        "prompt": prompt,
        "duration": str(duration),
        "aspect_ratio": aspect_ratio
    }

    if image_path:
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Source image not found: {image_path}")
        print(f"[*] Uploading source image to Fal S3: {image_path}...")
        image_url = fal_client.upload_file(str(image_path))
        print(f"[✓] Uploaded image URL: {image_url}")
        arguments["image_url"] = image_url
    else:
        # Text-to-video endpoint
        if "image-to-video" in model_endpoint:
            model_endpoint = "fal-ai/kling-video/v1.6/pro/text-to-video"

    print(f"[*] Submitting request to Fal ({model_endpoint})...")
    print(f"    Prompt: {prompt[:120]}...")
    print(f"    Duration: {duration}s | Aspect Ratio: {aspect_ratio}")

    try:
        handler = fal_client.submit(model_endpoint, arguments=arguments)
        print(f"[*] Generation queued (Request ID: {handler.request_id}). Polling...")
        result = handler.get()
        print("[✓] Generation complete!")

        video_url = result.get("video", {}).get("url")
        if not video_url:
            print("[!] No video URL in result:", result)
            return None

        if not output_path:
            output_path = Path(f"kling_output_{handler.request_id[:8]}.mp4")
        else:
            output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"[*] Downloading generated MP4 from {video_url}...")
        r = requests.get(video_url)
        r.raise_for_status()
        output_path.write_bytes(r.content)
        print(f"[✓] Saved video locally: {output_path} ({len(r.content):,} bytes)")
        return str(output_path)
    except Exception as e:
        print(f"[!] Fal Kling error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Fal AI Kling Video Generator")
    parser.add_argument("--prompt", required=True, help="Video prompt description")
    parser.add_argument("--image", default=None, help="Optional source image path")
    parser.add_argument("--endpoint", default="fal-ai/kling-video/v1.6/pro/image-to-video")
    parser.add_argument("--duration", default="5", choices=["5", "10"])
    parser.add_argument("--aspect-ratio", default="9:16", choices=["9:16", "16:9", "1:1"])
    parser.add_argument("--output", default=None, help="Output MP4 file path")

    args = parser.parse_args()
    generate_kling_video(
        prompt=args.prompt,
        image_path=args.image,
        model_endpoint=args.endpoint,
        duration=args.duration,
        aspect_ratio=args.aspect_ratio,
        output_path=args.output
    )

if __name__ == "__main__":
    main()
