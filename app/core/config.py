"""Core configuration and settings for the FastAPI application."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Scalable FastAPI Application"
    version: str = "1.0.0"
    description: str = (
        "A scalable FastAPI application with auto-generated documentation "
        "and client type generation"
    )
    debug: bool = True

    # API settings
    api_v1_prefix: str = "/api/v1"
    allowed_hosts: list[str] = ["*"]

    # CORS settings
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
