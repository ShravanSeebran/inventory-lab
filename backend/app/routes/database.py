from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# The URL for our SQLite database file
SQLALCHEMY_DATABASE_URL = "sqlite:///./products.db"

# We create an engine that will handle the database connection.
# The `connect_args` are necessary for SQLite to work with FastAPI's threads.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# This is a factory for creating new database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# `declarative_base` is the base class for our database models.
Base = declarative_base()

# The dependency function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()