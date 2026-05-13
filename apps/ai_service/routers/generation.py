from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from apps.ai_service.core.response import success_response
from apps.ai_service.core.security import require_api_key
from apps.ai_service.services.model_client import generate_with_cloud_model, generate_with_local_model
from apps.ai_service.services.model_router import ModelRoute, route_prompt


router = APIRouter(prefix="", tags=["generation"], dependencies=[Depends(require_api_key)])


class RouteRequest(BaseModel):
    prompt: str = Field(min_length=1)
    sensitive_data: bool = False


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1)
    sensitive_data: bool = False


@router.post("/route")
async def choose_model(request: RouteRequest) -> dict:
    route = route_prompt(request.prompt, request.sensitive_data)
    return success_response(route.__dict__, message="Model route selected")


@router.post("/generate")
async def generate_text(request: GenerateRequest) -> dict:
    route = route_prompt(request.prompt, request.sensitive_data)
    try:
        if route.provider == "local":
            generated_text = generate_with_local_model(route.model_name, route.prompt)
        elif route.provider == "cloud":
            generated_text = generate_with_cloud_model(route.model_name, route.prompt)
        else:
            raise HTTPException(status_code=500, detail=f"Unsupported provider selected: {route.provider}")
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    response_data = {
        "provider": route.provider,
        "model_name": route.model_name,
        "prompt": route.prompt,
        "text": generated_text,
    }
    return success_response(response_data, message="Text generated")