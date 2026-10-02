from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_evaluate(monkeypatch):
    def fake_evaluation(scenario: str, answer: str):
        return {
            "critique": "Strong containerization plan, but observability is missing.",
            "improved_answer": "I would containerize the service and add monitoring."
        }

    monkeypatch.setattr(
        "app.main.run_interview_evaluation",
        fake_evaluation,
    )

    response = client.post(
        "/evaluate",
        json={
            "scenario": "Productionize an AI applcation.",
            "answer": "I would Dockerize it and deploy it."
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "critique" in body
    assert "improved_answer" in body


def test_evaluation_rejects_missing_answer():
    response = client.post(
        "/evaluate",
        json={
            "scenario": "Productionize an AI application."
        },
    )

    assert response.status_code == 422