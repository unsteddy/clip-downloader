import os

# Base directory for storing clips, outside of project for scalability
BASE_CLIP_DIR = os.path.join(os.path.dirname(__file__), "clips")

# Twitch API credentials (replace with your real credentials or use env vars)
TWITCH_CLIENT_ID = "your_client_id_here"
TWITCH_CLIENT_SECRET = "your_client_secret_here"

# List of Twitch channels to monitor (no @ symbol)
CHANNEL_LIST = [
    "caedrel"
]

# Twitch clips root directory (inside BASE_CLIP_DIR)
# Clips will be saved in: BASE_CLIP_DIR/twitch/{streamer}/{YYYY-MM-DD}/
TWITCH_CLIP_ROOT = os.path.join(BASE_CLIP_DIR, "twitch")
