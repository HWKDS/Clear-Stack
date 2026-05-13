from fastapi import Header, HTTPException

from apps.ai_service.core.config import settings


async def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    # If SERVICE_API_KEY is not configured, keep local development friction low.
    if not settings.service_api_key:
        return

    if x_api_key != settings.service_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")