import logging
import time
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse

# NOTE: Replace this with your preferred FastAPI-compatible cache utility, e.g., aioredis or custom
from app.caching.utils.redis_cache import cache_result

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/expensive-api-example",
    response_model=dict[str, Any],
    summary="Expensive API Example",
    tags=["Caching Examples"],
)
@cache_result(timeout=60 * 15)  # Cache for 15 minutes
async def expensive_api_example() -> JSONResponse:
    """
    Example of caching an expensive API route using FastAPI.

    This demonstrates how to cache the entire response of an API endpoint
    that might be computationally expensive or time-consuming.
    """
    logger.info("Executing expensive API operation")
    # Simulate an expensive operation
    time.sleep(
        2
    )  # Simulate 2-second delay (replace with async sleep if using async cache)

    result = {
        "data": [
            {"id": 1, "name": "Item 1", "value": 100},
            {"id": 2, "name": "Item 2", "value": 200},
            {"id": 3, "name": "Item 3", "value": 300},
        ],
        "metadata": {"count": 3, "timestamp": time.time(), "source": "expensive_api"},
    }
    return JSONResponse(content=result)
