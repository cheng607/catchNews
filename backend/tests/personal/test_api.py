"""个人版 API 集成测试 — 使用内存 SQLite + StaticPool 验证响应格式。"""

import os
from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite://"

from core.models.base import Base, HotItem, PlatformHealth  # noqa: E402

_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


@pytest.fixture(autouse=True)
def _setup_tables():
    Base.metadata.create_all(bind=_engine)
    yield
    Base.metadata.drop_all(bind=_engine)


@pytest.fixture(name="db_session")
def fixture_db_session():
    session = _TestingSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(name="client")
def fixture_client(db_session: Session):
    import app.database as db_mod
    import app.main as main_mod
    from app.database import get_db

    orig_engine = db_mod.engine
    orig_session_local = db_mod.SessionLocal
    orig_main_session = main_mod.SessionLocal

    db_mod.engine = _engine
    db_mod.SessionLocal = _TestingSession
    main_mod.SessionLocal = _TestingSession

    def _override_db():
        try:
            yield db_session
        finally:
            pass

    main_mod.app.dependency_overrides[get_db] = _override_db

    with patch.object(main_mod, "run_all_collectors", new_callable=AsyncMock, return_value={}):
        with TestClient(main_mod.app, raise_server_exceptions=False) as c:
            yield c

    main_mod.app.dependency_overrides.clear()
    db_mod.engine = orig_engine
    db_mod.SessionLocal = orig_session_local
    main_mod.SessionLocal = orig_main_session


def _seed_github_items(db: Session, count: int = 3) -> None:
    now = datetime.now(tz=UTC)
    for i in range(1, count + 1):
        db.add(HotItem(
            id=f"github:owner/repo-{i}:daily",
            platform="github",
            track="tech",
            title=f"awesome-lib-{i}",
            url=f"https://github.com/owner/repo-{i}",
            rank=i,
            heat_score=float(1000 * i),
            metrics={"stars": 1000 * i, "language": "Python", "since": "daily"},
            captured_at=now,
            first_seen_at=now,
            link_status="ok",
            is_active=True,
        ))
    db.add(PlatformHealth(platform="github", last_success_at=now, status="ok"))
    db.commit()


class TestHotItemsEndpoint:
    def test_empty_response(self, client: TestClient, db_session: Session) -> None:
        db_session.add(PlatformHealth(platform="github", status="ok"))
        db_session.commit()
        resp = client.get("/api/v1/hot-items?track=tech")
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert "updated_at" in data["meta"]

    def test_github_items_response_shape(self, client: TestClient, db_session: Session) -> None:
        _seed_github_items(db_session)
        resp = client.get("/api/v1/hot-items?track=tech")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["items"]) == 3

        item = data["items"][0]
        for key in ("id", "title", "url", "rank", "metrics", "source_label"):
            assert key in item, f"missing key: {key}"
        assert item["platform"] == "github"
        assert item["url"].startswith("https://github.com/")

    def test_top_n_limits(self, client: TestClient, db_session: Session) -> None:
        _seed_github_items(db_session, count=5)
        resp = client.get("/api/v1/hot-items?track=tech&top_n=2")
        assert resp.status_code == 200
        assert len(resp.json()["items"]) == 2

    def test_search_filter(self, client: TestClient, db_session: Session) -> None:
        _seed_github_items(db_session)
        resp = client.get("/api/v1/hot-items?track=tech&q=lib-2")
        assert resp.status_code == 200
        items = resp.json()["items"]
        assert len(items) == 1
        assert "lib-2" in items[0]["title"]

    def test_platform_filter(self, client: TestClient, db_session: Session) -> None:
        _seed_github_items(db_session)
        resp = client.get("/api/v1/hot-items?platform=weibo")
        assert resp.status_code == 200
        assert resp.json()["items"] == []


class TestHealthEndpoint:
    def test_health_returns_ok(self, client: TestClient) -> None:
        resp = client.get("/api/v1/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["edition"] == "personal"
