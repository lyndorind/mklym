import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from repository_lab import database
from repository_lab.database import (
    get_database_url,
    get_engine,
    get_session,
    init_db,
)
from repository_lab.main import app


@pytest.fixture(autouse=True)
def _clear_engine_cache():
    get_engine.cache_clear()
    yield
    get_engine.cache_clear()


def test_database_url_from_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///x.db")
    assert get_database_url() == "sqlite:///x.db"


def test_database_url_with_password_file(monkeypatch, tmp_path):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    secret = tmp_path / "password"
    secret.write_text("s3cret\n", encoding="utf-8")
    monkeypatch.setenv("POSTGRES_PASSWORD_FILE", str(secret))
    monkeypatch.setenv("POSTGRES_HOST", "db")
    monkeypatch.setenv("POSTGRES_USER", "app")
    monkeypatch.setenv("POSTGRES_DB", "appdb")
    url = get_database_url()
    assert url.host == "db"
    assert url.password == "s3cret"
    assert url.database == "appdb"


def test_database_url_with_password_env(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("POSTGRES_PASSWORD_FILE", raising=False)
    monkeypatch.setenv("POSTGRES_PASSWORD", "pw")
    assert get_database_url().password == "pw"


def test_get_session_yields_session(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    generator = get_session()
    assert isinstance(next(generator), Session)
    generator.close()


def test_init_db_creates_tables(monkeypatch, tmp_path):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{(tmp_path / 't.db').as_posix()}")
    init_db()
    assert "items" in inspect(get_engine()).get_table_names()


def test_init_db_retries_until_ready(monkeypatch):
    attempts = []

    def flaky_create_all(*_args, **_kwargs):
        attempts.append(1)
        if len(attempts) < 3:
            raise OperationalError("connect", {}, Exception("down"))

    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    monkeypatch.setattr(database.Base.metadata, "create_all", flaky_create_all)
    monkeypatch.setattr(database.time, "sleep", lambda _seconds: None)
    init_db(retries=5)
    assert len(attempts) == 3


def test_init_db_gives_up(monkeypatch):
    def always_fail(*_args, **_kwargs):
        raise OperationalError("connect", {}, Exception("down"))

    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    monkeypatch.setattr(database.Base.metadata, "create_all", always_fail)
    monkeypatch.setattr(database.time, "sleep", lambda _seconds: None)
    with pytest.raises(OperationalError):
        init_db(retries=2)


def test_app_lifespan_initialises_database(monkeypatch, tmp_path):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{(tmp_path / 'a.db').as_posix()}")
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
    assert "items" in inspect(get_engine()).get_table_names()
