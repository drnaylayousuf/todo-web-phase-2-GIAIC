from sqlmodel import create_engine, Session
from .config import settings
from contextlib import contextmanager
from typing import Generator
from fastapi import Depends
from .models.user import User
from .models.task import Task
from sqlmodel import SQLModel

# Create the database engine
engine = create_engine(
    str(settings.database_url),
    echo=settings.db_echo,
    pool_pre_ping=True,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow
)

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)

def get_db_session() -> Generator[Session, None, None]:
    """Dependency for database sessions"""
    with Session(engine) as session:
        yield session