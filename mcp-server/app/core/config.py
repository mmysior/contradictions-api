from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """MCP Server settings."""

    model_config = SettingsConfigDict(
        env_file="../../../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_BASE_URL: str = Field(
        default="http://localhost:8000",
        description="Base URL for the backend API",
    )

    HOST: str = Field(
        default="0.0.0.0",
        description="Host to bind the MCP server to",
    )

    PORT: int = Field(
        default=8001,
        description="Port to run the MCP server on",
    )


settings = Settings()
