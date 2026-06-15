import logging
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.services.github_stars import fetch_repo_stars, parse_github_repo
from core.collectors.base import BaseCollector, RawItem
from core.collectors.github_trending import GitHubTrendingCollector
from core.link_validator import is_allowed_url
from core.models.base import HotItem, HotSnapshot, PlatformHealth
from core.normalizer import normalize
from core.schemas.hot_item import RankChange

logger = logging.getLogger(__name__)

SOURCE_LABELS = {
    "github": "GitHub Trending",
    "weibo": "微博热搜",
    "baidu": "百度热搜",
    "zhihu": "知乎热榜",
}


def _utcnow() -> datetime:
    return datetime.now(tz=UTC)


def _compute_rank_change(previous_rank: int | None, current_rank: int | None) -> RankChange | None:
    if current_rank is None:
        return None
    if previous_rank is None:
        return RankChange(type="new")
    delta = current_rank - previous_rank
    if delta == 0:
        return RankChange(type="flat")
    if delta < 0:
        return RankChange(type="up", value=abs(delta))
    return RankChange(type="down", value=delta)


async def _enrich_github_metrics(raw: RawItem) -> RawItem:
    parsed = parse_github_repo(raw.url)
    if parsed is None:
        return raw
    owner, repo = parsed
    api_metrics = await fetch_repo_stars(owner, repo)
    if api_metrics is None:
        return raw
    metrics = dict(raw.metrics)
    metrics.update(api_metrics)
    raw.metrics = metrics
    raw.heat_score = float(api_metrics["stars"])
    return raw


async def _ingest_collector(db: Session, collector: BaseCollector) -> int:
    platform = collector.platform
    try:
        raw_items = await collector.fetch()
        now = _utcnow()
        count = 0
        snapshot_payload: list[dict] = []

        for raw in raw_items:
            if not is_allowed_url(raw.url):
                continue
            if platform == "github":
                raw = await _enrich_github_metrics(raw)

            normalized = normalize(
                raw,
                platform=platform,
                track=collector.track,
                source_label=SOURCE_LABELS.get(platform, platform),
            )

            existing = db.get(HotItem, normalized.id)
            previous_rank = existing.rank if existing else None
            rank_change = _compute_rank_change(previous_rank, normalized.rank)

            stars_total = int(raw.metrics.get("stars", 0) or 0)
            stars_prev = 0
            if existing and isinstance(existing.metrics, dict):
                stars_prev = int(existing.metrics.get("stars", 0) or 0)
            stars_delta = stars_total - stars_prev if stars_total and stars_prev else 0

            metrics = dict(normalized.metrics)
            if platform == "github" and stars_total:
                metrics["stars"] = stars_total
                metrics["stars_today"] = max(stars_delta, 0) if stars_prev else 0
                if existing and isinstance(existing.metrics, dict):
                    metrics["stars_delta_7d"] = existing.metrics.get("stars_delta_7d", 0)
            if rank_change is not None:
                metrics["rank_change"] = rank_change.model_dump()

            schema = normalized.model_copy(
                update={
                    "metrics": metrics,
                    "rank_change": rank_change,
                    "first_seen_at": existing.first_seen_at if existing else now,
                    "captured_at": now,
                }
            )

            if existing is None:
                db.add(
                    HotItem(
                        id=schema.id,
                        platform=schema.platform,
                        track=schema.track,
                        title=schema.title,
                        url=schema.url,
                        rank=schema.rank,
                        heat_score=schema.heat_score,
                        metrics=schema.metrics,
                        captured_at=schema.captured_at,
                        first_seen_at=schema.first_seen_at,
                        link_status=schema.link_status,
                        is_active=True,
                    )
                )
            else:
                existing.title = schema.title
                existing.url = schema.url
                existing.rank = schema.rank
                existing.heat_score = schema.heat_score
                existing.metrics = schema.metrics
                existing.captured_at = schema.captured_at
                existing.is_active = True
                existing.link_status = schema.link_status

            snapshot_payload.append(schema.model_dump(mode="json"))
            count += 1

        db.add(
            HotSnapshot(
                platform=platform,
                snapshot_at=now,
                payload=snapshot_payload,
            )
        )

        health = db.get(PlatformHealth, platform)
        if health is None:
            health = PlatformHealth(platform=platform)
            db.add(health)
        health.last_success_at = now
        health.last_error = None
        health.status = "ok" if count else "degraded"

        db.commit()
        logger.info("Ingested %s items from %s", count, platform)
        return count
    except Exception as exc:
        db.rollback()
        logger.exception("Collector %s failed: %s", platform, exc)
        health = db.get(PlatformHealth, platform)
        if health is None:
            health = PlatformHealth(platform=platform)
            db.add(health)
        health.status = "error"
        health.last_error = str(exc)
        db.commit()
        return 0


async def run_github_trending_ingestion(db: Session, since: str = "daily") -> int:
    collector = GitHubTrendingCollector(since=since)  # type: ignore[arg-type]
    return await _ingest_collector(db, collector)


async def run_all_collectors(db: Session) -> dict[str, int]:
    results = {}
    results["github_daily"] = await run_github_trending_ingestion(db, since="daily")
    results["github_weekly"] = await run_github_trending_ingestion(db, since="weekly")
    return results
