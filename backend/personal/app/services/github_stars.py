import logging
import re

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

_REPO_RE = re.compile(r"github\.com/([^/]+)/([^/#?]+)")


async def fetch_repo_stars(owner: str, repo: str) -> dict[str, int] | None:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "CatchNews/0.1",
    }
    if settings.github_token:
        headers["Authorization"] = f"Bearer {settings.github_token}"

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


def parse_github_repo(url: str) -> tuple[str, str] | None:
    match = _REPO_RE.search(url)
    if not match:
        return None
    return match.group(1), match.group(2)
