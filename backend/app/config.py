"""
Configuration management for FastAPI backend
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    api_title: str = "Personal Agent Web Dashboard"
    api_version: str = "1.0.0"

    # Gemini API Configuration
    gemini_api_key: str = ""

    # CORS Configuration
    cors_origins: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"

    # Logging Configuration
    log_level: str = "INFO"
    log_dir: str = "./logs"

    # File Configuration
    output_dir: str = "./output"
    upload_dir: str = "./uploads"
    max_upload_size: int = 52428800  # 50MB

    # Personal Agent CLI Path
    cli_path: str = "./personal_agent"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cors_origins_list(self) -> list:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def output_path(self) -> Path:
        """Get output directory path."""
        path = Path(self.output_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def upload_path(self) -> Path:
        """Get upload directory path."""
        path = Path(self.upload_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def log_path(self) -> Path:
        """Get logs directory path."""
        path = Path(self.log_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path


# Load settings from environment
settings = Settings()
