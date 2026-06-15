import asyncio
import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.api.hot_items import router as hot_items_router
from app.api.refresh import router as refresh_router
from app.config import settings
from app.database import SessionLocal, init_db
from app.scheduler import register_jobs
from app.services.ingestion import run_all_collectors
from core.models.base import PlatformHealth
from core.schemas.hot_item import PlatformStatus

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def _bootstrap_collect() -> None:
    db = SessionLocal()
    try:
        await run_all_collectors(db)
    except Exception:
        logger.exception("Bootstrap collection failed")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    init_db()
    register_jobs(scheduler)
    scheduler.start()
    app.state.bootstrap_task = asyncio.create_task(_bootstrap_collect())
    logger.info("CatchNews Personal API started")
    yield
    scheduler.shutdown(wait=False)
    logger.info("CatchNews Personal API stopped")


app = FastAPI(
    title="CatchNews Personal API",
    version="0.1.0",
    docs_url="/docs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hot_items_router)
app.include_router(refresh_router)


@app.get("/api/v1/health")
async def health() -> dict:
    db = SessionLocal()
    try:
        rows = db.execute(select(PlatformHealth)).scalars().all()
        platforms = {
            row.platform: PlatformStatus(
                status=row.status,
                updated_at=row.last_success_at,
                last_error=row.last_error,
            ).model_dump(mode="json")
            for row in rows
        }
    finally:
        db.close()

    return {
        "status": "ok",
        "version": "0.1.0",
        "edition": "personal",
        "platforms": platforms,
    }
