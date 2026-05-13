from datetime import datetime

from pydantic import BaseModel, Field


class DigestRequest(BaseModel):
    # Defaults to the latest notifications and can be tuned by callers.
    limit: int = Field(default=20, ge=1, le=200)


class DigestItem(BaseModel):
    source: str
    count: int
    top_priority: int


class DigestResponse(BaseModel):
    generated_at: datetime
    total_notifications: int
    average_priority: float
    items: list[DigestItem]
    highlights: list[str]