from enum import auto
from secrets import token_urlsafe

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings

from core.enum import StrEnum


class EnvironmentType(StrEnum):
    DEVELOPMENT = auto()
    PRODUCTION = auto()
    TEST = auto()


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True


class Config(BaseConfig):
    APP_TITLE: str = "FastAPI Application"
    DEBUG: bool = False
    ENVIRONMENT: EnvironmentType = EnvironmentType.DEVELOPMENT
    WORKERS: int = 1

    POSTGRES_URL: PostgresDsn
    POSTGRES_TEST_URL: PostgresDsn
    REDIS_URL: RedisDsn

    SECRET_KEY: str = token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24

    SQLALCHEMY_POOL_SIZE: int = 15
    SQLALCHEMY_POOL_TIMEOUT: int = 30
    SQLALCHEMY_POOL_RECYCLE: int = 3600
    SQLALCHEMY_MAX_OVERFLOW: int = 5

    RELEASE_VERSION: str = "1.0"


config: Config = Config()
