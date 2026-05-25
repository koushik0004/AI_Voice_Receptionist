from fastapi.testclient import TestClient

from app.main import app


def test_root_serves_test_console() -> None:
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert "AI Voice Receptionist MVP" in response.text
    assert "Call Simulator" in response.text


def test_health_endpoint() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
