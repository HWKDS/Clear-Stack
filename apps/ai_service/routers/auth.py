"""Authentication endpoints for API key and token management."""

from fastapi import APIRouter, Depends, HTTPException, status

from apps.ai_service.core.security import require_api_key
from apps.ai_service.models.auth import (
    APIKeyCreateRequest,
    APIKeyListItem,
    APIKeyResponse,
    APIKeyRevokeRequest,
    TokenResponse,
)
from apps.ai_service.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"], dependencies=[Depends(require_api_key)])


@router.post("/api-keys", response_model=dict)
async def create_api_key(request: APIKeyCreateRequest) -> dict:
    """
    Create a new API key.
    
    Requires valid API key in header (x-api-key).
    """
    try:
        plain_key, record = auth_service.create_api_key(
            name=request.name,
            user_id=request.user_id,
            expires_in_days=request.expires_in_days,
        )
        
        response_data = APIKeyResponse(
            id=record.id,
            key=plain_key,  # Only shown once
            name=record.name,
            created_at=record.created_at,
        )
        
        return {
            "data": response_data.model_dump(),
            "error": None,
            "message": "API key created successfully. Store this key securely; it cannot be retrieved later.",
        }
    except Exception as e:
        return {
            "data": None,
            "error": str(e),
            "message": "Failed to create API key",
        }


@router.get("/api-keys", response_model=dict)
async def list_api_keys(user_id: str | None = None) -> dict:
    """
    List all API keys for a user.
    
    Requires valid API key in header (x-api-key).
    """
    try:
        keys = auth_service.list_api_keys(user_id=user_id)
        
        items = [
            APIKeyListItem(
                id=key.id,
                name=key.name,
                is_active=key.is_active,
                created_at=key.created_at,
                last_used_at=key.last_used_at,
                expires_at=key.expires_at,
            )
            for key in keys
        ]
        
        return {
            "data": [item.model_dump() for item in items],
            "error": None,
            "message": f"Retrieved {len(items)} API key(s)",
        }
    except Exception as e:
        return {
            "data": None,
            "error": str(e),
            "message": "Failed to list API keys",
        }


@router.post("/api-keys/{key_id}/revoke", response_model=dict)
async def revoke_api_key(key_id: str) -> dict:
    """
    Revoke an API key by ID.
    
    Requires valid API key in header (x-api-key).
    """
    try:
        success = auth_service.revoke_api_key(key_id)
        
        if not success:
            return {
                "data": None,
                "error": "Not found",
                "message": "API key not found",
            }
        
        return {
            "data": {"key_id": key_id, "is_active": False},
            "error": None,
            "message": "API key revoked successfully",
        }
    except Exception as e:
        return {
            "data": None,
            "error": str(e),
            "message": "Failed to revoke API key",
        }


@router.post("/token", response_model=dict)
async def issue_token(request: APIKeyCreateRequest) -> dict:
    """
    Issue a JWT token using an API key.
    
    Note: For testing/development. In production, pass the plain API key here.
    """
    try:
        # In a real app, the client would send their plain API key
        # and we'd validate it, then issue a JWT token.
        # For now, this is a placeholder.
        return {
            "data": None,
            "error": "Not implemented",
            "message": "Token endpoint requires API key in body (not yet implemented)",
        }
    except Exception as e:
        return {
            "data": None,
            "error": str(e),
            "message": "Failed to issue token",
        }
