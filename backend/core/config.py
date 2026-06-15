from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    github_token: str = ""
    refresh_interval_entertainment: int = 30
    refresh_interval_github: int = 360
    link_check_interval: int = 360
    top_n_default: int = 20
    cors_origins: str = "http://localhost:3000"
