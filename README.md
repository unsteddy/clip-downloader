# 🎮 Clip Downloader (Twitch Edition)

A modular microservice built in Python to **automatically download Twitch clips**, organize them, perform light editing (e.g., subtitles), and prepare for upload to platforms like YouTube Shorts. This forms part of an automated **clip farm** project aiming to scale monetizable content creation.

---

## 📁 Project Structure

```
clip-downloader/
├── config.py                      # Loads Twitch API credentials from env
├── downloader/
│   ├── __init__.py
│   ├── twitch_api.py             # Handles OAuth and Twitch API requests
│   ├── twitch_downloader.py     # Downloads clips via Streamlink
│   └── fetch_top_clips.py       # Entrypoint for fetching top clips
├── db/
│   ├── __init__.py
│   ├── db.py                     # DB engine and session setup
│   ├── clip_dao.py               # Clip insert/query logic
│   └── models.py                 # SQLAlchemy model definitions
├── tests/
│   ├── test_fetch_top_clips.py
│   ├── test_twitch_api.py
│   ├── test_twitch_downloader.py
│   └── ...
├── requirements.txt
├── .env                          # Optional - store Twitch credentials
└── README.md
```

---

## 🧠 Features

* ✅ Fetches top Twitch clips by period (day/week/month)
* ✅ Downloads clips in `.mp4` using Streamlink
* ✅ Stores metadata in SQLite (with Oracle planned)
* ✅ Saves clips under: `/clips/twitch/{streamer}/{YYYY-MM-DD}/clipname.mp4`
* ✅ Fully unit tested with mocks and patching
* ⚙️ Ready for expansion: subtitles, watermarks, upload pipeline

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/clip-downloader.git
cd clip-downloader
```

### 2. Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set environment variables

Use a `.env` file or export manually:

```env
TWITCH_CLIENT_ID=your_client_id
TWITCH_CLIENT_SECRET=your_client_secret
```

---

## ▶️ Usage

### Fetch top clips (e.g., daily)

```bash
python -m downloader.twitch.fetch_top_clips day
```

Periods: `day`, `week`, `month`

---

## 🧪 Testing

Tests are located in `tests/`. They mock all external dependencies (API, filesystem, environment).

```bash
pytest
```

Make sure to patch `TWITCH_CLIP_ROOT` to isolate file paths during tests.

---

## 📌 Dependencies

* `requests` – Twitch API calls
* `streamlink` – Downloads .mp4 from Twitch clip URLs
* `sqlalchemy` – ORM for metadata
* `python-dotenv` – Optional env loader
* `pytest` & `unittest.mock` – Test framework

---

## 🚧 Coming Soon

* Automated subtitle generation (Whisper)
* Language localization pipeline
* Video editing module (FFmpeg, watermarking)
* Upload automation to Shorts, TikTok, etc.

---

## 💬 Feedback & Contributions

If you're using this as part of a clip-farm automation stack, feel free to contribute ideas or raise issues.

---
