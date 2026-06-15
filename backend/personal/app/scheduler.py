import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import settings

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def init_scheduler() -> None:
    """注册所有采集定时任务。M0 阶段先预留框架，后续里程碑逐步添加 job。"""
    logger.info(
        "Scheduler initialized — entertainment: %dm, github: %dm",
        settings.refresh_interval_entertainment,
        settings.refresh_interval_github,
    )
