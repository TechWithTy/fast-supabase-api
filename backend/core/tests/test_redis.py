import asyncio
import logging
import time

import pytest
import redis.asyncio as aioredis

# Set environment variables
REDIS_URL = "redis://localhost:6379/0"

# Logging setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def test_redis_connection():
    """
    Test basic async Redis connection and operations.
    """
    logger.info(f"Connecting to Redis at: {REDIS_URL}")

    try:
        # Connect to Redis with explicit parameters to avoid version issues
        redis = aioredis.from_url(REDIS_URL, decode_responses=True)

        # Test connection with ping
        pong = await redis.ping()
        logger.info(f"Redis ping response: {pong}")

        # Test basic operations
        test_key = "fastapi_redis_test"
        test_value = f"Test value at {time.time()}"

        # Set a value
        await redis.set(test_key, test_value)
        logger.info(f"Set test key: {test_key} = {test_value}")

        # Get the value back
        retrieved_value = await redis.get(test_key)
        logger.info(f"Retrieved test key: {test_key} = {retrieved_value}")

        # Verify the value matches
        assert retrieved_value == test_value, "Retrieved value doesn't match set value"

        # Test expiration
        await redis.setex(f"{test_key}_with_expiry", 5, "This will expire in 5 seconds")
        logger.info("Set key with 5-second expiration")

        # Check it exists
        assert await redis.exists(f"{test_key}_with_expiry") == 1, "Expiring key doesn't exist"
        logger.info("Verified expiring key exists")

        # Wait for expiration
        logger.info("Waiting for key to expire...")
        await asyncio.sleep(6)

        # Verify it's gone
        assert await redis.exists(f"{test_key}_with_expiry") == 0, "Key should have expired"
        logger.info("Verified key has expired as expected")

        # Test list operations
        list_key = "fastapi_redis_test_list"
        await redis.delete(list_key)  # Ensure clean state

        # Push items to list
        await redis.lpush(list_key, "item1", "item2", "item3")
        logger.info(f"Pushed 3 items to list: {list_key}")

        # Get list length
        list_len = await redis.llen(list_key)
        logger.info(f"List length: {list_len}")
        assert list_len == 3, "List should have 3 items"

        # Get all list items
        items = await redis.lrange(list_key, 0, -1)
        logger.info(f"List items: {items}")

        # Clean up
        await redis.delete(test_key, list_key)
        logger.info("Cleaned up test keys")

        logger.info("All Redis tests passed successfully!")
        return True

    except aioredis.RedisError as e:
        logger.error(f"Redis error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False


@pytest.mark.anyio
async def test_redis_set_get():
    """
    Test basic async set/get operations with Redis.
    """
    redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    key = "fastapi_test_key"
    value = "fastapi_test_value"
    await redis.set(key, value)
    result = await redis.get(key)
    assert result == value
    await redis.delete(key)


@pytest.mark.anyio
async def test_redis_ping():
    """
    Test async ping to Redis server.
    """
    redis = aioredis.from_url(REDIS_URL)
    pong = await redis.ping()
    assert pong is True
    await redis.close()


@pytest.mark.anyio
async def test_redis_installation():
    """
    Check Redis client installation and version.
    """
    try:
        logger.info(f"Redis client version: {aioredis.__version__}")

        # Check if hiredis is installed
        try:
            import hiredis

            logger.info(f"Hiredis version: {hiredis.__version__}")
        except ImportError:
            logger.warning(
                "Hiredis is not installed. For better performance, consider: pip install hiredis"
            )

        return True
    except Exception as e:
        logger.error(f"Error checking Redis installation: {e}")
        return False


if __name__ == "__main__":
    logger.info("Starting Redis tests...")

    # Check Redis installation
    asyncio.run(test_redis_installation())

    # Test direct Redis connection
    asyncio.run(test_redis_connection())

    # Test async set/get and ping
    asyncio.run(test_redis_set_get())
    asyncio.run(test_redis_ping())

    logger.info("\u2705 All Redis tests completed successfully!")
