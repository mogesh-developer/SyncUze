from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SyncUze"
    DATABASE_URL: str = "sqlite:///./storage/memory.db"


settings = Settings()