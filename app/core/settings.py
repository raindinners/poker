from __future__ import annotations

from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
    )


class APIProtectSettings(BaseSettings):
    ALLOWED_IPS: str


api_protect_settings = APIProtectSettings()


class ServerSettings(BaseSettings):
    DEBUG: bool
    RELOAD: bool
    HOSTNAME: str
    PORT: int


server_settings = ServerSettings()


class LoggingSettings(BaseSettings):
    MAIN_LOGGER_NAME: str
    LOGGING_LEVEL: str


logging_settings = LoggingSettings()


class CORSSettings(BaseSettings):
    ALLOW_ORIGINS: str
    ALLOW_CREDENTIALS: bool
    ALLOW_METHODS: str
    ALLOW_HEADERS: str


cors_settings = CORSSettings()


class DatabaseSettings(BaseSettings):
    DATABASE_DRIVER: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str

    @property
    def url(self) -> str:
        driver, user, password, host, port, name = (
            self.DATABASE_DRIVER,
            self.DATABASE_USERNAME,
            self.DATABASE_PASSWORD,
            self.DATABASE_HOSTNAME,
            self.DATABASE_PORT,
            self.DATABASE_NAME,
        )

        return f"{driver}://{user}:{password}@{host}:{port}/{name}"


database_settings = DatabaseSettings()


class RedisSettings(BaseSettings):
    REDIS_HOSTNAME: str
    REDIS_PORT: int
    REDIS_CHANNEL: str

    @property
    def url(self) -> str:
        driver, hostname, port = ("redis", self.REDIS_HOSTNAME, self.REDIS_PORT)

        return f"{driver}://{hostname}:{port}"


redis_settings = RedisSettings()
