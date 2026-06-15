from core.collectors.base import BaseCollector, RawItem


class WeiboCollector(BaseCollector):
    platform = "weibo"
    track = "entertainment"

    async def fetch(self) -> list[RawItem]:
        # M1: HTTP JSON first, Playwright fallback
        return []
