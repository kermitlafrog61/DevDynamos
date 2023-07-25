from pathlib import Path

from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    BASE_URL: str = 'http://localhost:8000'
    SECRET_KEY: str
    MEDIA_ROOT: Path = BASE_DIR / 'media'
    MEDIA_URL: str = BASE_URL + '/media/'

class AdminConfig(BaseSettings):
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

class DatabaseConfig(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str

    @property
    def DATABASE_URL(self)-> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:5432/{db_name}".format(
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            db_name=self.POSTGRES_DB
        )


class EmailConfig(BaseSettings):
    EMAIL_PASSWORD: str
    EMAIL_HOST: str


class CeleryConfig(BaseSettings):
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str


class Settings(AppConfig, AdminConfig, DatabaseConfig, EmailConfig, CeleryConfig):
    pass


settings = Settings()
