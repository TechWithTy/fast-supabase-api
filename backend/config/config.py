"""
FastAPI-compatible configuration using Pydantic BaseSettings.
This file defines the main application settings.
"""
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Example settings, extend as needed
    app_name: str = "Fast Supabase API"
    debug: bool = False
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "CHANGE_ME"
    redis_url: Optional[str] = None
    prometheus_enabled: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

"""
Usage:
from app.config.config import settings
print(settings.app_name)
"""
