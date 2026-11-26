"""Engine and session factory. SQLite by default; any SQLAlchemy URL (e.g. PostgreSQL) works."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Declarative base of all tables."""
    pass


def make_engine(url: str) -> Engine:
    """Create the engine; for SQLite also create the folder and enable foreign keys and WAL."""
    if url.startswith("sqlite"):
        path = url.split("///", 1)[1] if "///" in url else ""
        if path and path != ":memory:":
            import os

            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        engine = create_engine(url, connect_args={"check_same_thread": False}, pool_pre_ping=True)

        @event.listens_for(engine, "connect")
        def _pragmas(dbapi_conn, _record):  # type: ignore[no-untyped-def]
            cur = dbapi_conn.cursor()
            cur.execute("PRAGMA foreign_keys=ON")
            cur.execute("PRAGMA journal_mode=WAL")
            cur.close()

        return engine
    return create_engine(url, pool_pre_ping=True)


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Session factory bound to the engine."""
    return sessionmaker(engine, expire_on_commit=False)


@contextmanager
def session_scope(factory: sessionmaker[Session]) -> Iterator[Session]:
    """A session that commits on success and rolls back on error."""
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
