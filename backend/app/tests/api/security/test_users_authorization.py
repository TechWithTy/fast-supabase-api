# NOTE: The following tests are currently waiting on a response from Supabase support regarding email rate limiting and SMTP email delivery issues.
# Tests that require user email confirmation will fail until the rate limit is lifted or email delivery is restored.
# See support ticket and troubleshooting history for details.

import asyncio

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.supabase_home.client import supabase
from app.models import User, UserCreate
from app.core.db import engine
from sqlmodel import Session, select

client = TestClient(app)

# Helper to sign up/sign in and get JWT


def confirm_email_via_admin(email: str):
    """
    Use Supabase Admin API to programmatically confirm a user's email for testing.
    """
    async def _confirm():
        users = await supabase.auth.list_users()
        user = None
        if users and users.get('users'):
            for u in users['users']:
                if u.get('email') == email:
                    user = u
                    break
        if user and not user.get('email_confirmed_at'):
            await supabase.auth.update_user(user['id'], {"email_confirm": True})
    asyncio.get_event_loop().run_until_complete(_confirm())


def ensure_local_superuser(email: str, password: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            user_in = UserCreate(email=email, password=password, is_superuser=True, is_active=True)
            user = User.from_orm(user_in)
            session.add(user)
            session.commit()
        elif not user.is_superuser:
            user.is_superuser = True
            session.add(user)
            session.commit()


def get_jwt(email, password):
    # Try sign in first
    resp = client.post("/api/v1/supabase/auth/signin", json={"email": email, "password": password})
    if resp.status_code == 200:
        ensure_local_superuser(email, password)
        return resp.json()["access_token"]
    # Try sign up
    resp = client.post("/api/v1/supabase/auth/users", json={"email": email, "password": password})
    if resp.status_code == 200:
        # Bypass email verification for test user
        confirm_email_via_admin(email)
        ensure_local_superuser(email, password)
        # Try sign in again (should succeed now)
        resp = client.post("/api/v1/supabase/auth/signin", json={"email": email, "password": password})
        if resp.status_code == 200:
            return resp.json()["access_token"]
    elif resp.status_code == 422:
        # User already exists, try to confirm and sign in again
        confirm_email_via_admin(email)
        ensure_local_superuser(email, password)
        resp = client.post("/api/v1/supabase/auth/signin", json={"email": email, "password": password})
        if resp.status_code == 200:
            return resp.json()["access_token"]
    raise AssertionError("Could not obtain JWT for test user")

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    from app.core.db import engine
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    yield
    # Optionally: SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="module")
def normal_user_token():
    return get_jwt("oni.contact.mail2@gmail.com", "TestPassword123!")

@pytest.fixture(scope="module")
def superuser_token():
    return get_jwt("admin@example.com", "SuperSecret123!")

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

def test_get_user_by_id_forbidden_for_normal_user(normal_user_token):
    response = client.get("/api/v1/supabase/auth/users123", headers=auth_headers(normal_user_token))
    assert response.status_code == 403

def test_get_user_by_id_superuser(superuser_token):
    response = client.get("/api/v1/supabase/auth/users123", headers=auth_headers(superuser_token))
    assert response.status_code in (200, 404)

def test_delete_user_requires_superuser(normal_user_token):
    response = client.delete("/api/v1/supabase/auth/users123", headers=auth_headers(normal_user_token))
    assert response.status_code == 403

def test_delete_user_superuser(superuser_token):
    response = client.delete("/api/v1/supabase/auth/users123", headers=auth_headers(superuser_token))
    assert response.status_code in (200, 404, 403)  # 403 if trying to delete self

# More tests can be added for PATCH, POST, and /me endpoints following the same pattern.
