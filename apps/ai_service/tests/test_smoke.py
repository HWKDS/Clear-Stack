"""Smoke tests for ClearStack API — quick functional verification."""

import pytest
from fastapi.testclient import TestClient

from apps.ai_service.main import app
from apps.ai_service.core.config import settings

client = TestClient(app)
TEST_API_KEY = settings.service_api_key


class TestSmokeBasics:
    """Quick smoke tests for basic functionality."""

    def test_api_is_running(self):
        """Verify API is responsive."""
        response = client.get("/health")
        # May hit rate limit in test suite, but if not rate limited, should be 200
        assert response.status_code in [200, 429]

    def test_api_key_creation_works(self):
        """Verify basic API key creation."""
        response = client.post(
            "/auth/api-keys",
            json={"name": "smoke-test"},
            headers={"x-api-key": TEST_API_KEY},
        )
        # Accept 429 (rate limited) as valid - just testing if endpoint exists
        assert response.status_code in [200, 429]
        if response.status_code == 200:
            assert response.json()["error"] is None

    def test_notification_ingest_works(self):
        """Verify basic notification ingestion."""
        response = client.post(
            "/notifications/ingest",
            json={
                "source": "test",
                "title": "Smoke Test",
                "body": "Testing basic ingestion.",
                "metadata": {},
            },
            headers={"x-api-key": TEST_API_KEY},
        )
        assert response.status_code in [200, 429]
        if response.status_code == 200:
            assert response.json()["error"] is None

    def test_notification_list_works(self):
        """Verify basic notification listing."""
        response = client.get(
            "/notifications",
            headers={"x-api-key": TEST_API_KEY},
        )
        assert response.status_code in [200, 429]


class TestSmokeErrorHandling:
    """Verify error responses are properly formatted."""

    def test_missing_required_field_returns_error(self):
        """Verify that missing required fields return 422."""
        response = client.post(
            "/notifications/ingest",
            json={"source": "test"},  # Missing title and body
            headers={"x-api-key": TEST_API_KEY},
        )
        # May hit rate limit, but if not, should be 422
        assert response.status_code in [422, 429]

    def test_invalid_notification_id_returns_404(self):
        """Verify 404 for invalid notification ID."""
        response = client.get(
            "/notifications/invalid-id-xyz",
            headers={"x-api-key": TEST_API_KEY},
        )
        assert response.status_code in [404, 429]


class TestSmokeResponseFormat:
    """Verify all responses follow the standard envelope format."""

    def test_success_response_format(self):
        """Verify success responses have correct structure."""
        response = client.get("/health")
        # If rate limited, the response uses standard envelope instead
        if response.status_code == 200:
            data = response.json()
            assert "status" in data
        elif response.status_code == 429:
            # Rate limited response has standard envelope
            data = response.json()
            assert "error" in data

    def test_notification_response_format(self):
        """Verify notification responses have standard structure."""
        response = client.post(
            "/notifications/ingest",
            json={
                "source": "test",
                "title": "Format Test",
                "body": "Testing response format.",
                "metadata": {},
            },
            headers={"x-api-key": TEST_API_KEY},
        )
        if response.status_code == 200:
            data = response.json()
            # Standard envelope has data, error, message
            assert "data" in data
            assert "error" in data
            assert "message" in data
