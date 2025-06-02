# downloader/twitch_api.py

import requests
from config import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, CHANNEL_LIST

TWITCH_AUTH_URL = "https://id.twitch.tv/oauth2/token"
TWITCH_API_URL = "https://api.twitch.tv/helix"


def get_access_token():
    response = requests.post(TWITCH_AUTH_URL, params={
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    })
    response.raise_for_status()
    return response.json()["access_token"]


def get_user_ids(headers):
    user_ids = {}
    for username in CHANNEL_LIST:
        response = requests.get(
            f"{TWITCH_API_URL}/users",
            headers=headers,
            params={"login": username}
        )
        response.raise_for_status()
        data = response.json()["data"]
        if data:
            user_ids[username] = data[0]["id"]
    return user_ids


def get_top_clips(headers, user_id, period="day", first=10):
    response = requests.get(
        f"{TWITCH_API_URL}/clips",
        headers=headers,
        params={
            "broadcaster_id": user_id,
            "period": period,
            "first": first
        }
    )
    response.raise_for_status()
    return response.json().get("data", [])


def fetch_all_top_clips(period="day", first=10):
    access_token = get_access_token()
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }

    user_ids = get_user_ids(headers)
    all_clips = []
    for username, user_id in user_ids.items():
        clips = get_top_clips(headers, user_id, period=period, first=first)
        all_clips.extend(clips)
    return all_clips


if __name__ == "__main__":
    print("--- Top Clips (24h) ---")
    for clip in fetch_all_top_clips(period="day"):
        print(clip["url"])

    print("\n--- Top Clips (7d) ---")
    for clip in fetch_all_top_clips(period="week"):
        print(clip["url"])

    print("\n--- Top Clips (30d) ---")
    for clip in fetch_all_top_clips(period="month"):
        print(clip["url"])

    print("\n--- All-Time Top Clips ---")
    for clip in fetch_all_top_clips(period="all"):
        print(clip["url"])
