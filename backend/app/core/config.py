from importlib import resources as pkg_resources
from pathlib import Path
from typing import Literal

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMProviderSettings(BaseSettings):
    """Base settings for LLM providers."""

    temperature: float | None = Field(alias="DEFAULT_TEMPERATURE", default=0.1)
    max_tokens: int | None = Field(alias="DEFAULT_MAX_TOKENS", default=None)
    top_p: float | None = Field(alias="DEFAULT_TOP_P", default=1)
    max_retries: int = 3

    model_config = SettingsConfigDict(
        env_file="../.env", env_file_encoding="utf-8", extra="ignore"
    )


class OpenAISettings(LLMProviderSettings):
    api_key: str | None = Field(alias="OPENAI_API_KEY", default=None)
    base_url: str = "https://api.openai.com/v1"


class AnthropicSettings(LLMProviderSettings):
    api_key: str | None = Field(alias="ANTHROPIC_API_KEY", default=None)


class TogetherAISettings(LLMProviderSettings):
    api_key: str | None = Field(alias="TOGETHER_API_KEY", default=None)
    base_url: str = "https://api.together.xyz/v1"


class PerplexitySettings(LLMProviderSettings):
    api_key: str | None = Field(alias="PERPLEXITY_API_KEY", default=None)
    base_url: str = "https://api.perplexity.ai"


class GroqSettings(LLMProviderSettings):
    api_key: str | None = Field(alias="GROQ_API_KEY", default=None)
    base_url: str = "https://api.groq.com/openai/v1"


class OllamaSettings(LLMProviderSettings):
    api_key: str = "ollama"
    base_url: str = Field(
        default="http://localhost:11434/v1",
        alias="OLLAMA_BASE_URL",
    )


class LMStudioSettings(LLMProviderSettings):
    api_key: str = "lmstudio"
    base_url: str = "http://localhost:1234/v1"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str = ""

    DEFAULT_MODEL: str = "gpt-4.1-mini"
    DEFAULT_PROVIDER: str = "openai"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # LLM Provider settings
    openai: OpenAISettings = OpenAISettings()
    ollama: OllamaSettings = OllamaSettings()
    groq: GroqSettings = GroqSettings()
    anthropic: AnthropicSettings = AnthropicSettings()
    lmstudio: LMStudioSettings = LMStudioSettings()
    perplexity: PerplexitySettings = PerplexitySettings()
    together: TogetherAISettings = TogetherAISettings()

    @computed_field
    @property
    def TEMPLATES_DIR(self) -> Path:
        return Path(pkg_resources.files("app.prompts").joinpath("templates"))

    @computed_field
    @property
    def PARAMETERS_FILE_PATH(self) -> Path:
        return Path(pkg_resources.files("app.data").joinpath("parameters.json"))

    @computed_field
    @property
    def PRINCIPLES_FILE_PATH(self) -> Path:
        return Path(pkg_resources.files("app.data").joinpath("principles.json"))


settings = Settings()
