from app.db import models  # noqa: F401
from app.db.database import Base, engine


def init_db() -> None:
    """Create tables from SQLAlchemy models for the learning version."""
    Base.metadata.create_all(bind=engine)


def reset_db() -> None:
    """Drop and recreate all tables for repeatable local demos."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
