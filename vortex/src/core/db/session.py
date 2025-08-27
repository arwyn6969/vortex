"""Database session management for Vortex."""

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

# Get database URL from environment or use default
DATABASE_URL = os.getenv(
    'VORTEX_DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/vortex'
)

# Create engine with connection pooling
try:
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800  # Recycle connections after 30 minutes
    )
except ImportError:
    # Fallback to in-memory SQLite if psycopg2 is not available
    engine = create_engine("sqlite:///:memory:", echo=False)

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db() -> None:
    """Initialize the database."""
    from .models import Base
    Base.metadata.create_all(bind=engine)

def get_session() -> Session:
    """Get a new database session."""
    return SessionLocal() 