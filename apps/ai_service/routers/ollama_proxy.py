from fastapi import APIRouter, Depends, HTTPException, Request
import httpx

from apps.ai_service.core.config import settings
from apps.ai_service.core.response import success_response
from apps.ai_service.core.security import require_api_key


router = APIRouter(prefix="/api/ollama", tags=["ollama"], dependencies=[Depends(require_api_key)])


@router.post("/generate")
async def generate_ollama(request: Request) -> dict:
    """Proxy endpoint that forwards prompt to a local Ollama server.

    Accepts either a JSON body `{ "prompt": "...", "model": "..." }`
    or a plain text body containing the prompt. This is a convenience fallback
    to make calling the endpoint from different shells easier.
    """
    prompt = None
    model = None

    # Try JSON first
    try:
        payload = await request.json()
        if isinstance(payload, dict):
            prompt = payload.get("prompt")
            model = payload.get("model")
    except Exception:
        # Not JSON — try plain text body
        raw = await request.body()
        try:
            prompt = raw.decode("utf-8").strip()
        except Exception:
            prompt = None

    if not prompt:
        raise HTTPException(status_code=422, detail="Missing prompt in request body")

    model = model or settings.local_model_name

    base_url = settings.ollama_base_url.rstrip("/")
    url = f"{base_url}/api/generate"
    params = {"model": model} if model else {}

    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            # If the client originally sent JSON, forward JSON to Ollama (preserving structure).
            # Otherwise send plain text content.
            try:
                # re-read JSON safely from request (if available)
                payload = await request.json()
                is_json = isinstance(payload, dict)
            except Exception:
                is_json = False

            if is_json:
                # Ensure model is present in the JSON payload we forward to Ollama.
                if isinstance(payload, dict):
                    if not payload.get("model"):
                        payload["model"] = model
                resp = await client.post(url, params=params, json=payload)
            else:
                # Ollama expects JSON; wrap plain-text prompt into a JSON body and include model.
                resp = await client.post(url, params=params, json={"prompt": prompt, "model": model})
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Failed to contact Ollama: {exc}") from exc

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Ollama error {resp.status_code}: {resp.text}")

    return success_response({"model": model, "text": resp.text}, message="Generated from Ollama")
