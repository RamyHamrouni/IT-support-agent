"""
Application configuration settings using Pydantic.
"""

import os
from typing import List, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings class."""

    PROJECT_NAME: str = "IT Support Agent"
    PROJECT_DESCRIPTION: str = "IT Support Agent is an AI-powered virtual assistant designed to help people solve technical problems on their devices or software. It provides step-by-step troubleshooting guidance, automated diagnostics, and ticket management when issues cannot be resolved automatically."
    VERSION: str = "0.1.0"
    API_PREFIX: str = ""
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    DEV_MODE: bool = DEBUG

    HF_TOKEN: str
    HF_API_BASE: str

    # CORS
    ALLOWED_ORIGINS: str

    # Database
    DB_URL: str

    # Qdrant
  
    QDRANT_URL: str
    QDRANT_API_KEY: str

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    @field_validator("CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from string to list if needed."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        # covers JSON-style list string, e.g. '["http://a.com", "http://b.com"]'
        elif isinstance(v, str):
            import json

            try:
                parsed = json.loads(v)
                if isinstance(parsed, list) and all(isinstance(i, str) for i in parsed):
                    return parsed
            except Exception:
                pass
        raise ValueError(
            f"CORS_ORIGINS must be a list of strings or a comma-separated string. cors value{v}"
        )

    # Database
    DB_ENGINE: str = os.getenv("DB_ENGINE", "sqlite")
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_PORT: str = os.getenv("DB_PORT", "")
    DB_NAME: str = os.getenv("DB_NAME", "db.sqlite3")

    

    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL based on configuration."""
        if self.DB_ENGINE == "sqlite":
            return f"sqlite+aiosqlite:///{self.DB_NAME}"
        elif self.DB_ENGINE == "postgresql":
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def TEST_DATABASE_URL(self) -> str:
        """Construct database URL based on configuration."""
        if self.DB_ENGINE == "sqlite":
            return f"sqlite+aiosqlite:///{self.DB_NAME}-test"
        elif self.DB_ENGINE == "postgresql":
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}-test"
        return f"{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}-test"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
