import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CatchNews Personal API",
    version="0.1.0",
    docs_url="/docs",
    root_path="",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    logger.info("Initializing database...")
    init_db()
    logger.info("CatchNews Personal API started")


@app.get("/api/v1/health")
async def health() -> dict:
    return {"status": "ok", "version": "0.1.0", "edition": "personal"}
