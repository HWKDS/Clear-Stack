import json
from urllib import error

import pytest

from apps.ai_service.core.config import settings
from apps.ai_service.services.model_client import generate_with_cloud_model


class _FakeHttpResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_cloud_generation_returns_text(monkeypatch) -> None:
    monkeypatch.setattr(settings, "cloud_api_key", "dummy-key")

    def _fake_urlopen(_request, timeout):
        assert timeout == settings.request_timeout_seconds
        return _FakeHttpResponse({"choices": [{"message": {"content": "Cloud answer"}}]})

    monkeypatch.setattr("apps.ai_service.services.model_client.request.urlopen", _fake_urlopen)

    output = generate_with_cloud_model("gpt-4o-mini", "Say hello")
    assert output == "Cloud answer"


def test_cloud_generation_requires_api_key(monkeypatch) -> None:
    monkeypatch.setattr(settings, "cloud_api_key", "")

    with pytest.raises(RuntimeError, match="CLOUD_API_KEY is missing"):
        generate_with_cloud_model("gpt-4o-mini", "Say hello")


def test_cloud_generation_handles_network_failure(monkeypatch) -> None:
    monkeypatch.setattr(settings, "cloud_api_key", "dummy-key")

    def _fake_urlopen(_request, timeout):
        raise error.URLError("network unavailable")

    monkeypatch.setattr("apps.ai_service.services.model_client.request.urlopen", _fake_urlopen)

    with pytest.raises(RuntimeError, match="Could not reach cloud model provider"):
        generate_with_cloud_model("gpt-4o-mini", "Say hello")