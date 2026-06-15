from core.collectors.base import BaseCollector, RawItem


class GitHubStarsCollector(BaseCollector):
    platform = "github"
    track = "tech"

    async def fetch(self) -> list[RawItem]:
        # M0: enrich star metrics via GitHub REST API
        return []
