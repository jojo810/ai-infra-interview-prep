from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_scenario(monkeypatch):
    def fake_scenario():
        return "Design a production-ready AI service."

    monkeypatch.setattr(
        "app.main.generate_interview_scenario",
        fake_scenario,
    )

    response = client.get("/scenario")

    assert response.status_code == 200
    assert response.json() == {
        "scenario": "Design a production-ready AI service."
    }