import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import settings
from app.database import SessionLocal
from app.services.ingestion import run_all_collectors

logger = logging.getLogger(__name__)


async def _scheduled_collect() -> None:
    db = SessionLocal()
    try:
        await run_all_collectors(db)
    finally:
        db.close()


def register_jobs(scheduler: AsyncIOScheduler) -> None:
    scheduler.add_job(
        _scheduled_collect,
        "interval",
        minutes=settings.refresh_interval_github,
        id="github_trending_collect",
        replace_existing=True,
        max_instances=1,
    )
    logger.info(
        "Scheduler registered — github interval: %dm, entertainment interval: %dm (M1)",
        settings.refresh_interval_github,
        settings.refresh_interval_entertainment,
    )
