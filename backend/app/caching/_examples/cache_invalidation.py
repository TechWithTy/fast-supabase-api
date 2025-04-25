import logging
import time
from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import asyncio
from app.caching.utils.redis_cache import invalidate_cache

logger = logging.getLogger(__name__)
router = APIRouter()

# Define cache key patterns for different model types
CACHE_KEYS = {
    'user': [
        'user_list',
        'user_count',
        'user_permissions:*',
    ],
    'product': [
        'product_list',
        'product_detail:*',
        'featured_products',
    ],
}

async def invalidate_model_caches(model_type: str, instance_id: Any = None) -> None:
    """
    Invalidate all caches related to a specific model type and optionally a specific instance.
    """
    if model_type not in CACHE_KEYS:
        return
    logger.info(f"Invalidating caches for {model_type} (id={instance_id})")
    cache_key_patterns = CACHE_KEYS[model_type]
    for pattern in cache_key_patterns:
        if '*' in pattern and instance_id is not None:
            specific_key = pattern.replace('*', str(instance_id))
            invalidate_cache(specific_key)
            logger.debug(f"Invalidated cache key: {specific_key}")
        else:
            invalidate_cache(pattern)
            logger.debug(f"Invalidated cache key: {pattern}")

# Versioned cache implementation
class VersionedCache:
    """
    Utility for managing versioned cache keys.
    Allows instant invalidation of all caches for a resource type by incrementing the version.
    """
    _versions = {}

    @classmethod
    def get_version(cls, resource_type: str) -> str:
        return str(cls._versions.get(resource_type, 1))

    @classmethod
    def increment_version(cls, resource_type: str) -> str:
        cls._versions[resource_type] = cls._versions.get(resource_type, 1) + 1
        logger.info(f"Incremented cache version for {resource_type}: {cls._versions[resource_type]}")
        return str(cls._versions[resource_type])

    @classmethod
    def get_key(cls, resource_type: str, key_suffix: str) -> str:
        version = cls.get_version(resource_type)
        return f"{resource_type}:{key_suffix}:v{version}"

# Example functions using versioned cache

async def get_cached_products(category: str = None) -> dict:
    """
    Get a list of products with versioned caching.
    """
    cache_key = VersionedCache.get_key('product', f"list:{category or 'all'}")
    # Simulate fetching from cache (replace with actual cache lookup)
    logger.info(f"Fetching products with cache key: {cache_key}")
    await asyncio.sleep(1)  # Simulate delay
    return {
        "products": [
            {"id": 1, "name": "Product 1", "category": category or "all"},
            {"id": 2, "name": "Product 2", "category": category or "all"},
        ],
        "cache_key": cache_key,
        "timestamp": time.time(),
    }

async def invalidate_product_cache() -> str:
    """
    Invalidate all product-related caches by incrementing the version.
    """
    new_version = VersionedCache.increment_version('product')
    return new_version

# API endpoints for demonstration
@router.get("/cached-products", summary="Get cached products", tags=["Caching Examples"])
async def cached_products_view(category: str = None) -> JSONResponse:
    """
    Endpoint returning cached products using versioned cache keys.
    """
    data = await get_cached_products(category)
    return JSONResponse(content=data)

@router.post("/invalidate-product-cache", summary="Invalidate product cache", tags=["Caching Examples"])
async def invalidate_product_cache_view() -> JSONResponse:
    """
    Endpoint that invalidates all product caches by incrementing the version.
    """
    new_version = await invalidate_product_cache()
    return JSONResponse(content={"message": "Product cache invalidated", "new_version": new_version})
