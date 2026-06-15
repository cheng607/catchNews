from core.collectors.base import BaseCollector, RawItem


class BaiduCollector(BaseCollector):
    platform = "baidu"
    track = "entertainment"

    async def fetch(self) -> list[RawItem]:
        # M1: HTTP JSON
        return []
