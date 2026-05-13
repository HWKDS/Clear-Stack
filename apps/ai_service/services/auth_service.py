"""Authentication service for API key and token management."""

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Optional

import jwt

from apps.ai_service.core.config import settings
from apps.ai_service.models.auth import APIKey
from apps.ai_service.repositories.api_key_repository import sql_api_key_repository


class AuthService:
    """Manage API keys and JWT tokens for authentication."""

    def __init__(self, repository=None):
        self.repository = repository or sql_api_key_repository
        self.jwt_secret = settings.service_api_key  # Use service API key as JWT secret
        self.token_expiry_seconds = 3600  # 1 hour token expiry

    def generate_api_key(self) -> str:
        """Generate a new secure API key."""
        # Generate 32 random bytes and encode as hex
        return secrets.token_urlsafe(32)

    def hash_api_key(self, key: str) -> str:
        """Hash an API key using HMAC-SHA256."""
        return hmac.new(
            self.jwt_secret.encode(),
            key.encode(),
            hashlib.sha256
        ).hexdigest()

    def create_api_key(
        self,
        name: str,
        user_id: Optional[str] = None,
        expires_in_days: Optional[int] = None,
    ) -> tuple[str, APIKey]:
        """
        Create a new API key.
        
        Returns:
            Tuple of (plain_key, stored_record)
            The plain key should be shown to the user only once.
        """
        plain_key = self.generate_api_key()
        hashed_key = self.hash_api_key(plain_key)
        
        expires_at = None
        if expires_in_days:
            expires_at = datetime.now(UTC) + timedelta(days=expires_in_days)
        
        stored_record = self.repository.create(
            key=hashed_key,
            name=name,
            user_id=user_id,
            expires_at=expires_at,
        )
        
        return plain_key, stored_record

    def validate_api_key(self, key: str) -> Optional[APIKey]:
        """
        Validate an API key and return the record if valid.
        
        Returns None if invalid, expired, or inactive.
        """
        hashed_key = self.hash_api_key(key)
        api_key = self.repository.get_by_key(hashed_key)
        
        if not api_key:
            return None
        
        # Check if active
        if not api_key.is_active:
            return None
        
        # Check if expired
        if api_key.expires_at:
            # Ensure both datetimes are timezone-aware for comparison
            expires_at = api_key.expires_at
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=UTC)
            if datetime.now(UTC) > expires_at:
                return None
        
        # Update last used
        self.repository.update_last_used(api_key.id)
        
        return api_key

    def issue_token(self, api_key: APIKey) -> str:
        """Issue a JWT token for an API key."""
        payload = {
            "sub": api_key.id,
            "key_name": api_key.name,
            "user_id": api_key.user_id,
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(seconds=self.token_expiry_seconds),
        }
        
        token = jwt.encode(
            payload,
            self.jwt_secret,
            algorithm="HS256"
        )
        
        return token

    def verify_token(self, token: str) -> Optional[dict]:
        """Verify a JWT token and return the payload."""
        try:
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=["HS256"]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke an API key."""
        return self.repository.revoke(key_id)

    def list_api_keys(self, user_id: Optional[str] = None) -> list[APIKey]:
        """List all API keys for a user."""
        return self.repository.list_by_user(user_id)


# Singleton instance for use throughout the app
auth_service = AuthService()
