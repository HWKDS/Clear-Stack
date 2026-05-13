from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from apps.ai_service.core.config import settings
from apps.ai_service.core.response import error_response
from apps.ai_service.routers.auth import router as auth_router
from apps.ai_service.routers.digest import router as digest_router
from apps.ai_service.routers.generation import router as generation_router
from apps.ai_service.routers.integrations import router as integrations_router
from apps.ai_service.routers.notifications import router as notifications_router
from apps.ai_service.core.rate_limiter import RateLimitMiddleware


app = FastAPI(title=settings.app_name)

# Add rate limiting middleware early in the stack
app.add_middleware(RateLimitMiddleware)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    # Keep API errors in the standard response envelope.
    detail = exc.detail if isinstance(exc.detail, str) else "Request failed"
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(message=detail, error="http_error"),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=error_response(message="Unexpected server error", error="internal_error"),
    )


app.include_router(auth_router)
app.include_router(generation_router)
app.include_router(notifications_router)
app.include_router(digest_router)
app.include_router(integrations_router)
