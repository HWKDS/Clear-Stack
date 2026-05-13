from fastapi import APIRouter, Depends
from pydantic import BaseModel

from apps.ai_service.core.response import success_response
from apps.ai_service.core.security import require_api_key


router = APIRouter(prefix="/integrations", tags=["integrations"], dependencies=[Depends(require_api_key)])


class IntegrationConnectRequest(BaseModel):
    account_identifier: str


AVAILABLE_INTEGRATIONS = [
    {"provider": "gmail", "status": "available"},
    {"provider": "google_calendar", "status": "available"},
    {"provider": "whatsapp", "status": "planned"},
    {"provider": "linkedin", "status": "planned"},
]


@router.get("")
async def list_integrations() -> dict:
    return success_response(AVAILABLE_INTEGRATIONS, message="Integrations listed")


@router.post("/{provider}/connect")
async def connect_integration(provider: str, payload: IntegrationConnectRequest) -> dict:
    # This is a safe placeholder while OAuth flow is being implemented.
    integration = {
        "provider": provider,
        "account_identifier": payload.account_identifier,
        "status": "connected_stub",
    }
    return success_response(integration, message="Integration connection simulated")