"""GitHub Star 指标富化模块。

与 GitHubTrendingCollector 配合使用: Trending 采集器获取基础列表,
本模块通过 GitHub REST API 为每个仓库补全 stars / forks / open_issues 精确指标。

本模块不作为独立 Collector 调用, 而是由 ingestion 服务层在入库前调用 enrich。
"""

import logging
import re

import httpx

logger = logging.getLogger(__name__)

_REPO_RE = re.compile(r"github\.com/([^/]+)/([^/#?]+)")


def parse_github_repo(url: str) -> tuple[str, str] | None:
    match = _REPO_RE.search(url)
    if not match:
        return None
    return match.group(1), match.group(2)


async def fetch_repo_stars(
    owner: str,
    repo: str,
    *,
    token: str = "",
) -> dict[str, int] | None:
    """调用 GitHub REST API 获取仓库 Star/Fork/Issue 指标。"""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "CatchNews/0.1",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        logger.warning("GitHub API failed for %s/%s: %s", owner, repo, exc)
        return None

    return {
        "stars": int(data.get("stargazers_count", 0)),
        "forks": int(data.get("forks_count", 0)),
        "open_issues": int(data.get("open_issues_count", 0)),
    }
