import logging

from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CatchNews Pro API",
    version="0.1.0",
    docs_url="/docs",
)


@app.get("/api/v1/health")
async def health() -> dict:
    return {"status": "ok", "version": "0.1.0", "edition": "pro"}
