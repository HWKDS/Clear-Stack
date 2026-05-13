from fastapi import APIRouter, Depends, HTTPException, Query

from apps.ai_service.core.response import success_response
from apps.ai_service.core.security import require_api_key
from apps.ai_service.models.notification import NotificationIn
from apps.ai_service.services.notification_service import notification_service


router = APIRouter(prefix="/notifications", tags=["notifications"], dependencies=[Depends(require_api_key)])


@router.post("/ingest")
async def ingest_notification(payload: NotificationIn) -> dict:
    created = notification_service.ingest(payload)
    return success_response(created.model_dump(), message="Notification ingested")


@router.get("")
async def list_notifications(
    source: str | None = Query(default=None),
    min_priority: int | None = Query(default=None, ge=0, le=100),
) -> dict:
    notifications = notification_service.list_notifications(source=source, min_priority=min_priority)
    data = [item.model_dump() for item in notifications]
    return success_response(data, message="Notifications fetched")


@router.get("/{notification_id}")
async def get_notification(notification_id: str) -> dict:
    record = notification_service.get_notification(notification_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return success_response(record.model_dump(), message="Notification fetched")