# Ensure environment variables are loaded for all tests
import os
# Set test user credentials globally for all tests



from collections.abc import Generator

import pytest
import redis.asyncio as aioredis
from fastapi.testclient import TestClient
from fastapi_limiter import FastAPILimiter
from sqlmodel import Session

from app.core.config import settings
from app.core.utils.db_selector import get_db_client
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="module", autouse=True)
async def init_redis_limiter():
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)
    yield
    # Optionally, close redis connection after tests
    await redis.close()
    
@pytest.fixture(scope="session", autouse=True)
def db():
    db_client = get_db_client()
    yield db_client
    # Optionally: cleanup code for SQLAlchemy, if used


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
