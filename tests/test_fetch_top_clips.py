# tests/test_fetch_top_clips.py

import unittest
from unittest.mock import patch, MagicMock
from downloader.twitch import fetch_top_clips


class TestFetchTopClips(unittest.TestCase):

    @patch("downloader.twitch.fetch_top_clips.download_twitch_clip")
    @patch("downloader.twitch.fetch_top_clips.fetch_all_top_clips")
    def test_main_success(self, mock_fetch_clips, mock_download_clip):
        mock_fetch_clips.return_value = [
            {"url": "https://twitch.tv/clip/fakeclip1"},
            {"url": "https://twitch.tv/clip/fakeclip2"}
        ]
        mock_download_clip.return_value = "/clips/fakeclip1.mp4"

        with patch("builtins.print") as mock_print:
            fetch_top_clips.main()

        mock_fetch_clips.assert_called_once()
        self.assertEqual(mock_download_clip.call_count, 2)
        mock_print.assert_any_call("[SUCCESS] Saved to: /clips/fakeclip1.mp4")

    @patch("downloader.twitch.fetch_top_clips.download_twitch_clip")
    @patch("downloader.twitch.fetch_top_clips.fetch_all_top_clips")
    def test_main_download_failure(self, mock_fetch_clips, mock_download_clip):
        mock_fetch_clips.return_value = [
            {"url": "https://twitch.tv/clip/failingclip"}
        ]
        mock_download_clip.side_effect = RuntimeError("Download error")

        with patch("builtins.print") as mock_print:
            fetch_top_clips.main()

        mock_print.assert_any_call("[ERROR] Failed to download clip: Download error")

    @patch("downloader.twitch.fetch_top_clips.download_twitch_clip")
    @patch("downloader.twitch.fetch_top_clips.fetch_all_top_clips")
    def test_main_clip_skipped(self, mock_fetch_clips, mock_download_clip):
        mock_fetch_clips.return_value = [
            {"url": "https://twitch.tv/clip/skippedclip"}
        ]
        mock_download_clip.return_value = None  # Simulates skipped download

        with patch("builtins.print") as mock_print:
            fetch_top_clips.main()

        mock_print.assert_any_call("[SKIPPED] Already downloaded.")


if __name__ == "__main__":
    unittest.main()
