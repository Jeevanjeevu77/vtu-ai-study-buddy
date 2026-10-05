"""
database.py — SQLAlchemy setup for VTU Genius AI
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'vtu.db')

# On Vercel, the filesystem is read-only except for /tmp.
if os.environ.get("VERCEL") == "1":
    tmp_db_path = "/tmp/vtu.db"
    if not os.path.exists(tmp_db_path) and os.path.exists(db_path):
        shutil.copy2(db_path, tmp_db_path)
    db_path = tmp_db_path

DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency — yields a DB session and closes it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()