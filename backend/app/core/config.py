from importlib import resources as pkg_resources
from pathlib import Path
from typing import Literal, Optional

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str = ""
    TEMPLATES_DIR: str = "./prompts"

    DEFAULT_MODEL: str = "gpt-4.1-mini"
    DEFAULT_PROVIDER: str = "openai"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def PARAMETERS_FILE_PATH(self) -> Path:
        return Path(pkg_resources.files("app.data").joinpath("parameters.json"))

    @computed_field  # type: ignore[prop-decorator]
    @property
    def PRINCIPLES_FILE_PATH(self) -> Path:
        return Path(pkg_resources.files("app.data").joinpath("principles.json"))


settings = Settings()
