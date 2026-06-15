from pathlib import Path

from pydantic_settings import SettingsConfigDict

from core.config import BaseAppSettings

_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseAppSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "sqlite:///./data/catchnews.db"


settings = Settings()
