"""normalizer 单元测试 — 验证 RawItem → HotItemSchema 映射。"""

from core.collectors.base import RawItem
from core.normalizer import normalize


def _make_raw(
    pid: str = "owner/repo:daily",
    title: str = "test repo",
    url: str = "https://github.com/owner/repo",
    rank: int = 1,
    heat_score: float | None = 100.0,
    metrics: dict | None = None,
) -> RawItem:
    return RawItem(
        platform_item_id=pid,
        title=title,
        url=url,
        rank=rank,
        heat_score=heat_score,
        metrics=metrics or {"stars": 100, "language": "Python"},
    )


class TestNormalize:
    def test_id_format(self) -> None:
        schema = normalize(_make_raw(), platform="github", track="tech", source_label="GitHub Trending")
        assert schema.id == "github:owner/repo:daily"

    def test_fields_mapping(self) -> None:
        raw = _make_raw(title="FastAPI Framework", url="https://github.com/tiangolo/fastapi", rank=3, heat_score=5000.0)
        schema = normalize(raw, platform="github", track="tech", source_label="GitHub Trending")

        assert schema.platform == "github"
        assert schema.track == "tech"
        assert schema.title == "FastAPI Framework"
        assert schema.url == "https://github.com/tiangolo/fastapi"
        assert schema.rank == 3
        assert schema.heat_score == 5000.0
        assert schema.source_label == "GitHub Trending"

    def test_link_status_default_ok(self) -> None:
        schema = normalize(_make_raw(), platform="github", track="tech", source_label="GH")
        assert schema.link_status == "ok"

    def test_rank_change_is_none(self) -> None:
        schema = normalize(_make_raw(), platform="github", track="tech", source_label="GH")
        assert schema.rank_change is None

    def test_metrics_preserved(self) -> None:
        raw = _make_raw(metrics={"stars": 999, "forks": 50, "language": "Rust"})
        schema = normalize(raw, platform="github", track="tech", source_label="GH")
        assert schema.metrics["stars"] == 999
        assert schema.metrics["forks"] == 50

    def test_timestamps_set(self) -> None:
        schema = normalize(_make_raw(), platform="github", track="tech", source_label="GH")
        assert schema.captured_at is not None
        assert schema.first_seen_at is not None
        assert schema.captured_at == schema.first_seen_at

    def test_no_heat_score(self) -> None:
        raw = _make_raw(heat_score=None)
        schema = normalize(raw, platform="github", track="tech", source_label="GH")
        assert schema.heat_score is None
