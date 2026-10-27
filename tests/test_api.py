import allure
from fastapi.testclient import TestClient

from repository_lab.main import app

client = TestClient(app)

@allure.feature("Endpoints")
@allure.story("Root")
def test_root_returns_welcome_message():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Repository Lab API"}

@allure.feature("Endpoints")
@allure.story("Info")
def test_info_returns_service_name():
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json() == {"service": "Repository Lab API"}

@allure.feature("Endpoints")
@allure.story("Health")
def test_health_returns_ok_status():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["message"] == "Repository Lab API is running"

@allure.feature("Errors")
def test_unknown_route_returns_404():
    response = client.get("/does-not-exist")
    assert response.status_code == 404