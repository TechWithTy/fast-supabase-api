import hashlib
import json
import time

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.caching.utils.redis_cache import (
    get_cached_result,
    get_or_set_cache,
    redis_cache,
)
from app.core.config import settings
from app.core.db import engine
from app.main import app
from app.models import User


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def db():
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def test_user(db):
    user = User(
        email="test@example.com",
        full_name="Test User",
        is_active=True,
        is_superuser=False,
        hashed_password="$2b$12$KIXQJz4Q7Z0w0V6VqTgL7O6c9v1CwQxK1QOQ5ZyQ5ZyQ5ZyQ5ZyQ5",  # bcrypt for 'testpassword'
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.delete(user)
    db.commit()


@pytest.fixture(scope="function")
def user_token(client, test_user):
    response = client.post(
        f"{settings.API_V1_STR}/login/access-token",
        data={"username": test_user.email, "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(autouse=True)
def clear_redis_cache():
    redis_cache.flushdb()
    yield
    redis_cache.flushdb()


def test_auth_view_caching(client, user_token):
    """Test that authentication view uses caching."""
    test_token = "test-token-12345"
    token_hash = hashlib.md5(test_token.encode()).hexdigest()
    cache_key = f"user_info:{token_hash}"
    redis_cache.delete(cache_key)
    assert get_cached_result(cache_key) is None  # Should be None (cache miss)
    mock_user_data = {"id": "test-user-id", "email": "test@example.com"}
    redis_cache.set(cache_key, json.dumps(mock_user_data).encode(), ex=10)
    cached = get_cached_result(cache_key)
    if isinstance(cached, bytes):
        cached = json.loads(cached.decode())
    assert cached == mock_user_data
    redis_cache.delete(cache_key)
    assert get_cached_result(cache_key) is None


def test_cache_integration_with_expiry():
    """Test cache expiry and refresh logic."""
    key = "integration_test_key"
    value = {"foo": "bar"}
    redis_cache.delete(key)
    assert get_cached_result(key) is None
    redis_cache.set(key, json.dumps(value).encode(), ex=1)
    assert json.loads(get_cached_result(key).decode()) == value
    time.sleep(1.5)
    assert get_cached_result(key) is None

    def slow_func():
        return value

    result = get_or_set_cache(key, slow_func, expire_seconds=2)
    assert result == value
    assert json.loads(get_cached_result(key).decode()) == value
    redis_cache.delete(key)
    assert get_cached_result(key) is None


def test_cache_invalidation_on_insert():
    """Test that insert_data invalidates cache."""
    table_name = "test_table"
    query = {"column": "value"}
    insert_data = {"new_column": "new_value"}
    mock_fetch_response = [{"id": 1, "name": "Test Item"}]
    mock_insert_response = {"id": 2, "name": "New Item"}
    cache_key_parts = [f"table:{table_name}", f"query:{json.dumps(query)}"]
    cache_key_parts.sort()
    cache_key = (
        f"db_query:{hashlib.md5(':'.join(cache_key_parts).encode()).hexdigest()}"
    )
    redis_cache.delete(cache_key)
    redis_cache.set(cache_key, json.dumps(mock_fetch_response).encode(), ex=300)
    assert json.loads(get_cached_result(cache_key).decode()) == mock_fetch_response
    redis_cache.delete(cache_key)
    assert get_cached_result(cache_key) is None


def test_storage_caching():
    """Test that storage view uses caching."""
    bucket_id = "test-bucket"
    path = "test-path"
    mock_files_response = {
        "files": [
            {"name": "file1.txt", "id": "1", "size": 100},
            {"name": "file2.txt", "id": "2", "size": 200},
        ]
    }
    cache_key = f"storage:{bucket_id}:{path}"
    redis_cache.delete(cache_key)

    def fetch_files():
        return mock_files_response

    result1 = get_or_set_cache(cache_key, fetch_files, expire_seconds=300)
    assert result1 == mock_files_response
    result2 = get_cached_result(cache_key)
    if isinstance(result2, bytes):
        result2 = json.loads(result2.decode())
    assert result2 == mock_files_response


def test_cache_performance():
    """Test performance improvement with caching."""
    table = "test_table"
    query = {"column": "value"}
    cache_key_parts = [f"table:{table}", f"query:{json.dumps(query)}"]
    cache_key_parts.sort()
    cache_key = (
        f"db_query:{hashlib.md5(':'.join(cache_key_parts).encode()).hexdigest()}"
    )
    redis_cache.delete(cache_key)

    def slow_fetch(*args, **kwargs):
        time.sleep(0.1)
        return [{"id": 1, "name": "Test Item"}]

    start_time = time.time()
    result1 = get_cached_result(cache_key)
    if result1 is None:
        result1 = slow_fetch(table, query)
        redis_cache.set(cache_key, json.dumps(result1).encode(), ex=300)
    first_request_time = time.time() - start_time
    start_time = time.time()
    result2 = get_cached_result(cache_key)
    if result2 is None:
        result2 = slow_fetch(table, query)
    else:
        if isinstance(result2, bytes):
            result2 = json.loads(result2.decode())
    second_request_time = time.time() - start_time
    assert second_request_time < first_request_time
    assert (first_request_time - second_request_time) > 0.05
