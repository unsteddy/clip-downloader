# tests/test_twitch_api.py

import unittest
from unittest.mock import patch, MagicMock
from downloader.twitch import twitch_api
import requests


class TestTwitchAPI(unittest.TestCase):

    @patch("downloader.twitch.twitch_api.requests.post")
    def test_get_access_token_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "fake_token"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        token = twitch_api.get_access_token()
        self.assertEqual(token, "fake_token")

    @patch("downloader.twitch.twitch_api.requests.post")
    def test_get_access_token_failure(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("API error")
        with self.assertRaises(requests.exceptions.RequestException):
            twitch_api.get_access_token()

    @patch("downloader.twitch.twitch_api.requests.get")
    def test_get_user_ids_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{"id": "123", "login": "streamer1"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        headers = {"Authorization": "Bearer fake_token"}
        with patch("downloader.twitch.twitch_api.CHANNEL_LIST", ["streamer1"]):
            user_ids = twitch_api.get_user_ids(headers)
            self.assertEqual(user_ids, {"streamer1": "123"})

    @patch("downloader.twitch.twitch_api.requests.get")
    def test_get_user_ids_empty_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        headers = {"Authorization": "Bearer fake_token"}
        with patch("downloader.twitch.twitch_api.CHANNEL_LIST", ["unknown_user"]):
            user_ids = twitch_api.get_user_ids(headers)
            self.assertEqual(user_ids, {})

    @patch("downloader.twitch.twitch_api.requests.get")
    def test_get_top_clips_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{"url": "https://twitch.tv/clip/abc123"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        headers = {"Authorization": "Bearer fake_token"}
        clips = twitch_api.get_top_clips(headers, user_id="123", period="day")
        self.assertEqual(len(clips), 1)
        self.assertEqual(clips[0]["url"], "https://twitch.tv/clip/abc123")

    @patch("downloader.twitch.twitch_api.requests.get")
    def test_get_top_clips_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Clip fetch error")
        headers = {"Authorization": "Bearer fake_token"}
        with self.assertRaises(requests.exceptions.RequestException):
            twitch_api.get_top_clips(headers, user_id="123", period="day")


if __name__ == "__main__":
    unittest.main()
