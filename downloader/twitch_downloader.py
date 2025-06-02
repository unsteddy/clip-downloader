# twitch_downloader.py

import subprocess
import os
import re
import sys
from db.clip_dao import add_clip_if_new, mark_clip_downloaded, mark_clip_failed
from config import CLIP_STORAGE_DIR


def download_twitch_clip(clip_url: str) -> str:
    """
    Downloads a Twitch clip using streamlink and saves it locally.

    Args:
        clip_url (str): The URL of the Twitch clip.

    Returns:
        str: Path to the downloaded video file.
    """
    print(f"[INFO] Starting download for: {clip_url}")

    if not os.path.exists(CLIP_STORAGE_DIR):
        os.makedirs(CLIP_STORAGE_DIR)
        print(f"[INFO] Created output directory: {CLIP_STORAGE_DIR}")

    # Extract clip slug from URL
    match = re.search(r"clip/([\w]+)", clip_url)
    if not match:
        raise ValueError("Invalid Twitch clip URL.")
    clip_slug = match.group(1)

    # Check and insert into DB if new
    if not add_clip_if_new(clip_slug, clip_url):
        print(f"[INFO] Clip already processed: {clip_slug}")
        return ""

    output_path = os.path.join(CLIP_STORAGE_DIR, f"{clip_slug}.mp4")
    print(f"[INFO] Output path: {output_path}")

    # Use streamlink to download the best quality clip
    command = [
        "streamlink",
        clip_url,
        "best",
        "--output",
        output_path
    ]

    print(f"[INFO] Running command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[ERROR] Streamlink failed with error:\n{result.stderr}", file=sys.stderr)
        mark_clip_failed(clip_slug, result.stderr)
        raise RuntimeError(f"Failed to download clip: {result.stderr}")

    mark_clip_downloaded(clip_slug, output_path)
    print(f"[SUCCESS] Clip downloaded to: {output_path}")
    return output_path
