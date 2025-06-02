# 📼 ClipDownloader

**ClipDownloader** is a Python microservice that automatically fetches, downloads, and tracks top Twitch clips for multiple channels. It's fully test-covered, scalable, and designed to support additional platforms later.

---

## 🚀 Features
- Fetch top Twitch clips (daily/weekly/monthly/all-time)
- Store clip metadata in a SQLite or Oracle-ready database
- Prevent duplicate downloads
- Modular, testable architecture
- Easy integration with Whisper, uploaders, etc.

---

## 🧱 Project Structure
```text
ClipDownloader/
├── config.py                  # Config for clip path, Twitch API, channels
├── main.py                    # Entry-point to download one clip
├── db/                        # Database models and DAO layer
├── downloader/
│   ├── twitch_downloader.py  # Core streamlink-based downloader
│   └── twitch/
│       ├── twitch_api.py     # Twitch OAuth + clip fetching logic
│       └── fetch_top_clips.py # Cron-compatible fetch+download runner
├── tests/                     # Full unit test suite (mocked)
└── clips/                     # (Optional) Output folder for downloaded clips
```

---

## ⚙️ Setup
```bash
pip install -r requirements.txt
```

Edit `config.py` to include your:
- `TWITCH_CLIENT_ID`
- `TWITCH_CLIENT_SECRET`
- List of Twitch channels to monitor

---

## 🧪 Run Tests
```bash
python -m unittest discover -s tests
```

---

## ⏱ Schedule Cron Job Example
```cron
0 3 * * * /usr/bin/python3 /path/to/fetch_top_clips.py day >> /path/to/logs/cron.log 2>&1
```

---

## 🔮 Future Plans
- Subtitle generation with Whisper
- Automatic short-form video uploaders
- Support for YouTube, Kick, Reddit clips

---

## 📄 License
MIT (or your preferred license)
