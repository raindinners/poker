from __future__ import annotations

from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
    )


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


class RedisSettings(BaseSettings):
    REDIS_HOSTNAME: str
    REDIS_PORT: int
    REDIS_CHANNEL: str

    @property
    def url(self) -> str:
        driver, hostname, port = ("redis", self.REDIS_HOSTNAME, self.REDIS_PORT)

        return f"{driver}://{hostname}:{port}"


redis_settings = RedisSettings()
