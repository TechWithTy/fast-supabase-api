import pytest
from fastapi import status
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_create_lead_rejects_xss_payload():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # XSS payload in name
        resp = await ac.post(
            "/api/leads/",
            json={"name": "<script>alert(1)</script>", "email": "bad@email.com"}
        )
        assert resp.status_code in (400, 422)
        # Should not echo input in response
        assert "<script>" not in resp.text

@pytest.mark.anyio
async def test_create_lead_rejects_sql_injection():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # SQL injection attempt in email
        resp = await ac.post(
            "/api/leads/",
            json={"name": "Good Name", "email": "test@example.com'; DROP TABLE users; --"}
        )
        assert resp.status_code in (400, 422)

@pytest.mark.anyio
async def test_create_lead_rejects_missing_required_fields():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Missing email
        resp = await ac.post(
            "/api/leads/",
            json={"name": "No Email"}
        )
        assert resp.status_code in (400, 422)

@pytest.mark.anyio
async def test_create_lead_rejects_invalid_email_format():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Invalid email format
        resp = await ac.post(
            "/api/leads/",
            json={"name": "Invalid Email", "email": "not-an-email"}
        )
        assert resp.status_code in (400, 422)

@pytest.mark.anyio
async def test_create_lead_rejects_long_name():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Name too long (assuming max 100 chars)
        resp = await ac.post(
            "/api/leads/",
            json={"name": "a" * 101, "email": "test@example.com"}
        )
        assert resp.status_code in (400, 422)
