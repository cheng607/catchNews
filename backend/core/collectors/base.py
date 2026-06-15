from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RawItem:
    platform_item_id: str
    title: str
    url: str
    rank: int | None = None
    heat_score: float | None = None
    metrics: dict[str, Any] = field(default_factory=dict)


class BaseCollector(ABC):
    platform: str
    track: str
    default_top_n: int = 20

    @abstractmethod
    async def fetch(self) -> list[RawItem]:
        ...
