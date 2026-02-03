from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.db.config import get_database_config


class Base(DeclarativeBase):
    """SQLAlchemy declarative base class for ORM models."""


_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker[AsyncSession] | None = None


def _get_engine() -> AsyncEngine:
    """Create (if needed) and return the shared async SQLAlchemy engine."""
    global _engine, _sessionmaker
    if _engine is None:
        cfg = get_database_config()
        _engine = create_async_engine(
            cfg.dsn,
            pool_pre_ping=True,
        )
        _sessionmaker = async_sessionmaker(bind=_engine, expire_on_commit=False, class_=AsyncSession)
    return _engine


# PUBLIC_INTERFACE
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an AsyncSession and closes it after request."""
    _get_engine()
    assert _sessionmaker is not None
    async with _sessionmaker() as session:
        yield session
