from core.collectors.base import BaseCollector, RawItem


class GitHubTrendingCollector(BaseCollector):
    platform = "github"
    track = "tech"

    async def fetch(self) -> list[RawItem]:
        # M0: implement trending page parse
        return []
