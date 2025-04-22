import os
import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    HttpUrl,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

from app.tests.utils.env_loader import load_env

load_env()


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    DOMAIN: str = os.environ.get("DOMAIN", "localhost.tiangolo.com")
    ENVIRONMENT: Literal["local", "staging", "production"] = os.environ.get("ENVIRONMENT", "local")
    PROJECT_NAME: str = os.environ.get("PROJECT_NAME", "Fast-Supabase-Api")
    STACK_NAME: str = os.environ.get("STACK_NAME", "fast-supabase")
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = os.environ.get("BACKEND_CORS_ORIGINS", "http://localhost,http://localhost:5173,https://localhost,https://localhost:5173,http://localhost.tiangolo.com")
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "changethis")
    FIRST_SUPERUSER: EmailStr = os.environ.get("FIRST_SUPERUSER", "admin@example.com")
    FIRST_SUPERUSER_PASSWORD: str = os.environ.get("FIRST_SUPERUSER_PASSWORD", "changethis")
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = os.environ.get("FRONTEND_HOST", "http://localhost:5173")
    SMTP_HOST: str | None = os.environ.get("SMTP_HOST")
    SMTP_USER: str | None = os.environ.get("SMTP_USER")
    SMTP_PASSWORD: str | None = os.environ.get("SMTP_PASSWORD")
    EMAILS_FROM_EMAIL: EmailStr | None = os.environ.get("EMAILS_FROM_EMAIL", "info@example.com")
    SMTP_TLS: bool = os.environ.get("SMTP_TLS", "True") == "True"
    SMTP_SSL: bool = os.environ.get("SMTP_SSL", "False") == "True"
    SMTP_PORT: int = int(os.environ.get("SMTP_PORT", 587))
    EMAILS_FROM_NAME: EmailStr | None = os.environ.get("EMAILS_FROM_NAME")
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = int(os.environ.get("EMAIL_RESET_TOKEN_EXPIRE_HOURS", 48))
    POSTGRES_SERVER: str | None = os.environ.get("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: int | None = int(os.environ.get("POSTGRES_PORT", 5432))
    POSTGRES_USER: str | None = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str | None = os.environ.get("POSTGRES_PASSWORD", "changethis")
    POSTGRES_DB: str | None = os.environ.get("POSTGRES_DB", "app")
    DATABASE_URL: str | None = os.environ.get("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/app")
    SUPABASE_URL: str | None = os.environ.get("SUPABASE_URL", "https://your-supabase-project.supabase.co")
    SUPABASE_ANON_KEY: str | None = os.environ.get("SUPABASE_ANON_KEY", "your_supabase_anon_key_here")
    SUPABASE_SERVICE_ROLE_KEY: str | None = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "your_supabase_service_role_key_here")
    SUPABASE_JWT_SECRET: str | None = os.environ.get("SUPABASE_JWT_SECRET", "your_supabase_jwt_secret_here")
    TEST_USER_EMAIL: EmailStr | None = os.environ.get("TEST_USER_EMAIL", "test@example.com")
    TEST_USER_PASSWORD: str | None = os.environ.get("TEST_USER_PASSWORD", "testpassword123")
    TEST_BUCKET_NAME: str | None = os.environ.get("TEST_BUCKET_NAME", "test-bucket")
    TEST_TABLE_NAME: str | None = os.environ.get("TEST_TABLE_NAME", "test_table")
    TEST_EDGE_FUNCTION: str | None = os.environ.get("TEST_EDGE_FUNCTION", "hello-world")
    SKIP_USER_CREATION: bool = os.environ.get("SKIP_USER_CREATION", "true") == "true"
    REDIS_URL: str | None = os.environ.get("REDIS_URL", "redis://redis:6379/0")
    CELERY_BROKER_URL: str | None = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND: str | None = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
    SENTRY_DSN: HttpUrl | None = os.environ.get("SENTRY_DSN", "your_sentry_dsn_here")
    DOCKER_IMAGE_BACKEND: str | None = os.environ.get("DOCKER_IMAGE_BACKEND", "backend")
    DEFAULT_THROTTLE_RATES_ANON: str = os.environ.get("DEFAULT_THROTTLE_RATES_ANON", "100/day")
    DEFAULT_THROTTLE_RATES_USER: str = os.environ.get("DEFAULT_THROTTLE_RATES_USER", "1000/day")
    DEFAULT_THROTTLE_RATES_PREMIUM: str = os.environ.get("DEFAULT_THROTTLE_RATES_PREMIUM", "5000/day")
    CORS_ALLOWED_ORIGINS: str | None = os.environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:3000,https://your-frontend-domain.com")
    VAPI_PRIVATE_TOKEN: str = os.environ.get("VAPI_PRIVATE_TOKEN", "")
    ELEVENLABS_API_KEY: str | None = os.environ.get("ELEVENLABS_API_KEY")
    ELEVENLABS_ORG_ID: str | None = os.environ.get("ELEVENLABS_ORG_ID")
    ELEVENLABS_PROJECT_ID: str | None = os.environ.get("ELEVENLABS_PROJECT_ID")
    ELEVENLABS_VOICE_ID: str | None = os.environ.get("ELEVENLABS_VOICE_ID")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    @computed_field  # type: ignore[prop-decorator]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    EMAIL_TEST_USER: EmailStr = "test@example.com"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str | None:
        if all(
            [
                self.POSTGRES_SERVER,
                self.POSTGRES_PORT,
                self.POSTGRES_USER,
                self.POSTGRES_PASSWORD,
                self.POSTGRES_DB,
            ]
        ):
            return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return None

    @property
    def supabase_enabled(self) -> bool:
        return bool(self.SUPABASE_URL and self.SUPABASE_ANON_KEY)

    @property
    def db_backend(self) -> str:
        if self.SQLALCHEMY_DATABASE_URI:
            return "postgres"
        elif self.supabase_enabled:
            return "supabase"
        else:
            raise RuntimeError(
                "No database backend configured. Set either Postgres or Supabase environment variables."
            )

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        if self.POSTGRES_PASSWORD:
            self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self


settings = Settings()  # type: ignore
