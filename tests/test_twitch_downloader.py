import unittest
from unittest.mock import patch, MagicMock

from downloader.twitch.twitch_downloader import download_twitch_clip
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

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(engine)

    @patch("subprocess.run")
    def test_successful_download_creates_correct_path(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        test_url = "https://www.twitch.tv/caedrel/clip/testslug"
        path = download_twitch_clip(test_url)

        # Check path includes twitch, streamer, and date folders
        self.assertIn("/clips/twitch/caedrel/", path)

        # Date folder: current UTC date string
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        self.assertIn(date_str, path)

        # Clip slug in filename
        self.assertTrue(path.endswith("testslug.mp4"))

        # Clip record updated in DB
        clip = self.session.query(Clip).filter_by(slug="testslug").first()
        self.assertIsNotNone(clip)
        self.assertEqual(clip.status, "downloaded")
        self.assertEqual(clip.path, path)

    @patch("subprocess.run")
    def test_failed_download(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Streamlink error"
        mock_run.return_value = mock_result

        test_url = "https://www.twitch.tv/caedrel/clip/failingclip"
        with self.assertRaises(RuntimeError):
            download_twitch_clip(test_url)

        clip = self.session.query(Clip).filter_by(slug="failingclip").first()
        self.assertIsNotNone(clip)
        self.assertEqual(clip.status, "failed")
        self.assertIn("Streamlink error", clip.error)

if __name__ == "__main__":
    unittest.main()
