import os
import time
from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


def _read_password() -> str:
    password_file = os.getenv("POSTGRES_PASSWORD_FILE")
    if password_file:
        with open(password_file, encoding="utf-8") as file:
            return file.read().strip()
    return os.getenv("POSTGRES_PASSWORD", "")


def get_database_url() -> str | URL:
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    return URL.create(
        "postgresql+psycopg",
        username=os.getenv("POSTGRES_USER", "app"),
        password=_read_password(),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        database=os.getenv("POSTGRES_DB", "appdb"),
    )


@lru_cache
def get_engine() -> Engine:
    return create_engine(get_database_url(), pool_pre_ping=True)


def get_session() -> Iterator[Session]:
    with Session(get_engine()) as session:
        yield session


def init_db(retries: int = 30, delay: float = 1.0) -> None:
    """Create tables, waiting for the database to become available."""
    for attempt in range(retries):
        try:
            Base.metadata.create_all(get_engine())
            return
        except OperationalError:
            if attempt == retries - 1:
                raise
            time.sleep(delay)
