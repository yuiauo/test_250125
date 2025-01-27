from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, RedisDsn


class JWTSettings(BaseSettings, extra="allow", env_file=".env"):
    """ JWT Settings """
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_LIFETIME: int


class DBSettings(BaseSettings, extra="allow", env_file=".env"):
    DATABASE_URL: PostgresDsn


class CacheSettings(BaseSettings, extra="allow", env_file=".env"):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_URL: RedisDsn


class APISettings(BaseSettings):
    """ Swagger API settings """
    title: str = "Hospital API"
    description: str = "Test task API"
    version: str = "1.0"
    debug: bool = True
    openapi_tags: list[dict] = [
        {
            "name": "Login",
            "description": "Get access token"
        },
        {
            "name": "Patient",
            "description": "Return all patients for current doctor."
        }
    ]


@lru_cache
class Settings:
    """ Settings singleton """
    def __init__(self):
        self.api = APISettings().model_dump()
        self.jwt = JWTSettings()
        self.db = DBSettings()
        self.cache = CacheSettings()

settings = Settings()
