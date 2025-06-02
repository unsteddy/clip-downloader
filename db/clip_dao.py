from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from db.db import engine
from db.models import Clip

Session = sessionmaker(bind=engine)


def add_clip_if_new(slug: str, url: str) -> bool:
    session = Session()
    try:
        clip = session.query(Clip).filter_by(slug=slug).first()
        if clip:
            if clip.status == "downloaded":
                # Already downloaded - skip
                return False
            elif clip.status == "failed":
                # Reset to pending for retry
                clip.status = "pending"
                clip.error = None
                clip.downloaded_at = None
                session.commit()
                return True
            else:
                # status pending or other, allow to proceed
                return True
        else:
            new_clip = Clip(slug=slug, url=url, status="pending", created_at=datetime.utcnow())
            session.add(new_clip)
            session.commit()
            return True
    finally:
        session.close()


def mark_clip_downloaded(slug: str, path: str):
    session = Session()
    try:
        clip = session.query(Clip).filter_by(slug=slug).first()
        if clip:
            clip.status = "downloaded"
            clip.path = path
            clip.downloaded_at = datetime.utcnow()
            session.commit()
    finally:
        session.close()


def mark_clip_failed(slug: str, error: str):
    session = Session()
    try:
        clip = session.query(Clip).filter_by(slug=slug).first()
        if clip:
            clip.status = "failed"
            clip.error = error
            session.commit()
    finally:
        session.close()
