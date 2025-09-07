"""
database.py

Database setup for the project using SQLAlchemy + SQLite.

- Exports: engine, SessionLocal, get_db, create_tables
- It will try to import Base from either `app.models` or `models`
depending on your project layout.
"""

import os
from contextlib import contextmanager
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

# Try flexible imports for Base (depending on whether models.py is in app/ or root)
try:
    # If your project uses package "app"
    from models import Base
except Exception:
    try:
        # If models.py is in the project root
        from models import Base
    except Exception:
        raise ImportError(
            "Could not import Base from app.models or models. "
            "Make sure your models.py defines Base = declarative_base()."
        )

# ----------------------------
# Configuration
# ----------------------------
# Use environment variable DATABASE_URL if present, otherwise default to local sqlite file.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nursery.db")

# For SQLite we must pass check_same_thread=False for multi-threaded apps (e.g. FastAPI uvicorn workers).
# Also enable pragmas for foreign keys (ensures FK enforcement in SQLite).
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False, future=True)

# Ensure SQLite enforces foreign keys (PRAGMA foreign_keys = ON) on each connection.
# This listener runs only for SQLite engines.
from sqlalchemy.engine import Engine
from sqlalchemy import text


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    # Only apply for sqlite
    if DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# Session factory (use this to create DB sessions)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


# ----------------------------
# Helpers / Dependency (FastAPI)
# ----------------------------
def get_db():
    """
    Dependency generator for FastAPI endpoints.

    Usage with FastAPI:
        from database import get_db
        @router.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session():
    """
    Context manager alternative for non-FastAPI code.
    Usage:
        with db_session() as db:
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------
# Create tables helper
# ----------------------------
def create_tables():
    """
    Create all tables defined on Base.metadata.
    Call this during initial setup or from a script.
    In production use migrations (Alembic) instead of this function.
    """
    Base.metadata.create_all(bind=engine)


# ----------------------------
# CLI convenience
# ----------------------------
if __name__ == "__main__":
    # Quick initialization when running this file directly:
    print("Creating database tables (if not exist)...")
    create_tables()
    print("Done. Database URL:", DATABASE_URL)
    # Optional: add seeding code here if you want initial records.
