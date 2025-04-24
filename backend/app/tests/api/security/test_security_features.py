"""
Security Feature Tests:
- Brute Force/Lockout
- CSRF
- RLS (Row-Level Security)
- OAuth Scope
- Replay Attack (Webhooks)
- File Upload Security
- Error Handling

All tests are isolated and should be run with a clean test database. Any required backend implementation is marked as TODO if not present.
"""

import os
import pytest
from fastapi.testclient import TestClient
from asgi_lifespan import LifespanManager

from app.api.main import app  # CRITICAL: use the app with lifespan handler
from app.tests.api.security.test_users_authorization import auth_headers, get_jwt
from app.tests.utils.env_loader import load_env

load_env()

ADMIN_EMAIL = os.getenv("ADMIN_TEST_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_TEST_PASSWORD", "AdminPassword123!")
USER_EMAIL = os.getenv("USER_TEST_EMAIL", "user@example.com")
USER_PASSWORD = os.getenv("USER_TEST_PASSWORD", "UserPassword123!")

# # --- List Registered Routes (Debug) ---
# def test_list_routes():
#     print("\nRegistered routes:", [route.path for route in app.routes])


# --- Brute Force/Lockout (Redis-backed) ---
@pytest.mark.anyio
async def test_brute_force_lockout_redis():
    """
    Simulate repeated failed login attempts using Redis backend. After N failures, login should be locked.
    """
    email = USER_EMAIL

    async with LifespanManager(app):
        redis_client = app.state.redis_client
        await redis_client.delete(f"lockout:{email}")  # ensure clean state

        with TestClient(app) as client:
            for _ in range(6):
                resp = client.post(
                    "/api/v1/supabase/auth/signin",
                    json={"email": email, "password": "wrong"},
                )
            assert resp.status_code == 423
            assert "lock" in resp.text.lower()

        await redis_client.delete(f"lockout:{email}")


# --- CSRF Protection ---
@pytest.mark.anyio
async def test_csrf_token_required_on_state_change():
    """
    Simulate PUT to update user without CSRF token. Should be rejected.
    """
    token = get_jwt(USER_EMAIL, USER_PASSWORD)
    headers = auth_headers(token)
    user_id = 1
    async with LifespanManager(app):
        with TestClient(app) as client:
            resp = client.put(
                f"/api/v1/supabase/auth/users/{user_id}",
                json={"user_data": {"name": "hacker"}},
                headers=headers,
            )
            assert resp.status_code in (403, 422)
            assert "csrf" in resp.text.lower()


# --- RLS (Row-Level Security) ---
@pytest.mark.anyio
async def test_rls_user_cannot_access_others():
    """
    Try to fetch/update/delete another user's resource. Should be forbidden.
    """
    token = get_jwt(ADMIN_EMAIL, ADMIN_PASSWORD)
    headers = auth_headers(token)
    async with LifespanManager(app):
        with TestClient(app) as client:
            resp = client.get("/api/v1/supabase/leads/other-user-id", headers=headers)
            assert resp.status_code in (403, 404)
            resp2 = client.delete("/api/v1/supabase/leads/other-user-id", headers=headers)
            assert resp2.status_code in (403, 404)


# --- OAuth Scope ---
def test_oauth_scope_enforced():
    """
    Use a token with insufficient scope to access a protected resource. Should be denied.
    """
    # Simulate a limited-scope token
    limited_scope_token = "dummy-oauth-token-without-scope"
    headers = auth_headers(limited_scope_token)
    with TestClient(app) as client:
        resp = client.get(
            "/api/v1/supabase/integrations/protected-resource", headers=headers
        )
        assert resp.status_code == 403
        assert "scope" in resp.text.lower()


# --- Replay Attack (Redis-backed) ---
@pytest.mark.anyio
async def test_webhook_replay_attack_redis():
    """
    Send a webhook with a reused nonce. Should be rejected on second use (Redis-backed).
    """
    token = get_jwt(ADMIN_EMAIL, ADMIN_PASSWORD)
    headers = auth_headers(token)
    from uuid import uuid4

    nonce = str(uuid4())
    webhook_url = "/api/v1/vapi/calls/status-webhook"
    payload = {"call_id": nonce, "status": "completed"}
    # Add CSRF token header since middleware is enabled
    headers["x-csrf-token"] = "test-csrf-token"
    async with LifespanManager(app):
        with TestClient(app) as client:
            resp1 = client.post(webhook_url, json=payload, headers=headers)
            assert resp1.status_code in (200, 204)
            resp2 = client.post(webhook_url, json=payload, headers=headers)
            # Should be rejected as a replay (simulate by expecting 409 or similar)
            assert resp2.status_code in (409, 400, 422)
            assert "replay" in resp2.text.lower() or "nonce" in resp2.text.lower() or "already" in resp2.text.lower()


# --- File Upload Security ---
def test_file_upload_rejects_dangerous_or_oversized():
    """
    Upload a dangerous file (e.g., .exe) or oversized file. Should be rejected.
    """
    token = get_jwt(USER_EMAIL, USER_PASSWORD)
    headers = auth_headers(token)
    files = {"file": ("evil.exe", b"MZ...", "application/octet-stream")}
    with TestClient(app) as client:
        resp = client.post("/api/v1/upload", files=files, headers=headers)
        assert resp.status_code in (400, 413, 422)
        assert "file" in resp.text.lower() and (
            "danger" in resp.text.lower() or "size" in resp.text.lower()
        )


# --- Error Handling ---
def test_error_responses_do_not_leak_sensitive_info():
    """
    Trigger an error and check that response does not include stack trace or sensitive info.
    """
    token = get_jwt(USER_EMAIL, USER_PASSWORD)
    headers = auth_headers(token)
    with TestClient(app) as client:
        resp = client.get("/api/v1/trigger-error", headers=headers)
        assert resp.status_code >= 400
        assert "traceback" not in resp.text.lower()
        assert "error" in resp.text.lower() or "message" in resp.text.lower()
        assert not any(
            word in resp.text.lower()
            for word in ["password", "supabase", "localhost", "sql", "env", "secret"]
        )
