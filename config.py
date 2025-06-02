# config.py

import os

# Use a writable directory within the project structure
CLIP_STORAGE_DIR = os.path.join(os.path.dirname(__file__), "clips")

TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID", "your_client_id_here")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET", "your_client_secret_here")

# Hardcoded list of Twitch usernames to monitor
CHANNEL_LIST = [
    "caedrel"
]
