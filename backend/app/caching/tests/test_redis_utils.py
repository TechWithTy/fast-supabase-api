import json
import time
import pytest
import hashlib
from unittest.mock import patch, MagicMock
from app.caching.utils.redis_cache import (
    cache_result,
    get_cached_result,
    get_or_set_cache,
    invalidate_cache,
    redis_cache,
)

@pytest.fixture(autouse=True)
def clear_redis_cache():
    redis_cache.flushdb()
    yield
    redis_cache.flushdb()

def test_get_cached_result_returns_none_for_missing_key():
    assert get_cached_result("nonexistent_key") is None

def test_get_or_set_cache_sets_and_gets_value():
    key = "test_get_or_set_key"
    value = {"foo": "bar"}
    def compute():
        return value
    # Should set and return value
    result = get_or_set_cache(key, compute, expire_seconds=5)
    assert result == value
    # Should get cached value
    cached = get_cached_result(key)
    assert cached == value or json.loads(cached.decode()) == value

def test_invalidate_cache_removes_key():
    key = "invalidate_test"
    redis_cache.set(key, b"some value")
    assert get_cached_result(key) is not None
    assert invalidate_cache(key) is True
    assert get_cached_result(key) is None

def test_cache_result_decorator_caches_result():
    calls = {"count": 0}
    @cache_result(expire_seconds=5, key_prefix="decorator_test")
    def slow_add(a, b):
        calls["count"] += 1
        return a + b
    result1 = slow_add(1, 2)
    result2 = slow_add(1, 2)
    assert result1 == 3
    assert result2 == 3
    assert calls["count"] == 1  # Only called once due to caching

def test_cache_result_decorator_cache_expires():
    calls = {"count": 0}
    @cache_result(expire_seconds=1, key_prefix="expire_test")
    def slow_mul(a, b):
        calls["count"] += 1
        return a * b
    result1 = slow_mul(2, 3)
    time.sleep(1.1)
    result2 = slow_mul(2, 3)
    assert result1 == 6
    assert result2 == 6
    assert calls["count"] == 2  # Called again after cache expired
