from typing import Any


def success_response(data: Any, message: str = "Success") -> dict[str, Any]:
    # Keep a consistent response contract across all endpoints.
    return {"data": data, "error": None, "message": message}


def error_response(message: str, error: str) -> dict[str, Any]:
    return {"data": None, "error": error, "message": message}