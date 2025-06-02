# downloader/fetch_top_clips.py

import sys
from downloader.twitch.twitch_api import fetch_all_top_clips
from downloader.twitch_downloader import download_twitch_clip


def main():
    period = "day"  # Default timeframe
    if len(sys.argv) > 1:
        period = sys.argv[1]  # e.g. 'day', 'week', 'month', 'all'

    print(f"[INFO] Fetching top clips for period: {period}")
    clips = fetch_all_top_clips(period=period)
    for clip in clips:
        try:
            url = clip["url"]
            print(f"[INFO] Downloading clip: {url}")
            path = download_twitch_clip(url)
            if path:
                print(f"[SUCCESS] Saved to: {path}")
            else:
                print("[SKIPPED] Already downloaded.")
        except Exception as e:
            print(f"[ERROR] Failed to download clip: {e}")


if __name__ == "__main__":
    main()
