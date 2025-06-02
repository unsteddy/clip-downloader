# tests/test_twitch_downloader.py

import unittest
from unittest.mock import patch, MagicMock
from downloader.twitch_downloader import download_twitch_clip
from db.db import engine
from db.models import Base, Clip
from sqlalchemy.orm import sessionmaker

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
    def test_successful_download(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        test_url = "https://www.twitch.tv/clip/FakeClipSlug"
        path = download_twitch_clip(test_url)

        self.assertTrue(path.endswith("FakeClipSlug.mp4"))
        clip = self.session.query(Clip).filter_by(slug="FakeClipSlug").first()
        self.assertIsNotNone(clip)
        self.assertEqual(clip.status, "downloaded")
        self.assertEqual(clip.path, path)

    @patch("subprocess.run")
    def test_failed_download(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Streamlink error"
        mock_run.return_value = mock_result

        test_url = "https://www.twitch.tv/clip/FailingClip"
        with self.assertRaises(RuntimeError):
            download_twitch_clip(test_url)

        clip = self.session.query(Clip).filter_by(slug="FailingClip").first()
        self.assertIsNotNone(clip)
        self.assertEqual(clip.status, "failed")
        self.assertIn("Streamlink error", clip.error)

    def test_invalid_url(self):
        invalid_url = "https://www.twitch.tv/videos/12345"
        with self.assertRaises(ValueError):
            download_twitch_clip(invalid_url)


if __name__ == '__main__':
    unittest.main()
