import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from repository_lab.database import Base, get_session
from repository_lab.main import app


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    def override_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    engine.dispose()


def test_create_item(client):
    response = client.post("/items", json={"name": "book", "description": "paper"})
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == "book"


def test_list_items(client):
    client.post("/items", json={"name": "a"})
    client.post("/items", json={"name": "b"})
    response = client.get("/items")
    assert response.status_code == 200
    assert [item["name"] for item in response.json()] == ["a", "b"]


def test_get_item(client):
    created = client.post("/items", json={"name": "pen"}).json()
    response = client.get(f"/items/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "pen"


def test_get_missing_item_returns_404(client):
    assert client.get("/items/999").status_code == 404


def test_delete_item(client):
    created = client.post("/items", json={"name": "tmp"}).json()
    assert client.delete(f"/items/{created['id']}").status_code == 204
    assert client.get(f"/items/{created['id']}").status_code == 404


def test_delete_missing_item_returns_404(client):
    assert client.delete("/items/999").status_code == 404


def test_create_item_validation(client):
    assert client.post("/items", json={"name": ""}).status_code == 422
