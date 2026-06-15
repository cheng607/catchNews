from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.ingestion import run_all_collectors

router = APIRouter(prefix="/api/v1", tags=["refresh"])


@router.post("/refresh")
async def refresh_all(db: Session = Depends(get_db)) -> dict:
    results = await run_all_collectors(db)
    return {"status": "ok", "results": results}
