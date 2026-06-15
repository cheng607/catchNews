from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class HotItem(Base):
    __tablename__ = "hot_items"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    platform: Mapped[str] = mapped_column(Text, index=True)
    track: Mapped[str] = mapped_column(Text, index=True)
    title: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(Text)
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    heat_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    captured_at: Mapped[datetime] = mapped_column(DateTime)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime)
    link_status: Mapped[str] = mapped_column(Text, default="ok")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class HotSnapshot(Base):
    __tablename__ = "hot_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    platform: Mapped[str] = mapped_column(Text, index=True)
    snapshot_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    payload: Mapped[list[dict[str, Any]]] = mapped_column(JSON)


class PlatformHealth(Base):
    __tablename__ = "platform_health"

    platform: Mapped[str] = mapped_column(Text, primary_key=True)
    last_success_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(Text, default="ok")
