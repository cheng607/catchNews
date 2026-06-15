"""个人版 GitHub Star 指标服务 — 封装 core 层并注入本地配置。"""

from app.config import settings
from core.collectors.github_stars import fetch_repo_stars as _core_fetch
from core.collectors.github_stars import parse_github_repo

__all__ = ["fetch_repo_stars", "parse_github_repo"]


async def fetch_repo_stars(owner: str, repo: str) -> dict[str, int | str] | None:
    return await _core_fetch(owner, repo, token=settings.github_token)
