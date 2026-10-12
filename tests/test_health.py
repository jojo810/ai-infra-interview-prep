from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_config_check():
    response = client.get("/config-check")

    assert response.status_code == 200

    body = response.json()

    assert "openai_configured" in body
    assert "model" in body
    assert isinstance(body["openai_configured"], bool)