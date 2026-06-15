from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.hot_item_service import list_hot_items
from core.schemas.hot_item import HotItemsResponse

router = APIRouter(prefix="/api/v1", tags=["hot-items"])


@router.get("/hot-items", response_model=HotItemsResponse)
async def get_hot_items(
    track: str = Query("all"),
    time_range: str = Query("realtime"),
    platform: str | None = None,
    top_n: int = Query(20, ge=1, le=50),
    q: str | None = None,
    include_broken: bool = False,
    db: Session = Depends(get_db),
) -> HotItemsResponse:
    _ = time_range  # today/week aggregation in later milestones
    return list_hot_items(
        db,
        track=track,
        platform=platform,
        top_n=top_n,
        q=q,
        include_broken=include_broken,
    )
