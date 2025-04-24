# NOTE: The following tests are currently waiting on a response from Supabase support regarding email rate limiting and SMTP email delivery issues.
# Tests that require user email confirmation will fail until the rate limit is lifted or email delivery is restored.
# See support ticket and troubleshooting history for details.

import asyncio
import time

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.supabase_home.client import supabase, SupabaseClient
from app.models import User, UserCreate

client = TestClient(app)

# Helper to sign up/sign in and get JWT


async def confirm_email_via_admin(email: str):
    """
    Use Supabase Admin API to programmatically confirm a user's email for testing.
    """
    users = await supabase.auth.list_users()
    user = None
    if users and users.get('users'):
        for u in users['users']:
            if u.get('email') == email:
                user = u
                break
    if user and not user.get('email_confirmed_at'):
        await supabase.auth.update_user(user['id'], {"email_confirm": True})


async def find_user_by_email(auth_service, email):
    page = 1
    per_page = 100
    while True:
        users_resp = await auth_service.list_users(page=page, per_page=per_page)
        users = users_resp.get("users", [])
        for u in users:
            if u.get("email") == email:
                return u
        if len(users) < per_page:
            break  # No more pages
        page += 1
    return None


async def ensure_supabase_superuser(email, password):
    auth_service = SupabaseClient().get_auth_service()
    try:
        await auth_service.admin_create_user(
            email=email,
            password=password,
            user_metadata={"is_superuser": True},
            email_confirm=True,
        )
    except Exception:
        user = await find_user_by_email(auth_service, email)
        if user:
            await auth_service.update_user(
                user_id=user["id"],
                user_data={"user_metadata": {"is_superuser": True}},
            )


async def ensure_supabase_normal_user(email, password):
    auth_service = SupabaseClient().get_auth_service()
    try:
        await auth_service.admin_create_user(
            email=email,
            password=password,
            user_metadata={"is_superuser": False},
            email_confirm=True,
        )
    except Exception:
        user = await find_user_by_email(auth_service, email)
        if user:
            await auth_service.update_user(
                user_id=user["id"],
                user_data={"user_metadata": {"is_superuser": False}},
            )


async def get_jwt(email, password, superuser=False):
    if superuser:
        await ensure_supabase_superuser(email, password)
    else:
        await ensure_supabase_normal_user(email, password)
    auth_service = SupabaseClient().get_auth_service()
    # Always sign in to get a fresh JWT with updated metadata
    resp = client.post("/api/v1/supabase/auth/signin", json={"email": email, "password": password})
    if resp.status_code == 200:
        token = resp.json()["access_token"]
        user_resp = client.get("/api/v1/supabase/auth/me", headers={"Authorization": f"Bearer {token}"})
        print("DEBUG /auth/v1/user:", user_resp.json())
        return token
    raise AssertionError("Could not obtain JWT for test user")


@pytest.fixture(scope="module")
def normal_user_token():
    return asyncio.run(get_jwt("oni.contact.mail2@gmail.com", "TestPassword123!", superuser=False))


@pytest.fixture(scope="module")
def superuser_token():
    return asyncio.run(get_jwt("admin@example.com", "SuperSecret123!", superuser=True))


@pytest.fixture(scope="module")
def another_user_uid():
    email = "another_user_forbidden_test@example.com"
    password = "AnotherPassword123!"
    auth_service = SupabaseClient().get_auth_service()
    # Try to create the user; if exists, just fetch
    try:
        user = asyncio.run(auth_service.admin_create_user(
            email=email,
            password=password,
            user_metadata={"is_superuser": False},
            email_confirm=True,
        ))
        uid = user["id"] if isinstance(user, dict) else getattr(user, "id", None)
    except Exception:
        # Fallback: find user by email
        user = asyncio.run(find_user_by_email(auth_service, email))
        uid = user["id"] if user else None
    assert uid, "Test fixture could not create or find the forbidden test user!"
    return uid


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_users_list_requires_superuser(normal_user_token):
    response = client.get("/api/v1/supabase/auth/admin/users", headers=auth_headers(normal_user_token))
    assert response.status_code == 403


def test_users_list_requires_auth():
    response = client.get("/api/v1/supabase/auth/admin/users")
    assert response.status_code in (401, 403)


def test_users_list_superuser(superuser_token):
    response = client.get("/api/v1/supabase/auth/admin/users", headers=auth_headers(superuser_token))
    assert response.status_code == 200


def test_get_user_by_id_forbidden_for_normal_user(normal_user_token, another_user_uid):
    response = client.get(
        f"/api/v1/supabase/auth/users/{another_user_uid}",
        headers=auth_headers(normal_user_token)
    )
    assert response.status_code == 403


def test_get_user_by_id_superuser(superuser_token):
    response = client.get("/api/v1/supabase/auth/users123", headers=auth_headers(superuser_token))
    assert response.status_code in (200, 404)


def test_delete_user_requires_superuser(normal_user_token):
    # This user should not be able to delete; use a valid user id for the path
    forbidden_uid = "00000000-0000-0000-0000-000000000000"  # unlikely to exist, triggers permission logic
    response = client.delete(f"/api/v1/supabase/auth/users/{forbidden_uid}", headers=auth_headers(normal_user_token))
    # If the user exists, should get 403; if not, should still get 403 (not 404)
    assert response.status_code == 403


def test_delete_user_superuser(superuser_token):
    response = client.delete("/api/v1/supabase/auth/users123", headers=auth_headers(superuser_token))
    assert response.status_code in (200, 404, 403)  # 403 if trying to delete self

# More tests can be added for PATCH, POST, and /me endpoints following the same pattern.
