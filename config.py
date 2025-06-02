# config.py

import os

# Use a writable directory within the project structure
CLIP_STORAGE_DIR = os.path.join(os.path.dirname(__file__), "clips")

# Hardcoded Twitch API credentials (for development only)
TWITCH_CLIENT_ID = "your-hardcoded-client-id"
TWITCH_CLIENT_SECRET = "your-hardcoded-client-secret"

# Hardcoded list of Twitch usernames to monitor
CHANNEL_LIST = [
    "caedrel"#
]
