# tests/test_clip_dao.py

import unittest
from unittest.mock import patch
from db.db import engine
from db.models import Base, Clip
from db.clip_dao import add_clip_if_new, mark_clip_downloaded, mark_clip_failed
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)


class TestClipDAO(unittest.TestCase):

    def setUp(self):
        # Create all tables fresh for each test
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(engine)

    def test_add_clip_if_new(self):
        slug = "testslug1"
        url = "https://www.twitch.tv/clip/testslug1"
        added = add_clip_if_new(slug, url)
        self.assertTrue(added)

        # Try adding again
        added_again = add_clip_if_new(slug, url)
        self.assertFalse(added_again)

    def test_mark_clip_downloaded(self):
        slug = "testslug2"
        url = "https://www.twitch.tv/clip/testslug2"
        path = "/clips/testslug2.mp4"
        add_clip_if_new(slug, url)
        mark_clip_downloaded(slug, path)

        clip = self.session.query(Clip).filter_by(slug=slug).first()
        self.assertEqual(clip.status, "downloaded")
        self.assertEqual(clip.path, path)
        self.assertIsNotNone(clip.downloaded_at)

    def test_mark_clip_failed(self):
        slug = "testslug3"
        url = "https://www.twitch.tv/clip/testslug3"
        error = "Download failed due to timeout"
        add_clip_if_new(slug, url)
        mark_clip_failed(slug, error)

        clip = self.session.query(Clip).filter_by(slug=slug).first()
        self.assertEqual(clip.status, "failed")
        self.assertEqual(clip.error, error)


if __name__ == '__main__':
    unittest.main()
