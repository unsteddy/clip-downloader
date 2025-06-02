# db.py

from sqlalchemy import create_engine
from db.models import Base

# SQLite for now – change this for Oracle later
engine = create_engine("sqlite:///clipfarm.db")

# Create tables if not already present
Base.metadata.create_all(engine)
