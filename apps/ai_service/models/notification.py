from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField
from sqlalchemy import Column
from sqlalchemy import JSON as SAJSON


class NotificationIn(BaseModel):
    source: str = Field(min_length=1, max_length=50)
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)
    sensitive_data: bool = False


class NotificationRecord(SQLModel, table=True):
    id: str = SQLField(default_factory=lambda: str(uuid4()), primary_key=True)
    source: str
    title: str
    body: str
    summary: str
    priority_score: int
    meta: dict[str, Any] = SQLField(default_factory=dict, sa_column=Column(SAJSON))
    created_at: datetime = SQLField(default_factory=lambda: datetime.now(UTC))


class NotificationListFilters(BaseModel):
    source: str | None = None
    min_priority: int | None = Field(default=None, ge=0, le=100)