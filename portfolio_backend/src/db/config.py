import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class DatabaseConfig:
    """Configuration for connecting to PostgreSQL."""

    dsn: str


def _read_db_connection_guidance_file() -> Optional[str]:
    """
    Read DSN guidance from the database container's db_connection.txt.

    The referenced file typically contains a command like:
        psql postgresql://user:pass@host:port/dbname

    Returns the URL portion (postgresql://...) or None if not found.
    """
    # Repo layout: student-portfolio-hub-.../portfolio_backend/src/db/config.py
    # We want:    student-portfolio-hub-.../database/db_connection.txt
    repo_root = Path(__file__).resolve().parents[3]
    guidance_path = repo_root.parent / "student-portfolio-hub-211738-211748" / "database" / "db_connection.txt"
    if not guidance_path.exists():
        return None

    content = guidance_path.read_text(encoding="utf-8").strip()
    if not content:
        return None

    # Usually "psql <dsn>"
    parts = content.split()
    for part in parts:
        if part.startswith("postgresql://") or part.startswith("postgres://"):
            return part

    # Fallback: if the entire line is the DSN
    if content.startswith("postgresql://") or content.startswith("postgres://"):
        return content

    return None


def _normalize_to_async_driver(dsn: str) -> str:
    """
    Ensure DSN uses asyncpg driver for SQLAlchemy async engine.

    SQLAlchemy async URL format for Postgres:
      postgresql+asyncpg://user:pass@host:port/db
    """
    if dsn.startswith("postgresql+asyncpg://"):
        return dsn
    if dsn.startswith("postgresql://"):
        return dsn.replace("postgresql://", "postgresql+asyncpg://", 1)
    if dsn.startswith("postgres://"):
        # Some providers use postgres://; SQLAlchemy prefers postgresql://
        return dsn.replace("postgres://", "postgresql+asyncpg://", 1)
    return dsn


# PUBLIC_INTERFACE
def get_database_config() -> DatabaseConfig:
    """Return the active database configuration.

    Precedence:
    1) DATABASE_DSN environment variable (recommended for deployments)
    2) db_connection.txt guidance (repository-provided dev/local default)

    Notes:
    - db_connection.txt currently indicates port 5000; the work item mentions DB preview on 5001.
      We follow db_connection.txt as the authoritative DSN guidance for the backend connection.
    """
    env_dsn = os.getenv("DATABASE_DSN")
    if env_dsn:
        return DatabaseConfig(dsn=_normalize_to_async_driver(env_dsn))

    guidance_dsn = _read_db_connection_guidance_file()
    if guidance_dsn:
        return DatabaseConfig(dsn=_normalize_to_async_driver(guidance_dsn))

    raise RuntimeError(
        "Database DSN not configured. Set DATABASE_DSN env var or provide database/db_connection.txt."
    )
