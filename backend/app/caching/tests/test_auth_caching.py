# Refactored for FastAPI/pytest style
import hashlib
import time
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.caching.utils.redis_cache import get_cached_result, get_or_set_cache
from app.main import app

# Import the SupabaseAuthService directly (FastAPI style)
from app.supabase_home.functions.auth import SupabaseAuthService

auth_service = SupabaseAuthService()


@pytest.fixture(autouse=True)
def clear_cache():
    # Clear the cache before each test
    # If using a real cache backend, adapt this as needed
    try:
        from django.core.cache import cache

        cache.clear()
    except ImportError:
        pass
    yield
    try:
        from django.core.cache import cache

        cache.clear()
    except ImportError:
        pass


@pytest.fixture
def test_token(monkeypatch):
    # Mock user and token creation logic for FastAPI
    user_data = {"id": 1, "username": "testuser", "email": "test@example.com"}
    token = "testtoken123"
    monkeypatch.setattr(
        auth_service,
        "get_user_by_token",
        lambda t: user_data if t == token else Exception("Invalid token"),
    )
    return token, user_data


@pytest.fixture
def client():
    return TestClient(app)


def test_get_current_user_caching(test_token):
    token, expected_user_data = test_token
    token_hash = hashlib.md5(token.encode()).hexdigest()
    cache_key = f"user_info:{token_hash}"

    # Ensure cache is empty
    assert get_cached_result(cache_key) is None

    with patch.object(
        auth_service, "get_user_by_token", return_value=expected_user_data
    ) as mock_get_user:

        def fetch_func():
            return auth_service.get_user_by_token(token)

        # First request - cache miss
        result = get_or_set_cache(cache_key, fetch_func, timeout=300)
        mock_get_user.assert_called_once_with(token)
        assert result == expected_user_data
        # Now it's cached
        cached_result = get_cached_result(cache_key)
        assert cached_result == expected_user_data


def test_get_current_user_cache_hit(test_token):
    token, expected_user_data = test_token
    token_hash = hashlib.md5(token.encode()).hexdigest()
    cache_key = f"user_info:{token_hash}"
    # Manually set cache
    from django.core.cache import cache

    cache.set(cache_key, expected_user_data, timeout=300)
    assert get_cached_result(cache_key) == expected_user_data
    with patch.object(auth_service, "get_user_by_token") as mock_get_user:
        result = get_cached_result(cache_key)
        mock_get_user.assert_not_called()
        assert result == expected_user_data


def test_get_current_user_invalid_token():
    invalid_token = "invalid_token"
    token_hash = hashlib.md5(invalid_token.encode()).hexdigest()
    cache_key = f"user_info:{token_hash}"
    from django.core.cache import cache

    cache.delete(cache_key)
    with patch.object(auth_service, "get_user_by_token") as mock_get_user:
        mock_get_user.side_effect = Exception("Invalid token")

        def fetch_func():
            return auth_service.get_user_by_token(invalid_token)

        with pytest.raises(Exception):
            get_or_set_cache(cache_key, fetch_func, timeout=300)
        mock_get_user.assert_called_once_with(invalid_token)
        assert get_cached_result(cache_key) is None


def test_get_current_user_performance(test_token):
    token, expected_user_data = test_token
    token_hash = hashlib.md5(token.encode()).hexdigest()
    cache_key = f"user_info:{token_hash}"
    from django.core.cache import cache

    cache.delete(cache_key)

    def slow_get_user(*args, **kwargs):
        time.sleep(0.1)
        return expected_user_data

    with patch.object(auth_service, "get_user_by_token", side_effect=slow_get_user):
        start_time = time.time()

        def fetch_func():
            return auth_service.get_user_by_token(token)

        result1 = get_or_set_cache(cache_key, fetch_func, timeout=300)
        first_request_time = time.time() - start_time
        assert result1 == expected_user_data
    with patch.object(auth_service, "get_user_by_token", side_effect=slow_get_user):
        start_time = time.time()
        result2 = get_cached_result(cache_key)
        second_request_time = time.time() - start_time
        assert result2 == expected_user_data
    assert second_request_time < first_request_time
    assert (first_request_time - second_request_time) > 0.05
