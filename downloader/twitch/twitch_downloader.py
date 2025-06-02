import os
import subprocess
from datetime import datetime
from urllib.parse import urlparse
from db import add_clip_if_new, mark_clip_downloaded, mark_clip_failed
from config import TWITCH_CLIP_ROOT

def extract_streamer_from_url(url: str) -> str:
    """
    Extract streamer/channel name from the Twitch clip URL.
    Example URL: https://www.twitch.tv/caedrel/clip/ClipName
    Returns: 'caedrel'
    """
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")
    if len(path_parts) < 2:
        raise ValueError(f"Invalid Twitch clip URL: {url}")
    # path_parts example: ['caedrel', 'clip', 'ClipName']
    streamer = path_parts[0]
    return streamer

def extract_clip_slug_from_url(url: str) -> str:
    """
    Extract clip slug (clip name) from URL.
    """
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")
    # Clip slug usually the last part
    slug = path_parts[-1]
    return slug

def download_twitch_clip(clip_url: str) -> str:
    print(f"[INFO] Starting download for: {clip_url}")
    try:
        streamer = extract_streamer_from_url(clip_url)
        clip_slug = extract_clip_slug_from_url(clip_url)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return ""

    # Date folder: today's date (UTC)
    date_str = datetime.utcnow().strftime("%Y-%m-%d")

    # Construct directory path: /clips/twitch/{streamer}/{YYYY-MM-DD}/
    output_dir = os.path.join(TWITCH_CLIP_ROOT, streamer, date_str)
    os.makedirs(output_dir, exist_ok=True)

    # Output file path
    output_path = os.path.join(output_dir, f"{clip_slug}.mp4")

    # Check if clip was already downloaded successfully
    if not add_clip_if_new(clip_slug, clip_url):
        print("[INFO] Clip already downloaded. Skipping.")
        return ""

    print(f"[INFO] Output path: {output_path}")

    # Prepare Streamlink command
    command = [
        "streamlink",
        clip_url,
        "best",
        "--output",
        output_path,
    ]
    print(f"[INFO] Running command: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            error_msg = result.stderr.strip()
            print(f"[ERROR] Streamlink failed: {error_msg}")
            mark_clip_failed(clip_slug, error_msg)
            return ""
        # Mark successful download
        mark_clip_downloaded(clip_slug, output_path)
        print("[INFO] Download complete.")
        return output_path
    except FileNotFoundError:
        error_msg = "streamlink command not found. Please install streamlink."
        print(f"[ERROR] {error_msg}")
        mark_clip_failed(clip_slug, error_msg)
        return ""
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Unexpected error: {error_msg}")
        mark_clip_failed(clip_slug, error_msg)
        return ""
