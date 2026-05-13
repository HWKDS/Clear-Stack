from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField


class APIKey(SQLModel, table=True):
    """Database model for API keys."""
    id: str = SQLField(default_factory=lambda: str(uuid4()), primary_key=True)
    key: str = SQLField(unique=True, index=True)  # Hashed API key
    user_id: str | None = None  # Optional user identifier (could be email or UUID)
    name: str  # Friendly name for the key (e.g., "mobile app", "prod server")
    is_active: bool = SQLField(default=True)
    created_at: datetime = SQLField(default_factory=lambda: datetime.now(UTC))
    last_used_at: datetime | None = None
    expires_at: datetime | None = None  # Optional expiration


class APIKeyCreateRequest(BaseModel):
    """Request to create a new API key."""
    name: str = Field(min_length=1, max_length=100)
    user_id: str | None = None
    expires_in_days: int | None = Field(default=None, ge=1, le=365)


class APIKeyResponse(BaseModel):
    """Response when creating an API key (includes plain key for one-time display)."""
    id: str
    key: str  # Only shown once during creation
    name: str
    created_at: datetime


class APIKeyListItem(BaseModel):
    """Response for listing API keys (no plain key exposed)."""
    id: str
    name: str
    is_active: bool
    created_at: datetime
    last_used_at: datetime | None
    expires_at: datetime | None


class APIKeyRevokeRequest(BaseModel):
    """Request to revoke an API key."""
    key_id: str


class TokenResponse(BaseModel):
    """JWT token response for API access."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # Seconds
