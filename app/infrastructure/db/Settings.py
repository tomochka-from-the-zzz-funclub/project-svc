import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Параметры для базы данных
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # Параметры для S3
    S3_BUCKET_NAME: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_REGION_NAME: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")