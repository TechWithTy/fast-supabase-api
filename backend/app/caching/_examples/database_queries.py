import logging
import time
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.caching.utils.redis_cache import cache_result, get_or_set_cache

logger = logging.getLogger(__name__)
router = APIRouter()


# Mock classes for demonstration
class MockOrder:
    @classmethod
    def objects(cls):
        return MockQuerySet()


class MockQuerySet:
    def filter(self, *args, **kwargs):
        return self

    def annotate(self, *args, **kwargs):
        return self

    def values(self, *args):
        return self

    def all(self):
        return self

    def select_related(self, *args):
        return self

    def prefetch_related(self, *args):
        return self

    def count(self):
        time.sleep(1)
        return 100

    def first(self):
        time.sleep(1)
        return {"id": 1, "total": 1000, "items": 5}

    def __iter__(self):
        time.sleep(1)
        for i in range(3):
            yield {"id": i, "total": i * 100, "items": i * 2}


Order = MockOrder


@router.get("/complex-query", summary="Cached Complex Query", tags=["Caching Examples"])
@cache_result(timeout=60 * 30)
async def cached_complex_query() -> JSONResponse:
    """
    Example of caching a complex database query with joins and aggregations.
    In a real application, this might be a complex report or dashboard query.
    """
    logger.info("Executing complex database query")
    # Example of a complex query that would be expensive to run frequently
    time.sleep(2)  # Simulate slow query
    results = [
        {"id": 1, "total_value": 1000, "item_count": 5, "avg_item_value": 200},
        {"id": 2, "total_value": 1500, "item_count": 7, "avg_item_value": 214},
        {"id": 3, "total_value": 800, "item_count": 3, "avg_item_value": 266},
    ]
    return JSONResponse(content={
        "results": results,
        "count": len(results),
        "timestamp": time.time()
    })


def get_user_order_stats(user_id: int) -> dict[str, Any]:
    """
    Example function that performs a complex query for a specific user.
    Demonstrates how to cache results for individual users/entities.
    """
    cache_key = f"user_order_stats:{user_id}"

    def get_stats():
        logger.info(f"Computing order stats for user {user_id}")
        # Mock data only, since we're not using Django ORM
        time.sleep(1.5)  # Simulate slow query
        return {
            "order_count": 12,
            "total_spent": 2345.67,
            "avg_order_value": 195.47,
        }

    return get_or_set_cache(cache_key, get_stats, timeout=60*60)


@router.get("/user-order-stats/{user_id}", summary="User Order Stats", tags=["Caching Examples"])
@cache_result(timeout=60 * 10)
async def user_order_stats_view(user_id: int) -> JSONResponse:
    """
    View that uses the cached user order stats function.
    Demonstrates how to use a cached function in a FastAPI view.
    """
    logger.info(f"Fetching order stats for user {user_id}")
    stats = get_user_order_stats(user_id)
    return JSONResponse(content={
        "user_id": user_id,
        "stats": stats,
        "timestamp": time.time()
    })
