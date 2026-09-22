#!/usr/bin/env python3
"""
Fal Character Lip-Sync & Face Animation Pipeline
Uses Fal AI (Hedra Character-2 and LatentSync / Sync-Lips) to animate
character stills or existing video clips with custom speech audio tracks.

Usage:
  # Image + Audio -> Talking Character Video (Hedra Character-2)
  python fal_character_lipsync.py --image character.png --audio speech.wav --model hedra --output synced.mp4

  # Existing Video + Audio -> Re-synced Video (LatentSync)
  python fal_character_lipsync.py --video silent_clip.mp4 --audio speech.wav --model latentsync --output final_synced.mp4
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

def run_lipsync(image_path: Path = None, video_path: Path = None, audio_path: Path = None,
                model: str = "hedra", aspect_ratio: str = "9:16", output_path: Path = None):
    try:
        import fal_client
        import requests
    except ImportError:
        print("[!] Error: 'fal-client' or 'requests' not installed. Run: pip install fal-client requests")
        sys.exit(1)

    fal_key = get_fal_key()
    if not fal_key:
        print("[!] Error: No FAL_KEY found in environment or .env file.")
        sys.exit(1)
    os.environ["FAL_KEY"] = fal_key

    if not audio_path or not Path(audio_path).exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print(f"[*] Uploading audio asset: {audio_path}...")
    audio_url = fal_client.upload_file(str(audio_path))
    print(f"[✓] Audio URL: {audio_url}")

    if model == "hedra":
        if not image_path or not Path(image_path).exists():
            raise FileNotFoundError(f"Hedra requires --image parameter. Image not found: {image_path}")
        print(f"[*] Uploading image asset: {image_path}...")
        image_url = fal_client.upload_file(str(image_path))
        print(f"[✓] Image URL: {image_url}")

        endpoint = "fal-ai/hedra/character-2"
        arguments = {
            "image_url": image_url,
            "audio_url": audio_url,
            "aspect_ratio": aspect_ratio
        }
    elif model in ("latentsync", "sync-lips"):
        if not video_path or not Path(video_path).exists():
            raise FileNotFoundError(f"LatentSync requires --video parameter. Video not found: {video_path}")
        print(f"[*] Uploading video asset: {video_path}...")
        video_url = fal_client.upload_file(str(video_path))
        print(f"[✓] Video URL: {video_url}")

        endpoint = "fal-ai/latentsync" if model == "latentsync" else "fal-ai/sync-lips"
        arguments = {
            "video_url": video_url,
            "audio_url": audio_url
        }
    else:
        raise ValueError(f"Unknown model: {model}")

    print(f"[*] Submitting request to {endpoint}...")
    try:
        result = fal_client.subscribe(endpoint, arguments=arguments)
        print("[✓] Subscription completed!")
        video_url = result.get("video", {}).get("url")
        if not video_url:
            print("[!] No video URL in result:", result)
            return None

        if not output_path:
            output_path = Path(f"lipsync_output_{model}.mp4")
        else:
            output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"[*] Downloading lip-synced video from {video_url}...")
        r = requests.get(video_url)
        r.raise_for_status()
        output_path.write_bytes(r.content)
        print(f"[✓] Saved lip-synced video: {output_path} ({len(r.content):,} bytes)")
        return str(output_path)
    except Exception as e:
        print(f"[!] Error running {model}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Fal Character Lip-Sync & Face Animation Pipeline")
    parser.add_argument("--image", default=None, help="Character portrait image (for Hedra)")
    parser.add_argument("--video", default=None, help="Base video clip (for LatentSync)")
    parser.add_argument("--audio", required=True, help="Speech audio track (.wav or .mp3)")
    parser.add_argument("--model", default="hedra", choices=["hedra", "latentsync", "sync-lips"])
    parser.add_argument("--aspect-ratio", default="9:16", choices=["9:16", "16:9", "1:1"])
    parser.add_argument("--output", default=None, help="Output MP4 file path")

    args = parser.parse_args()
    run_lipsync(
        image_path=args.image,
        video_path=args.video,
        audio_path=args.audio,
        model=args.model,
        aspect_ratio=args.aspect_ratio,
        output_path=args.output
    )

if __name__ == "__main__":
    main()
