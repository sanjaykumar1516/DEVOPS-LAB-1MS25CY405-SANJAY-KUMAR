
from fastapi.testclient import TestClient
from security_log_api.main import app, events, alerts, failed_attempts

client = TestClient(app)


def setup_function():
    events.clear()
    alerts.clear()
    failed_attempts.clear()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_failed_login_creates_alert():
    for i in range(5):
        response = client.post(
            "/events",
            json={
                "source_ip": "192.168.1.50",
                "username": "admin",
                "event_type": "failed_login"
            }
        )
        assert response.status_code == 200

    response = client.get("/alerts")
    assert response.json()["total_alerts"] == 1


def test_invalid_ip_rejected():
    response = client.post(
        "/events",
        json={
            "source_ip": "not-an-ip",
            "username": "admin",
            "event_type": "failed_login"
        }
    )

    assert response.status_code == 400
