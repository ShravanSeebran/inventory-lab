"""Database setup and session management using SQLAlchemy."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./inventory.db")

options = {}
if DATABASE_URL.startswith("sqlite"):
    options["connect_args"] = {"check_same_thread": False}
    if ":memory:" in DATABASE_URL or DATABASE_URL == "sqlite://":
        options["poolclass"] = StaticPool
engine = create_engine(DATABASE_URL, **options)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
