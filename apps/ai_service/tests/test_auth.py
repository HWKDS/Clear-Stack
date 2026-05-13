"""Tests for auth endpoints and service."""

import pytest
from fastapi.testclient import TestClient

from apps.ai_service.main import app
from apps.ai_service.services.auth_service import auth_service

client = TestClient(app)


@pytest.fixture
def test_api_key():
    """Fixture to provide a valid test API key."""
    # Use the service API key from config for testing
    from apps.ai_service.core.config import settings
    return settings.service_api_key


class TestAuthService:
    """Test authentication service logic."""

    def test_generate_api_key(self):
        """Test API key generation."""
        key = auth_service.generate_api_key()
        assert key
        assert len(key) > 20  # urlsafe tokens are reasonably long

    def test_hash_api_key(self):
        """Test API key hashing."""
        key = "test-key-12345"
        hashed = auth_service.hash_api_key(key)
        assert hashed
        assert hashed != key  # Should be different from plain key
        assert len(hashed) == 64  # SHA256 hex is 64 chars

    def test_create_api_key(self):
        """Test API key creation and storage."""
        plain_key, record = auth_service.create_api_key(
            name="test-key",
            user_id="user123",
        )
        assert plain_key
        assert record.id
        assert record.name == "test-key"
        assert record.user_id == "user123"
        assert record.is_active is True

    def test_validate_api_key(self):
        """Test API key validation."""
        plain_key, _ = auth_service.create_api_key(name="validate-test")
        
        # Should validate successfully
        result = auth_service.validate_api_key(plain_key)
        assert result is not None
        assert result.name == "validate-test"

    def test_validate_invalid_key(self):
        """Test validation with invalid key."""
        result = auth_service.validate_api_key("invalid-key-xyz")
        assert result is None

    def test_revoke_api_key(self):
        """Test API key revocation."""
        _, record = auth_service.create_api_key(name="revoke-test")
        
        # Should revoke successfully
        success = auth_service.revoke_api_key(record.id)
        assert success is True

    def test_issue_token(self):
        """Test JWT token issuance."""
        _, record = auth_service.create_api_key(name="token-test")
        token = auth_service.issue_token(record)
        assert token
        assert isinstance(token, str)

    def test_verify_token(self):
        """Test JWT token verification."""
        _, record = auth_service.create_api_key(name="verify-test")
        token = auth_service.issue_token(record)
        
        # Should verify successfully
        payload = auth_service.verify_token(token)
        assert payload is not None
        assert payload["sub"] == record.id
        assert payload["key_name"] == "verify-test"

    def test_verify_invalid_token(self):
        """Test verification with invalid token."""
        result = auth_service.verify_token("invalid.token.here")
        assert result is None


class TestAuthEndpoints:
    """Test auth API endpoints."""

    def test_create_api_key_endpoint(self, test_api_key):
        """Test POST /auth/api-keys endpoint."""
        response = client.post(
            "/auth/api-keys",
            json={"name": "endpoint-test"},
            headers={"x-api-key": test_api_key},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["error"] is None
        assert data["data"]["name"] == "endpoint-test"
        assert "key" in data["data"]  # Plain key should be in response

    def test_create_api_key_without_auth(self):
        """Test that endpoint works in dev mode without auth (when no service_api_key is set)."""
        # In development, when service_api_key is not set, the endpoint is accessible
        response = client.post(
            "/auth/api-keys",
            json={"name": "no-auth-test"},
        )
        # In dev mode, this is allowed (lenient for development)
        assert response.status_code == 200

    def test_list_api_keys_endpoint(self, test_api_key):
        """Test GET /auth/api-keys endpoint."""
        response = client.get(
            "/auth/api-keys",
            headers={"x-api-key": test_api_key},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["error"] is None
        assert isinstance(data["data"], list)

    def test_revoke_api_key_endpoint(self, test_api_key):
        """Test POST /auth/api-keys/{key_id}/revoke endpoint."""
        # First create a key
        create_response = client.post(
            "/auth/api-keys",
            json={"name": "revoke-endpoint-test"},
            headers={"x-api-key": test_api_key},
        )
        key_id = create_response.json()["data"]["id"]
        
        # Then revoke it
        revoke_response = client.post(
            f"/auth/api-keys/{key_id}/revoke",
            headers={"x-api-key": test_api_key},
        )
        assert revoke_response.status_code == 200
        data = revoke_response.json()
        assert data["error"] is None
        assert data["data"]["is_active"] is False

    def test_revoke_nonexistent_key(self, test_api_key):
        """Test revoking a key that doesn't exist."""
        response = client.post(
            "/auth/api-keys/nonexistent-id/revoke",
            headers={"x-api-key": test_api_key},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["error"] == "Not found"
