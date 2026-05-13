from fastapi import APIRouter, Depends

from apps.ai_service.core.response import success_response
from apps.ai_service.core.security import require_api_key
from apps.ai_service.models.digest import DigestRequest
from apps.ai_service.services.digest_service import build_digest
from apps.ai_service.services.notification_service import notification_service


router = APIRouter(prefix="/digest", tags=["digest"], dependencies=[Depends(require_api_key)])


@router.post("/daily")
async def generate_daily_digest(payload: DigestRequest) -> dict:
    notifications = notification_service.list_notifications()
    digest = build_digest(notifications, limit=payload.limit)
    return success_response(digest.model_dump(), message="Digest generated")