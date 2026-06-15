from core.collectors.base import BaseCollector, RawItem


class ZhihuCollector(BaseCollector):
    platform = "zhihu"
    track = "entertainment"

    async def fetch(self) -> list[RawItem]:
        # M3: HTTP JSON
        return []
