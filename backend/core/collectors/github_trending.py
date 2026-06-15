import logging
import re
from typing import Literal

import httpx
from selectolax.parser import HTMLParser

from core.collectors.base import BaseCollector, RawItem
from core.link_validator import is_allowed_url

logger = logging.getLogger(__name__)

TrendingSince = Literal["daily", "weekly", "monthly"]

_REPO_PATH_RE = re.compile(r"^/([^/]+)/([^/#?]+)")
_STARS_GAINED_RE = re.compile(r"^([\d,]+)\s+stars\s+(today|this week)$", re.IGNORECASE)


class GitHubTrendingCollector(BaseCollector):
    platform = "github"
    track = "tech"

    def __init__(self, since: TrendingSince = "daily", language: str | None = None) -> None:
        self.since = since
        self.language = language

    def _build_url(self) -> str:
        url = f"https://github.com/trending?since={self.since}"
        if self.language and self.language.lower() not in ("all", ""):
            url += f"&spoken_language_code={self.language.lower()}"
        return url

    @staticmethod
    def _parse_stars(text: str) -> int | None:
        cleaned = text.strip().replace(",", "")
        if not cleaned:
            return None
        try:
            return int(cleaned)
        except ValueError:
            return None

    @staticmethod
    def _parse_language(article: HTMLParser) -> str | None:
        for span in article.css("span[itemprop='programmingLanguage']"):
            value = span.text(strip=True)
            if value:
                return value
        return None

    @staticmethod
    def _parse_description(article: HTMLParser) -> str | None:
        for paragraph in article.css("p"):
            text = paragraph.text(strip=True)
            if text:
                return text
        return None

    @staticmethod
    def _parse_stars_gained(article: HTMLParser, since: TrendingSince) -> int | None:
        for span in article.css("span.d-inline-block.float-sm-right"):
            match = _STARS_GAINED_RE.match(span.text(strip=True))
            if not match:
                continue
            value = int(match.group(1).replace(",", ""))
            period = match.group(2).lower()
            if since == "daily" and period == "today":
                return value
            if since == "weekly" and period == "this week":
                return value
            if since == "monthly" and period == "this month":
                return value
        return None

    def _parse_repo(self, article: HTMLParser, rank: int) -> RawItem | None:
        link = article.css_first("h2 a")
        if link is None:
            return None
        href = link.attributes.get("href", "")
        match = _REPO_PATH_RE.match(href)
        if not match:
            return None
        owner, repo = match.group(1), match.group(2)
        url = f"https://github.com/{owner}/{repo}"
        if not is_allowed_url(url):
            return None

        title = link.text(strip=True).replace("\n", " ").replace("  ", " ").strip()
        if not title:
            title = f"{owner}/{repo}"

        stars: int | None = None
        for anchor in article.css("a.Link--muted"):
            label = anchor.text(strip=True)
            if label and label.replace(",", "").isdigit():
                stars = self._parse_stars(label)
                break

        language = self._parse_language(article)
        description = self._parse_description(article)
        stars_gained = self._parse_stars_gained(article, self.since)
        metrics: dict[str, int | str] = {"since": self.since}
        if stars is not None:
            metrics["stars"] = stars
        if language:
            metrics["language"] = language
        if description:
            metrics["description"] = description
        if stars_gained is not None:
            if self.since == "weekly":
                metrics["stars_this_week"] = stars_gained
            else:
                metrics["stars_today"] = stars_gained

        return RawItem(
            platform_item_id=f"{owner}/{repo}:{self.since}",
            title=title,
            url=url,
            rank=rank,
            heat_score=float(stars) if stars is not None else None,
            metrics=metrics,
        )

    async def fetch(self) -> list[RawItem]:
        url = self._build_url()
        headers = {
            "User-Agent": "CatchNews/0.1 (+https://github.com/cheng607/catchNews)",
            "Accept": "text/html",
        }
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
        except Exception as exc:
            logger.exception("GitHub trending fetch failed: %s", exc)
            return []

        tree = HTMLParser(response.text)
        items: list[RawItem] = []
        for rank, article in enumerate(tree.css("article.Box-row"), start=1):
            item = self._parse_repo(article, rank)
            if item is not None:
                items.append(item)
            if len(items) >= self.default_top_n:
                break
        return items
