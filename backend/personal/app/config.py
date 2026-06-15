from core.config import BaseAppSettings


class Settings(BaseAppSettings):
    database_url: str = "sqlite:///./data/catchnews.db"


settings = Settings()
