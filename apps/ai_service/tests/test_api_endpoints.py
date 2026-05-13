from fastapi.testclient import TestClient

from apps.ai_service.core.config import settings
from apps.ai_service.main import app
from apps.ai_service.services.notification_service import notification_repository


client = TestClient(app)


def _headers() -> dict[str, str]:
    if settings.service_api_key:
        return {"x-api-key": settings.service_api_key}
    return {}


def setup_function() -> None:
    # Keep tests isolated from each other.
    notification_repository.replace_all([])


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ingest_and_list_notifications() -> None:
    ingest_response = client.post(
        "/notifications/ingest",
        headers=_headers(),
        json={
            "source": "gmail",
            "title": "Urgent meeting update",
            "body": "Email me at jane.doe@example.com with details.",
            "sensitive_data": True,
            "metadata": {"thread_id": "abc123"},
        },
    )
    assert ingest_response.status_code == 200

    created = ingest_response.json()["data"]
    assert created["source"] == "gmail"
    assert "[REDACTED_EMAIL]" in created["body"]
    assert created["priority_score"] >= 20

    list_response = client.get("/notifications", headers=_headers())
    assert list_response.status_code == 200
    listed = list_response.json()["data"]
    assert len(listed) == 1
    assert listed[0]["id"] == created["id"]


def test_generate_digest() -> None:
    client.post(
        "/notifications/ingest",
        headers=_headers(),
        json={
            "source": "gmail",
            "title": "Deadline tomorrow",
            "body": "Project deadline is tomorrow at 10am.",
            "sensitive_data": False,
            "metadata": {},
        },
    )

    digest_response = client.post("/digest/daily", headers=_headers(), json={"limit": 10})
    assert digest_response.status_code == 200

    digest_data = digest_response.json()["data"]
    assert digest_data["total_notifications"] == 1
    assert len(digest_data["items"]) == 1
    assert digest_data["items"][0]["source"] == "gmail"


def test_generate_uses_local_model_path(monkeypatch) -> None:
    monkeypatch.setattr(settings, "model_provider", "local")

    def _fake_local_generate(model_name: str, prompt: str) -> str:
        return f"local:{model_name}:{prompt[:10]}"

    monkeypatch.setattr("apps.ai_service.routers.generation.generate_with_local_model", _fake_local_generate)

    response = client.post(
        "/generate",
        headers=_headers(),
        json={"prompt": "Summarize this message", "sensitive_data": False},
    )

    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["provider"] == "local"
    assert payload["text"].startswith("local:")


def test_api_key_required_when_configured(monkeypatch) -> None:
    monkeypatch.setattr(settings, "service_api_key", "secret-key")

    unauthorized = client.get("/notifications")
    assert unauthorized.status_code == 401

    authorized = client.get("/notifications", headers={"x-api-key": "secret-key"})
    assert authorized.status_code == 200

    monkeypatch.setattr(settings, "service_api_key", "")