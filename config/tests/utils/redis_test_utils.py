import redis
import logging
import time
import os
from typing import Optional

try:
    # Try to import FastAPI settings if available
    from app.config.config import settings
except ImportError:
    settings = None

logger = logging.getLogger(__name__)

def get_redis_url() -> str:
    """
    Get the Redis URL from FastAPI settings or environment variable.
    """
    if settings and hasattr(settings, 'redis_url') and settings.redis_url:
        return settings.redis_url
    return os.getenv('REDIS_URL', 'redis://localhost:6379/1')

def ensure_redis_connection(max_retries: int = 3, retry_interval: int = 2) -> bool:
    """
    Ensures a Redis connection is available before running tests.
    Returns True if connection is successful, False otherwise.
    Args:
        max_retries: Maximum number of retry attempts
        retry_interval: Time interval in seconds between retries
    """
    retries = 0
    redis_url = get_redis_url()
    while retries < max_retries:
        try:
            logger.info(f"Attempting to connect to Redis at {redis_url}")
            # Clean up the redis URL if it has the redis:// prefix
            url_no_prefix = redis_url[len('redis://'):] if redis_url.startswith('redis://') else redis_url
            # Parse host and port from URL
            if '/' in url_no_prefix:
                host_port, db = url_no_prefix.rsplit('/', 1)
            else:
                host_port, db = url_no_prefix, '0'
            if ':' in host_port:
                host, port = host_port.split(':')
            else:
                host, port = host_port, '6379'
            # Try to connect directly with redis-py
            r = redis.Redis(host=host, port=int(port), db=int(db), socket_timeout=5)
            r.ping()  # Raises exception if connection fails
            # Direct Redis set/get test
            r.set('redis_test_key', 'test_value', ex=10)
            test_value = r.get('redis_test_key')
            if test_value != b'test_value':
                raise Exception(f"Redis test failed: got {test_value} instead of 'test_value'")
            logger.info("✅ Redis connection successful!")
            return True
        except Exception as e:
            logger.warning(f"Redis connection attempt {retries+1} failed: {str(e)}")
            retries += 1
            if retries < max_retries:
                logger.info(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
    logger.error(f"❌ Could not connect to Redis after {max_retries} attempts")
    return False
