# clip_dao.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from db.db import engine
from db.models import Clip

Session = sessionmaker(bind=engine)


def add_clip_if_new(slug: str, url: str) -> bool:
    session = Session()
    try:
        if session.query(Clip).filter_by(slug=slug).first():
            return False
        clip = Clip(slug=slug, url=url, status="pending", created_at=datetime.utcnow())
        session.add(clip)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
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
