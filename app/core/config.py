from functools import lru_cache
from pathlib import Path
from typing import Annotated, Any, Literal
from urllib.parse import quote_plus

from pydantic import Field, computed_field, field_validator
from pydantic_settings import BaseSettings as PydanticSettings
from pydantic_settings import SettingsConfigDict

from app.core.enums import AppEnvEnum

PROJECT_DIR = Path(__file__).parent.parent.parent


class BaseSettings(PydanticSettings):
    model_config = SettingsConfigDict(env_file=f"{PROJECT_DIR}/.env", extra="allow", env_file_encoding="utf-8")


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

    host: str = "localhost"
    user: str = "user"
    password: str = "pass"
    port: int = 5432
    name: str = "chat_storage_db"
    echo: bool = False

    @computed_field  # type: ignore[prop-decorator]
    @property
    def pg_dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{quote_plus(self.password)}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    db: DBSettings = DBSettings()

    # CORS SETTINGS
    base_prefix: Annotated[str, Field(validate_default=True)] = "/api"
    env_name: AppEnvEnum = AppEnvEnum.PROD
    backend_cors_origins: list[str] = ["*"]
    backend_cors_headers: list[str] = ["*"]

    # LOG SETTINGS
    log_level: Literal["INFO", "DEBUG", "WARN", "ERROR"] = "INFO"
    log_json_format: bool = False

    # UVICORN SETTINGS
    uvicorn_host: str = "0.0.0.0"
    uvicorn_port: int = 8000

    limiter_limit: str = "1/second"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def internal_env(self) -> bool:
        return self.env_name in {AppEnvEnum.LOCAL, AppEnvEnum.DEV, AppEnvEnum.TEST}

    @computed_field  # type: ignore[prop-decorator]
    @property
    def external_env(self) -> bool:
        return not self.internal_env

    # DOCS SETTINGS
    @computed_field  # type: ignore[prop-decorator]
    @property
    def openapi_url(self) -> str:
        return f"{self.base_prefix}/openapi.json"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def swagger_url(self) -> str:
        return f"{self.base_prefix}/docs"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def redoc_url(self) -> str:
        return f"{self.base_prefix}/redoc"


class TestSettings(Settings):
    limiter_limit: str = ""  # unlimited

    # Test are hardcoded to use api as base_url.
    # This is to avoid having to change the base_url in every test
    @field_validator("base_prefix")
    def force_base_url_value(cls, _: str, __: dict[str, Any]) -> str:
        return "/api"


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()

    if settings.env_name == AppEnvEnum.TEST:
        return TestSettings()

    return settings


config: Settings = get_settings()
