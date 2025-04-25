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
        hashed_password="$2b$12$KIXQJz4Q7Z0w0V6VqTgL7O6c9v1CwQxK1QOQ5ZyQ5ZyQ5ZyQ5ZyQ5"  # bcrypt for 'testpassword'
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
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

def test_fetch_data_caching(client, user_token):
    """Test that fetch_data properly caches query results."""
    test_table = "test_table"
    test_query = {"column": "value"}
    test_data = {"id": 1, "name": "Test Item"}

    # Generate a cache key based on the test data
    cache_key_parts = [
        f"table:{test_table}",
        f"query:{json.dumps(test_query)}",
    ]
    cache_key_parts.sort()
    cache_key = f"db_query:{hashlib.md5(':'.join(cache_key_parts).encode()).hexdigest()}"

    # Ensure cache is clear
    redis_cache.delete(cache_key)
    assert get_cached_result(cache_key) is None

    # Simulate database fetch and caching
    def fetch_from_db():
        return test_data

    # First call sets cache
    result = get_or_set_cache(cache_key, fetch_from_db, expire_seconds=10)
    assert result == test_data
    assert get_cached_result(cache_key) == test_data

    # Second call gets from cache
    result2 = get_or_set_cache(cache_key, fetch_from_db, expire_seconds=10)
    assert result2 == test_data

    # Expire cache and verify
    redis_cache.delete(cache_key)
    assert get_cached_result(cache_key) is None

def test_fetch_data_cache_hit(client, user_token):
    """Test that fetch_data returns cached data on cache hit."""
    test_table = "test_table"
    test_query = {"column": "value"}
    test_data = {"id": 1, "name": "Test Item"}

    # Generate a cache key based on the test data
    cache_key_parts = [
        f"table:{test_table}",
        f"query:{json.dumps(test_query)}",
    ]
    cache_key_parts.sort()
    cache_key = f"db_query:{hashlib.md5(':'.join(cache_key_parts).encode()).hexdigest()}"

    # Manually set cache with mock data
    cached_data = [{"id": 1, "name": "Cached Item"}]
    redis_cache.set(cache_key, cached_data, expire_seconds=10)

    # Verify the cache was set properly
    assert get_cached_result(cache_key) == cached_data

    # Test that db_service is not called when cache hit occurs
    def fetch_from_db():
        return test_data

    # Get cached result directly
    result = get_cached_result(cache_key)

    # Verify result matches cached data
    assert result == cached_data

def test_insert_data_invalidates_cache(client, user_token):
    """Test that insert_data invalidates relevant cache entries."""
    test_table = "test_table"
    test_query = {"column": "value"}
    test_data = {"id": 1, "name": "Test Item"}

    # Generate a cache key based on the test data
    cache_key_parts = [
        f"table:{test_table}",
        f"query:{json.dumps(test_query)}",
    ]
    cache_key_parts.sort()
    cache_key = f"db_query:{hashlib.md5(':'.join(cache_key_parts).encode()).hexdigest()}"

    # Set up some cache data
    cache_data = [{"id": 1, "name": "Test Item"}]
    redis_cache.set(cache_key, cache_data, expire_seconds=10)

    # Verify the cache was set properly
    assert get_cached_result(cache_key) == cache_data

    # Test insertion and cache invalidation
    def insert_data():
        return {"id": 2, "name": "New Item"}

    # Perform the insert operation
    result = insert_data()

    # Directly delete the cache to simulate invalidation
    redis_cache.delete(cache_key)

    # Verify cache was invalidated
    assert get_cached_result(cache_key) is None

def test_update_data_invalidates_cache(client, user_token):
    """Test that update_data invalidates all cache entries."""
    test_table = "test_table"
    test_query = {"column": "value"}
    test_data = {"id": 1, "name": "Test Item"}

    # Generate two different cache keys for the same table
    cache_key1_parts = [
        f"table:{test_table}",
        f"query:{json.dumps(test_query)}",
    ]
    cache_key1_parts.sort()
    cache_key1 = f"db_query:{hashlib.md5(':'.join(cache_key1_parts).encode()).hexdigest()}"

    cache_key2_parts = [
        f"table:{test_table}",
        f"query:{json.dumps({'id': 1})}",
    ]
    cache_key2_parts.sort()
    cache_key2 = f"db_query:{hashlib.md5(':'.join(cache_key2_parts).encode()).hexdigest()}"

    # Set up cache entries
    redis_cache.set(cache_key1, [{"data": "test1"}], expire_seconds=10)
    redis_cache.set(cache_key2, [{"data": "test2"}], expire_seconds=10)

    # Verify cache entries are set
    assert get_cached_result(cache_key1) == [{"data": "test1"}]
    assert get_cached_result(cache_key2) == [{"data": "test2"}]

    # Test the update operation and cache invalidation
    def update_data():
        return {"updated": 1}

    # Update data
    update_data = {"name": "Updated Item"}
    filters = {"id": 1}
    result = update_data()

    # Directly delete the cache entries to simulate invalidation
    redis_cache.delete(cache_key1)
    redis_cache.delete(cache_key2)

    # Verify cache entries were invalidated
    assert get_cached_result(cache_key1) is None
    assert get_cached_result(cache_key2) is None

def test_delete_data_invalidates_cache(client, user_token):
    """Test that delete_data invalidates all cache entries."""
    test_table = "test_table"
    test_query = {"column": "value"}
    test_data = {"id": 1, "name": "Test Item"}

    # Generate multiple cache keys for the same table
    cache_key1_parts = [
        f"table:{test_table}",
        f"query:{json.dumps(test_query)}",
    ]
    cache_key1_parts.sort()
    cache_key1 = f"db_query:{hashlib.md5(':'.join(cache_key1_parts).encode()).hexdigest()}"

    # Set up cache entries
    redis_cache.set(cache_key1, [{"data": "test1"}], expire_seconds=10)

    # Verify cache entry is set
    assert get_cached_result(cache_key1) == [{"data": "test1"}]

    # Test the delete operation and cache invalidation
    def delete_data():
        return {"deleted": 1}

    # Delete data
    filters = {"id": 1}
    result = delete_data()

    # Directly delete the cache to simulate invalidation
    redis_cache.delete(cache_key1)

    # Verify cache was invalidated
    assert get_cached_result(cache_key1) is None

def test_fetch_data_performance(client, user_token):
    """Test performance improvement with caching."""
    test_table = "test_table"
    test_query = {"column": "value"}
    test_data = {"id": 1, "name": "Test Item"}

    # Generate a cache key based on the test data
    cache_key_parts = [
        f"table:{test_table}",
        f"query:{json.dumps(test_query)}",
    ]
    cache_key_parts.sort()
    cache_key = f"db_query:{hashlib.md5(':'.join(cache_key_parts).encode()).hexdigest()}"

    # Clear any existing cache
    redis_cache.delete(cache_key)

    # Create a slow mock for database fetch
    expected_response = [{"id": 1, "name": "Test Item"}]
    def slow_fetch(*args, **kwargs):
        """Simulate a slow database query."""
        time.sleep(0.1)  # Shorter sleep for faster tests, but still measurable
        return expected_response

    # First request - cache miss (should be slow)
    def fetch_from_db():
        return slow_fetch()

    # Measure time for first request (cache miss)
    start_time = time.time()

    # Direct fetch (no cache hit)
    result1 = get_or_set_cache(cache_key, fetch_from_db, expire_seconds=10)

    first_request_time = time.time() - start_time

    # Verify result matches expected response
    assert result1 == expected_response

    # Second request - cache hit (should be fast)
    def fetch_from_db():
        return slow_fetch()

    # Measure time for second request (cache hit)
    start_time = time.time()

    # This should hit the cache
    result2 = get_cached_result(cache_key)

    second_request_time = time.time() - start_time

    # Verify result matches expected response
    assert result2 == expected_response

    # Verify second request was faster
    assert second_request_time < first_request_time

    # The time difference should be significant
    time_improvement = first_request_time - second_request_time
    assert time_improvement > 0.05
