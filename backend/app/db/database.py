import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


# Keep the database URL configurable so local development, Docker, and
# production can each point at a different PostgreSQL database.
raw_database_url = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://workflowgym:workflowgym@localhost:5432/workflowgym",
)
if raw_database_url.startswith("postgres://"):
    DATABASE_URL = raw_database_url.replace("postgres://", "postgresql+psycopg://", 1)
elif raw_database_url.startswith("postgresql://"):
    DATABASE_URL = raw_database_url.replace("postgresql://", "postgresql+psycopg://", 1)
else:
    DATABASE_URL = raw_database_url


# The engine manages the database connection pool. pool_pre_ping checks
# connections before reuse, which helps deployed apps recover from stale DB
# connections after idle periods.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


# SessionLocal creates short-lived database sessions for requests and scripts.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Base class that future SQLAlchemy ORM models will inherit from."""


def get_db() -> Generator[Session, None, None]:
    """Provide one database session for a FastAPI request, then close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
