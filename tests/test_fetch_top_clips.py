import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from downloader.twitch import fetch_top_clips

class TestFetchTopClips(unittest.TestCase):

    def setUp(self):
        self.test_base_dir = os.path.join(os.path.dirname(__file__), "test_clips")
        self.test_clip_root = os.path.join(self.test_base_dir, "twitch")
        os.makedirs(self.test_clip_root, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_base_dir, ignore_errors=True)

    @patch("downloader.twitch.twitch_downloader.TWITCH_CLIP_ROOT", new=os.path.join(os.path.dirname(__file__), "test_clips", "twitch"))
    @patch("downloader.twitch.fetch_top_clips.download_twitch_clip")
    @patch("downloader.twitch.fetch_top_clips.fetch_all_top_clips")
    def test_main_success(self, mock_fetch_all_top_clips, mock_download_twitch_clip):
        mock_fetch_all_top_clips.return_value = [
            {"url": "https://twitch.tv/clip/fakeclip1"},
            {"url": "https://twitch.tv/clip/fakeclip2"}
        ]
        mock_download_twitch_clip.return_value = os.path.join(self.test_clip_root, "fakeclip1.mp4")

        with patch("builtins.print") as mock_print:
            fetch_top_clips.main()

        mock_fetch_all_top_clips.assert_called_once()
        self.assertEqual(mock_download_twitch_clip.call_count, 2)
        mock_print.assert_any_call(f"[SUCCESS] Saved to: {os.path.join(self.test_clip_root, 'fakeclip1.mp4')}")

    @patch("downloader.twitch.twitch_downloader.TWITCH_CLIP_ROOT", new=os.path.join(os.path.dirname(__file__), "test_clips", "twitch"))
    @patch("downloader.twitch.fetch_top_clips.download_twitch_clip")
    @patch("downloader.twitch.fetch_top_clips.fetch_all_top_clips")
    def test_main_download_failure(self, mock_fetch_all_top_clips, mock_download_twitch_clip):
        mock_fetch_all_top_clips.return_value = [
            {"url": "https://twitch.tv/clip/failingclip"}
        ]
        mock_download_twitch_clip.side_effect = RuntimeError("Download error")

        with patch("builtins.print") as mock_print:
            fetch_top_clips.main()

        mock_print.assert_any_call("[ERROR] Failed to download clip: Download error")

    @patch("downloader.twitch.twitch_downloader.TWITCH_CLIP_ROOT", new=os.path.join(os.path.dirname(__file__), "test_clips", "twitch"))
    @patch("downloader.twitch.fetch_top_clips.download_twitch_clip")
    @patch("downloader.twitch.fetch_top_clips.fetch_all_top_clips")
    def test_main_clip_skipped(self, mock_fetch_all_top_clips, mock_download_twitch_clip):
        mock_fetch_all_top_clips.return_value = [
            {"url": "https://twitch.tv/clip/skippedclip"}
        ]
        mock_download_twitch_clip.return_value = None  # Simulates skipped download

        with patch("builtins.print") as mock_print:
            fetch_top_clips.main()

        mock_print.assert_any_call("[SKIPPED] Already downloaded.")

if __name__ == "__main__":
    unittest.main()
