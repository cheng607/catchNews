"""GitHub Trending 采集器测试 — 解析 + mock fetch 三场景。"""

from unittest.mock import AsyncMock, patch

import pytest
from selectolax.parser import HTMLParser

from core.collectors.base import RawItem
from core.collectors.github_trending import GitHubTrendingCollector

SAMPLE_HTML = """
<html><body>
<article class="Box-row">
  <h2 class="h3 lh-condensed">
    <a href="/anthropics/claude-code">anthropics / claude-code</a>
  </h2>
  <span itemprop="programmingLanguage">TypeScript</span>
  <a class="Link Link--muted Link--secondary d-inline-block" href="/anthropics/claude-code/stargazers">
    <svg class="octicon-star"></svg>
    12,345
  </a>
</article>
<article class="Box-row">
  <h2 class="h3 lh-condensed">
    <a href="/vercel/next.js">vercel / next.js</a>
  </h2>
  <span itemprop="programmingLanguage">JavaScript</span>
  <a class="Link Link--muted Link--secondary d-inline-block" href="/vercel/next.js/stargazers">
    <svg class="octicon-star"></svg>
    88,900
  </a>
</article>
</body></html>
"""

EMPTY_HTML = "<html><body></body></html>"


class TestParseRepo:
    """_parse_repo 解析逻辑测试。"""

    def test_parse_single_repo(self) -> None:
        collector = GitHubTrendingCollector(since="daily")
        tree = HTMLParser(SAMPLE_HTML)
        articles = tree.css("article.Box-row")
        item = collector._parse_repo(articles[0], rank=1)

        assert item is not None
        assert item.title == "anthropics / claude-code"
        assert item.url == "https://github.com/anthropics/claude-code"
        assert item.metrics.get("stars") == 12345
        assert item.metrics.get("language") == "TypeScript"
        assert item.metrics.get("since") == "daily"
        assert item.rank == 1

    def test_parse_multiple_repos(self) -> None:
        collector = GitHubTrendingCollector(since="weekly")
        tree = HTMLParser(SAMPLE_HTML)
        items = []
        for rank, article in enumerate(tree.css("article.Box-row"), start=1):
            item = collector._parse_repo(article, rank)
            if item:
                items.append(item)

        assert len(items) == 2
        assert items[0].metrics.get("since") == "weekly"
        assert items[1].url == "https://github.com/vercel/next.js"
        assert items[1].metrics.get("stars") == 88900

    def test_parse_empty_html_yields_nothing(self) -> None:
        collector = GitHubTrendingCollector(since="daily")
        tree = HTMLParser(EMPTY_HTML)
        items = [
            collector._parse_repo(a, i)
            for i, a in enumerate(tree.css("article.Box-row"), 1)
        ]
        assert items == []


class TestBuildUrl:
    def test_daily_url(self) -> None:
        c = GitHubTrendingCollector(since="daily")
        assert c._build_url() == "https://github.com/trending?since=daily"

    def test_weekly_with_language(self) -> None:
        c = GitHubTrendingCollector(since="weekly", language="python")
        url = c._build_url()
        assert "since=weekly" in url
        assert "spoken_language_code=python" in url


class _FakeResponse:
    def __init__(self, text: str, status: int = 200) -> None:
        self.text = text
        self.status_code = status

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


class _FakeClient:
    def __init__(self, response: _FakeResponse) -> None:
        self._resp = response

    async def get(self, *args, **kwargs) -> _FakeResponse:
        return self._resp

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


@pytest.mark.asyncio
class TestFetchMock:
    """mock httpx 覆盖正常 / 空 / 异常 三场景。"""

    async def test_fetch_normal(self) -> None:
        fake_resp = _FakeResponse(SAMPLE_HTML)
        with patch("core.collectors.github_trending.httpx.AsyncClient", return_value=_FakeClient(fake_resp)):
            collector = GitHubTrendingCollector(since="daily")
            items = await collector.fetch()

        assert len(items) == 2
        assert all(isinstance(i, RawItem) for i in items)
        assert items[0].platform_item_id == "anthropics/claude-code:daily"

    async def test_fetch_empty_page(self) -> None:
        fake_resp = _FakeResponse(EMPTY_HTML)
        with patch("core.collectors.github_trending.httpx.AsyncClient", return_value=_FakeClient(fake_resp)):
            collector = GitHubTrendingCollector(since="daily")
            items = await collector.fetch()

        assert items == []

    async def test_fetch_network_error(self) -> None:
        async def _raise(*args, **kwargs):
            raise ConnectionError("network down")

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get = _raise

        with patch("core.collectors.github_trending.httpx.AsyncClient", return_value=mock_client):
            collector = GitHubTrendingCollector(since="weekly")
            items = await collector.fetch()

        assert items == []
