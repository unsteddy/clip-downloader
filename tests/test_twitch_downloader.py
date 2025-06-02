import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from downloader.twitch import twitch_downloader
from db.db import engine
from db.models import Base, Clip
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Session = sessionmaker(bind=engine)

class TestTwitchDownloader(unittest.TestCase):

    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()
        self.test_base_dir = os.path.join(os.path.dirname(__file__), "test_clips")
        self.test_clip_root = os.path.join(self.test_base_dir, "twitch")
        os.makedirs(self.test_clip_root, exist_ok=True)

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(engine)
        shutil.rmtree(self.test_base_dir, ignore_errors=True)

    @patch("downloader.twitch.twitch_downloader.TWITCH_CLIP_ROOT", new=os.path.join(os.path.dirname(__file__), "test_clips", "twitch"))
    @patch("subprocess.run")
    def test_successful_download_creates_correct_path(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        test_url = "https://www.twitch.tv/caedrel/clip/testslug"
        path = twitch_downloader.download_twitch_clip(test_url)

        self.assertIn("/twitch/caedrel/", path)
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        self.assertIn(date_str, path)
        self.assertTrue(path.endswith("testslug.mp4"))

        clip = self.session.query(Clip).filter_by(slug="testslug").first()
        self.assertIsNotNone(clip)
        self.assertEqual(clip.status, "downloaded")
        self.assertEqual(clip.path, path)

    @patch("downloader.twitch.twitch_downloader.TWITCH_CLIP_ROOT", new=os.path.join(os.path.dirname(__file__), "test_clips", "twitch"))
    @patch("subprocess.run")
    def test_failed_download(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Streamlink error"
        mock_run.return_value = mock_result

        test_url = "https://www.twitch.tv/caedrel/clip/failingclip"
        path = twitch_downloader.download_twitch_clip(test_url)

        self.assertEqual(path, "")

        clip = self.session.query(Clip).filter_by(slug="failingclip").first()
        self.assertIsNotNone(clip)
        self.assertEqual(clip.status, "failed")
        self.assertIn("Streamlink error", clip.error)

if __name__ == "__main__":
    unittest.main()
