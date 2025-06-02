# models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime

Base = declarative_base()

class Clip(Base):
    __tablename__ = 'clips'

    slug = Column(String, primary_key=True)
    url = Column(Text, nullable=False)
    status = Column(String, default="pending")
    path = Column(Text)
    error = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    downloaded_at = Column(DateTime)
