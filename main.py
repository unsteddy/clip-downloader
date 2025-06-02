# main.py

import sys
from twitch.twitch_downloader import download_twitch_clip


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <twitch_clip_url>")
        sys.exit(1)

    clip_url = sys.argv[1]
    try:
        output_path = download_twitch_clip(clip_url)
        if output_path:
            print(f"[MAIN] Clip successfully downloaded to: {output_path}")
        else:
            print("[MAIN] Clip was already processed.")
    except Exception as e:
        print(f"[MAIN] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
