from datetime import UTC, datetime

from core.collectors.base import RawItem
from core.schemas.hot_item import HotItemSchema


def normalize(raw: RawItem, platform: str, track: str, source_label: str) -> HotItemSchema:
    """将采集器 RawItem 映射为统一 HotItemSchema。"""
    now = datetime.now(tz=UTC)
    item_id = f"{platform}:{raw.platform_item_id}"

    return HotItemSchema(
        id=item_id,
        platform=platform,
        track=track,
        title=raw.title,
        url=raw.url,
        rank=raw.rank,
        heat_score=raw.heat_score,
        metrics=raw.metrics,
        rank_change=None,
        captured_at=now,
        first_seen_at=now,
        link_status="ok",
        source_label=source_label,
    )
