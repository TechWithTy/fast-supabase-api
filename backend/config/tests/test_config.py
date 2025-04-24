"""
Test configuration for FastAPI using Pydantic BaseSettings.
This file defines settings for the test environment.
"""

from pydantic import BaseSettings
from typing import Optional


class TestSettings(BaseSettings):
    # Example test settings, extend as needed
    app_name: str = "Fast Supabase API - Test"
    debug: bool = True
    database_url: str = "sqlite:///./test_test.db"
    secret_key: str = "TEST_SECRET_KEY"
    redis_url: Optional[str] = None
    prometheus_enabled: bool = False

    class Config:
        env_file = ".env.test"
        env_file_encoding = "utf-8"


test_settings = TestSettings()

"""
Usage:
from app.config.test_config import test_settings
print(test_settings.app_name)
"""
