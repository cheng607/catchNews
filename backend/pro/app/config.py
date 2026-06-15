from core.config import BaseAppSettings


class Settings(BaseAppSettings):
    database_url: str = "postgresql://catchnews:catchnews@localhost:5432/catchnews"
    redis_url: str = "redis://localhost:6379/0"


settings = Settings()
