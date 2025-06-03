# Clip Downloader

This project downloads clips from Twitch and TikTok, stores their metadata in a local SQLite database (`clipfarm.db`), and prepares them for further processing (e.g., subtitle removal and overlay for Chinese videos).

## Project Structure

```
clip-downloader/
├── db/
│   ├── db.py
│   ├── models.py
│   ├── clip_dao.py
├── downloader/
│   ├── twitch/
│   │   ├── twitch_api.py
│   │   ├── twitch_downloader.py
│   │   ├── fetch_top_clips.py
│   ├── tiktok/
│   │   ├── tiktok_scraper.py
│   │   ├── fetch_top_hashtag_videos.py
│   │   ├── fix_cookies.py
│   │   ├── stealth.min.js
│   │   ├── cookies.json
├── clips/
│   ├── twitch/...      # Saved Twitch clips
│   ├── tiktok/...      # Saved TikTok clips
│   └── samples/...     # Test input videos
```

## Requirements

```bash
pip install -r requirements.txt
playwright install
sudo apt install libnss3 libatk-bridge2.0-0 libxss1 libasound2 libxshmfence1 libgbm1 libgtk-3-0
```

## TikTok Hashtag Scraping

The `downloader/tiktok/tiktok_scraper.py` script fetches top TikTok videos from a given hashtag using Playwright.

**Key Features:**

* Headless browser with stealth.js injection
* Cookie-based authentication (needed to avoid detection)
* Scrolls dynamically to reveal video links
* Extracts top 10 video links and titles

### Running:

```bash
python3 -m downloader.tiktok.fetch_top_hashtag_videos
```

### Setting Up `cookies.json`

1. Install **[Cookie-Editor Chrome Extension](https://chrome.google.com/webstore/detail/cookie-editor/kkkbiiikibmpmjijgimjkkikbemlallb)**
2. Go to [https://www.tiktok.com/tag/funny](https://www.tiktok.com/tag/funny)
3. Click Cookie Editor → Export → Copy
4. Paste into `downloader/tiktok/cookies.json`
5. Run the fixer script:

```bash
python3 downloader/tiktok/fix_cookies.py
```

This will patch all cookies to include the required `sameSite` attribute.

## Subtitle Removal (Proof of Concept)

We tested automatic removal and translation overlay on a Douyin/TikTok frame:

* Detected red-colored Chinese subtitles using HSV masking
* Removed with inpainting
* Overlaid English translation in its place

This will be expanded to full-video automation.

## Next Steps

* Batch subtitle removal over full videos
* Whisper-based audio transcription + translation
* Subtitle re-rendering in consistent style
* Auto-upload pipeline
