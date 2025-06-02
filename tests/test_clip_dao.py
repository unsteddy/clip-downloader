import unittest
from datetime import datetime
from db.db import engine
from db.models import Base, Clip
from db.clip_dao import add_clip_if_new, mark_clip_downloaded, mark_clip_failed
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)


class TestClipDAO(unittest.TestCase):

    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(engine)

    def test_add_clip_if_new_when_no_existing(self):
        slug = "testslug1"
        url = "https://www.twitch.tv/clip/testslug1"
        added = add_clip_if_new(slug, url)
        self.assertTrue(added)

    def test_add_clip_if_new_when_already_downloaded(self):
        slug = "testslug2"
        url = "https://www.twitch.tv/clip/testslug2"
        add_clip_if_new(slug, url)
        mark_clip_downloaded(slug, "/clips/testslug2.mp4")

        # Should return False because already downloaded
        added_again = add_clip_if_new(slug, url)
        self.assertFalse(added_again)

    def test_add_clip_if_new_when_previously_failed(self):
        slug = "testslug3"
        url = "https://www.twitch.tv/clip/testslug3"
        add_clip_if_new(slug, url)
        mark_clip_failed(slug, "network error")

        # Should reset status to pending and allow retry
        added_again = add_clip_if_new(slug, url)
        self.assertTrue(added_again)

        # Verify clip status is reset to pending
        clip = self.session.query(Clip).filter_by(slug=slug).first()
        self.assertEqual(clip.status, "pending")
        self.assertIsNone(clip.error)
        self.assertIsNone(clip.downloaded_at)

    def test_mark_clip_downloaded(self):
        slug = "testslug4"
        url = "https://www.twitch.tv/clip/testslug4"
        add_clip_if_new(slug, url)
        mark_clip_downloaded(slug, "/clips/testslug4.mp4")

        clip = self.session.query(Clip).filter_by(slug=slug).first()
        self.assertEqual(clip.status, "downloaded")
        self.assertEqual(clip.path, "/clips/testslug4.mp4")
        self.assertIsNotNone(clip.downloaded_at)

    def test_mark_clip_failed(self):
        slug = "testslug5"
        url = "https://www.twitch.tv/clip/testslug5"
        add_clip_if_new(slug, url)
        mark_clip_failed(slug, "timeout error")

        clip = self.session.query(Clip).filter_by(slug=slug).first()
        self.assertEqual(clip.status, "failed")
        self.assertEqual(clip.error, "timeout error")

    def test_mark_clip_downloaded_saves_full_path(self):
        slug = "testslug_path"
        url = "https://www.twitch.tv/clip/testslug_path"
        add_clip_if_new(slug, url)
        path = "/clips/twitch/caedrel/2025-06-02/testslug_path.mp4"
        mark_clip_downloaded(slug, path)

        clip = self.session.query(Clip).filter_by(slug=slug).first()
        self.assertEqual(clip.status, "downloaded")
        self.assertEqual(clip.path, path)


if __name__ == "__main__":
    unittest.main()
