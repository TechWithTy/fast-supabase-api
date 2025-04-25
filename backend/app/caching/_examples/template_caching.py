import logging
import time

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

from app.caching.utils.redis_cache import get_or_set_cache

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/cached-template", response_class=HTMLResponse, summary="Cached Template Example", tags=["Caching Examples"])
async def cached_template_view() -> HTMLResponse:
    """
    Example endpoint that caches the entire rendered template.
    Useful for pages that are expensive to render but don't change frequently.
    """
    logger.info("Gathering data for template rendering")
    time.sleep(1)  # Simulate slow operation
    context = {
        "title": "Cached Template Example",
        "items": [
            {"name": "Item 1", "value": 100},
            {"name": "Item 2", "value": 200},
            {"name": "Item 3", "value": 300},
        ],
        "timestamp": time.time(),
    }
    # For demonstration, return an HTML string
    html = f"<html><body><h1>{context['title']}</h1><p>Time: {context['timestamp']}</p></body></html>"
    return HTMLResponse(content=html)


@router.get("/cached-template-fragment", response_class=HTMLResponse, summary="Cached Template Fragment", tags=["Caching Examples"])
async def cached_template_fragment(user_id: str = "anonymous") -> HTMLResponse:
    """
    Endpoint that demonstrates caching template fragments.
    Useful when only parts of a page are expensive to render.
    """
    def get_expensive_fragment():
        logger.info("Computing expensive template fragment")
        time.sleep(1.5)  # Simulate slow operation
        return "<div class='expensive-fragment'>This part was expensive to render</div>"
    expensive_fragment = get_or_set_cache(
        f"template_fragment:expensive:{user_id}",
        get_expensive_fragment,
        timeout=60 * 60,
    )
    personalized_content = f"<div>Hello, User {user_id}! Current time: {time.time()}</div>"
    html = f"""<html>
    <body>
        <h1>Template Fragment Caching Example</h1>
        {personalized_content}
        {expensive_fragment}
        <p>This page combines cached and non-cached content.</p>
    </body>
    </html>"""
    return HTMLResponse(content=html)


class VersionedTemplateCache:
    _version = 1

    @classmethod
    def get_version(cls) -> int:
        return cls._version

    @classmethod
    def increment_version(cls) -> int:
        cls._version += 1
        logger.info(f"Template cache version incremented to {cls._version}")
        return cls._version

    @classmethod
    def get_key(cls, key_suffix: str) -> str:
        return f"template:{key_suffix}:v{cls._version}"


@router.get("/versioned-template-caching", response_class=HTMLResponse, summary="Versioned Template Caching", tags=["Caching Examples"])
async def versioned_template_caching() -> HTMLResponse:
    """
    Endpoint that demonstrates versioned template caching.
    Useful when you need to invalidate all cached templates when the template design changes.
    """
    cache_key = VersionedTemplateCache.get_key("main")
    logger.info(f"Rendering with cache key: {cache_key}")
    html = f"<html><body><h1>Versioned Template Caching</h1><p>Cache key: {cache_key}</p></body></html>"
    return HTMLResponse(content=html)


@router.post("/invalidate-template-cache", response_class=JSONResponse, summary="Invalidate Template Cache", tags=["Caching Examples"])
async def invalidate_template_cache() -> JSONResponse:
    """
    Endpoint that invalidates all cached templates by updating the template version.
    """
    new_version = VersionedTemplateCache.increment_version()
    return JSONResponse(content={"message": "Template cache invalidated", "new_version": new_version})
