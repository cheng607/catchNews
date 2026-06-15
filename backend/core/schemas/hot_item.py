from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

Track = Literal["entertainment", "tech", "news"]
RankChangeType = Literal["up", "down", "new", "flat"]


class RankChange(BaseModel):
    type: RankChangeType
    value: int | None = None


class HotItemSchema(BaseModel):
    id: str
    platform: str
    track: Track
    title: str
    url: str
    rank: int | None = None
    heat_score: float | None = None
    metrics: dict[str, Any] = Field(default_factory=dict)
    rank_change: RankChange | None = None
    captured_at: datetime
    first_seen_at: datetime
    link_status: str = "ok"
    source_label: str


class PlatformStatus(BaseModel):
    status: str
    updated_at: datetime | None = None
    last_error: str | None = None


class HotItemsResponse(BaseModel):
    items: list[HotItemSchema]
    meta: dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    version: str
    platforms: dict[str, PlatformStatus]
