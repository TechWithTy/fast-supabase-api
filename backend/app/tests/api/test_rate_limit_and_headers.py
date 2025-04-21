"""
Tests for rate limiting and security headers middleware.
"""
import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app

@pytest.mark.asyncio
async def test_rate_limit_exceeded():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Exceed the rate limit for GET /api/v1/users/
        responses = []
        for _ in range(12):
            resp = await ac.get("/api/v1/users/")
            responses.append(resp)
        # The last two should be 429 Too Many Requests
        assert any(r.status_code == status.HTTP_429_TOO_MANY_REQUESTS for r in responses[-2:])

@pytest.mark.asyncio
async def test_security_headers_present():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/api/v1/users/")
        assert resp.headers["X-Content-Type-Options"] == "nosniff"
        assert resp.headers["X-Frame-Options"] == "DENY"
        assert resp.headers["Strict-Transport-Security"].startswith("max-age=")
        assert resp.headers["Referrer-Policy"] == "no-referrer"
        assert resp.headers["Permissions-Policy"] is not None
        assert resp.headers["X-XSS-Protection"] == "1; mode=block"
