import hashlib
import json
import logging
import os
import pickle
from collections.abc import Callable
from functools import wraps
from typing import Any, Optional, TypeVar

import redis

# Type variable for generic return types
T = TypeVar("T")

logger = logging.getLogger(__name__)

# Redis configuration (can be set via env vars for flexibility)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

redis_cache = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=False,  # We'll handle encoding/decoding
)


def get_cached_result(key: str, default: Any = None) -> Any:
    """
    Get a result from the Redis cache.

    Args:
        key: The cache key to retrieve
        default: Value to return if key is not found (default: None)

    Returns:
        The cached value or the default value if not found
    """
    try:
        value = redis_cache.get(key)
        if value is None:
            return default
        return pickle.loads(value)
    except Exception as e:
        logger.warning(f"Error retrieving from Redis cache: {str(e)}")
        return default


def invalidate_cache(key: str) -> bool:
    """
    Invalidate a specific cache key in Redis.

    Args:
        key: The cache key to invalidate

    Returns:
        True if the key was found and deleted, False otherwise
    """
    try:
        return bool(redis_cache.delete(key))
    except Exception as e:
        logger.warning(f"Error invalidating Redis cache: {str(e)}")
        return False


def get_or_set_cache(
    key: str, func: Callable[[], T], expire_seconds: int | None = None
) -> T:
    """
    Get a value from Redis, or compute and store it if not found.

    Args:
        key: The cache key to retrieve or store
        func: Function to call if the key is not in the cache
        expire_seconds: Optional cache expiration in seconds

    Returns:
        The cached or computed value
    """
    try:
        value = redis_cache.get(key)
        if value is not None:
            return pickle.loads(value)
        result = func()
        redis_cache.set(key, pickle.dumps(result), ex=expire_seconds)
        return result
    except Exception as e:
        logger.error(f"Error computing or caching result in Redis: {str(e)}")
        raise


def cache_result(expire_seconds: int | None = None, key_prefix: str = ""):
    """
    Decorator that caches the result of a function based on its arguments using Redis.

    Args:
        expire_seconds: Optional cache expiration in seconds
        key_prefix: Optional prefix for the cache key

    Returns:
        Decorated function that uses Redis caching
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key_args = json.dumps(args, sort_keys=True, default=str)
            key_kwargs = json.dumps(kwargs, sort_keys=True, default=str)
            raw_key = f"{key_prefix}:{func.__name__}:{key_args}:{key_kwargs}"
            key = hashlib.md5(raw_key.encode()).hexdigest()
            return get_or_set_cache(key, lambda: func(*args, **kwargs), expire_seconds)

        return wrapper

    return decorator
