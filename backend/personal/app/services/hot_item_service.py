from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.models.base import HotItem, PlatformHealth
from core.schemas.hot_item import HotItemSchema, HotItemsResponse, PlatformStatus, RankChange

TRACK_MAP = {
    "all": None,
    "entertainment": "entertainment",
    "tech": "tech",
    "news": "news",
}


def _to_schema(item: HotItem, source_label: str) -> HotItemSchema:
    metrics = item.metrics if isinstance(item.metrics, dict) else {}
    rank_change = None
    if isinstance(metrics.get("rank_change"), dict):
        rank_change = RankChange(**metrics["rank_change"])
    return HotItemSchema(
        id=item.id,
        platform=item.platform,
        track=item.track,  # type: ignore[arg-type]
        title=item.title,
        url=item.url,
        rank=item.rank,
        heat_score=item.heat_score,
        metrics=metrics,
        rank_change=rank_change,
        captured_at=item.captured_at,
        first_seen_at=item.first_seen_at,
        link_status=item.link_status,
        source_label=source_label,
    )


def _source_label(platform: str) -> str:
    labels = {
        "github": "GitHub Trending",
        "weibo": "微博热搜",
        "baidu": "百度热搜",
        "zhihu": "知乎热榜",
    }
    return labels.get(platform, platform)


def list_hot_items(
    db: Session,
    *,
    track: str = "all",
    platform: str | None = None,
    top_n: int = 20,
    q: str | None = None,
    include_broken: bool = False,
    time_range: str = "realtime",
) -> HotItemsResponse:
    stmt = select(HotItem).where(HotItem.is_active.is_(True))
    track_value = TRACK_MAP.get(track, track)
    if track_value:
        stmt = stmt.where(HotItem.track == track_value)
    if platform:
        platforms = [p.strip() for p in platform.split(",") if p.strip()]
        if platforms:
            stmt = stmt.where(HotItem.platform.in_(platforms))
    if not include_broken:
        stmt = stmt.where(HotItem.link_status == "ok")

    stmt = stmt.order_by(HotItem.rank.asc().nullslast(), HotItem.captured_at.desc())
    items = db.execute(stmt).scalars().all()

    schemas = [_to_schema(item, _source_label(item.platform)) for item in items]

    if time_range == "realtime":
        schemas = [
            s
            for s in schemas
            if s.platform != "github" or s.metrics.get("since") == "daily"
        ]
    elif time_range == "week":
        schemas = [
            s
            for s in schemas
            if s.platform != "github" or s.metrics.get("since") == "weekly"
        ]

    if q:
        keyword = q.lower()
        schemas = [s for s in schemas if keyword in s.title.lower()]

    schemas = schemas[: min(top_n, 50)]

    health_rows = db.execute(select(PlatformHealth)).scalars().all()
    platforms_meta: dict[str, PlatformStatus] = {}
    updated_at: datetime | None = None
    for row in health_rows:
        platforms_meta[row.platform] = PlatformStatus(
            status=row.status,
            updated_at=row.last_success_at,
            last_error=row.last_error,
        )
        if row.last_success_at and (updated_at is None or row.last_success_at > updated_at):
            updated_at = row.last_success_at

    if updated_at is None:
        updated_at = datetime.now(tz=UTC)

    return HotItemsResponse(
        items=schemas,
        meta={
            "updated_at": updated_at.isoformat(),
            "platforms": {k: v.model_dump(mode="json") for k, v in platforms_meta.items()},
        },
    )
