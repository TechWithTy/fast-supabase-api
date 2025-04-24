"""
Test configuration for FastAPI application.

This config is used for running tests. It inherits from the main Settings and overrides values for testing.
"""
from .config import Settings
from pydantic import EmailStr
import os

class TestSettings(Settings):
    ENVIRONMENT: str = "test"
    TESTING: bool = True
    DEBUG: bool = True
    # Use SQLite in-memory DB for tests (adjust as needed)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "test_user"
    POSTGRES_PASSWORD: str = "test_password"
    POSTGRES_DB: str = "test_db"
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "TEST_DATABASE_URI",
        "sqlite+aiosqlite:///:memory:"
    )
    # Use test email addresses and credentials
    FIRST_SUPERUSER: EmailStr = "testadmin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "testpassword"
    EMAILS_FROM_EMAIL: EmailStr = "testinfo@example.com"
    # Reduce token expiry for tests
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    # Add/override any other settings needed for tests

# Usage in tests:
# from app.core.test_config import TestSettings
# test_settings = TestSettings()
# assert test_settings.TESTING
