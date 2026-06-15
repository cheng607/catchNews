from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["hot-items"])


@router.get("/hot-items")
async def list_hot_items(
    track: str = "all",
    time_range: str = "realtime",
    platform: str | None = None,
    top_n: int = 20,
    q: str | None = None,
    include_broken: bool = False,
) -> dict:
    """M0: 返回热点列表，后续接入 service 层。"""
    return {"items": [], "meta": {"updated_at": None, "platforms": {}}}
