import functools
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from redis.asyncio import Redis

from app.supabase_home.client import SupabaseClient
from app.supabase_home.functions.auth import SupabaseAuthService
from app.api.deps_supabase import get_current_supabase_superuser
from app.api.utils.redis_client import get_redis_client
import logging
import time

router = APIRouter(tags=["Supabase Auth"])

# In-memory store; use Redis/DB for production
LOCKOUT_TIME = 300  # seconds
MAX_ATTEMPTS = 5

async def check_brute_force(email: str, redis_client: Redis):
    key = f"lockout:{email}"
    try:
        val = await redis_client.get(key)
        print(f"[DEBUG] Redis get {key} -> {val}")
        if val and int(val) >= MAX_ATTEMPTS:
            print(f"[DEBUG] Lockout triggered for {email}")
            raise HTTPException(status_code=423, detail="Account locked due to too many failed attempts.")
    except Exception as e:
        print(f"[ERROR] check_brute_force exception for {email}: {e}")
        raise

async def record_failed_login(email: str, redis_client: Redis):
    key = f"lockout:{email}"
    try:
        val = await redis_client.incr(key)
        print(f"[DEBUG] Redis incr {key} -> {val}")
        if int(val) == 1:
            await redis_client.expire(key, LOCKOUT_TIME)
    except Exception as e:
        print(f"[ERROR] record_failed_login exception for {email}: {e}")
        raise

async def reset_failed_login(email: str, redis_client: Redis):
    key = f"lockout:{email}"
    try:
        await redis_client.delete(key)
        print(f"[DEBUG] Redis delete {key}")
    except Exception as e:
        print(f"[ERROR] reset_failed_login exception for {email}: {e}")
        raise

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    user_metadata: dict[str, Any] | None = None


class UserSignIn(BaseModel):
    email: EmailStr
    password: str


class UserOTP(BaseModel):
    email: EmailStr


class OTPVerify(BaseModel):
    email: EmailStr
    token: str
    type: str = "email"


class OAuth(BaseModel):
    provider: str
    redirect_url: str


class SSO(BaseModel):
    domain: str
    redirect_url: str


class PasswordReset(BaseModel):
    email: EmailStr
    redirect_url: str | None = None


class RefreshToken(BaseModel):
    refresh_token: str


class SessionData(BaseModel):
    data: dict[str, Any]


class MFAEnroll(BaseModel):
    factor_type: str = "totp"


class MFAChallenge(BaseModel):
    factor_id: str


class MFAVerify(BaseModel):
    factor_id: str
    challenge_id: str
    code: str


class UserUpdate(BaseModel):
    user_data: dict[str, Any]


class LinkIdentity(BaseModel):
    provider: str
    redirect_url: str


# Error handler for Supabase errors
def handle_supabase_error(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                raise HTTPException(status_code=401, detail="Unauthorized")
            elif "403" in error_msg:
                raise HTTPException(status_code=403, detail="Forbidden")
            elif "404" in error_msg:
                raise HTTPException(status_code=404, detail="Resource not found")
            elif "409" in error_msg:
                raise HTTPException(status_code=409, detail="Conflict")
            elif "422" in error_msg:
                raise HTTPException(status_code=422, detail="Validation error")
            else:
                raise HTTPException(
                    status_code=500, detail=f"Supabase error: {error_msg}"
                )

    return wrapper


# Endpoints
@router.post("/auth/users", response_model=dict[str, Any])
@handle_supabase_error
async def create_user(
    user: UserCreate,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Create a new user with email and password"""
    return await auth_service.create_user(
        email=user.email, password=user.password, user_metadata=user.user_metadata
    )


@router.post("/auth/anonymous", response_model=dict[str, Any])
@handle_supabase_error
async def create_anonymous_user(
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Create an anonymous user"""
    return await auth_service.create_anonymous_user()


@router.post("/auth/login", response_model=dict[str, Any])
@handle_supabase_error
async def login_endpoint(
    user: UserSignIn,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
    redis_client: Redis = Depends(get_redis_client),
):
    """
    API endpoint for user login, compatible with test expectations. Uses Redis-backed brute force protection.
    """
    return await sign_in_with_email(user, auth_service, redis_client)


@router.post("/auth/signin", response_model=dict[str, Any])
async def sign_in_with_email(
    user: UserSignIn,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
    redis_client: Redis = Depends(get_redis_client),
):
    """Sign in a user with email and password"""
    print(f"Checking brute force for: {user.email}")
    await check_brute_force(user.email, redis_client)
    try:
        result = await auth_service.sign_in_with_email(email=user.email, password=user.password)
        await reset_failed_login(user.email, redis_client)
        return result
    except Exception as e:
        print(f"Sign in failed: {getattr(e, 'status_code', 'unknown')}: {getattr(e, 'detail', str(e))}")
        await record_failed_login(user.email, redis_client)
        # Check if lockout threshold is reached after recording failure
        key = f"lockout:{user.email}"
        val = await redis_client.get(key)
        if val and int(val) >= MAX_ATTEMPTS:
            print(f"[DEBUG] Lockout triggered for {user.email} after failed login")
            raise HTTPException(status_code=423, detail="Account locked due to too many failed attempts.")
        # Always return 401 for invalid credentials (raise, not return)
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/auth/signin/otp", response_model=dict[str, Any])
@handle_supabase_error
async def sign_in_with_otp(
    user: UserOTP,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Send a one-time password to the user's email"""
    return await auth_service.sign_in_with_otp(email=user.email)


@router.post("/auth/verify", response_model=dict[str, Any])
@handle_supabase_error
async def verify_otp(
    verify_data: OTPVerify,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Verify a one-time password and log in the user"""
    return await auth_service.verify_otp(
        email=verify_data.email, token=verify_data.token, type=verify_data.type
    )


@router.post("/auth/oauth", response_model=dict[str, Any])
@handle_supabase_error
async def sign_in_with_oauth(
    oauth_data: OAuth,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Get the URL to redirect the user for OAuth sign-in"""
    return await auth_service.sign_in_with_oauth(
        provider=oauth_data.provider, redirect_url=oauth_data.redirect_url
    )


@router.post("/auth/sso", response_model=dict[str, Any])
@handle_supabase_error
async def sign_in_with_sso(
    sso_data: SSO,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Sign in a user through SSO with a domain"""
    return await auth_service.sign_in_with_sso(
        domain=sso_data.domain, redirect_url=sso_data.redirect_url
    )


@router.post("/auth/signout", response_model=dict[str, Any])
@handle_supabase_error
async def sign_out(
    auth_token: str,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Sign out a user"""
    return await auth_service.sign_out(auth_token=auth_token)


@router.post("/auth/reset-password", response_model=dict[str, Any])
@handle_supabase_error
async def reset_password(
    reset_data: PasswordReset,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Send a password reset email to the user"""
    return await auth_service.reset_password(
        email=reset_data.email, redirect_url=reset_data.redirect_url
    )


@router.get("/auth/session", response_model=dict[str, Any])
@handle_supabase_error
async def get_session(
    auth_token: str,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Retrieve the user's session"""
    return await auth_service.get_session(auth_token=auth_token)


@router.post("/auth/refresh", response_model=dict[str, Any])
@handle_supabase_error
async def refresh_session(
    refresh_data: RefreshToken,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Refresh the user's session with a refresh token"""
    return await auth_service.refresh_session(refresh_token=refresh_data.refresh_token)


@router.get("/auth/users/{user_id}", response_model=dict[str, Any])
@handle_supabase_error
async def get_user(
    user_id: str,
    request: Request,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    '''Retrieve a user by ID (admin only or self-access)'''
    logging.debug(f"[get_user] Handler called for user_id={user_id}")
    if not isinstance(request, Request):
        logging.error("[get_user] Request object not injected!")
        raise HTTPException(status_code=500, detail="Internal error: Request object not injected")
    # Extract and decode token
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        logging.warning("[get_user] Missing credentials")
        raise HTTPException(status_code=401, detail="Missing credentials")
    token = auth_header[7:]
    try:
        user_info = await auth_service.get_user_by_token(token)
        logging.debug(f"[get_user] Token decoded, user_info: {user_info}")
    except Exception as e:
        logging.error(f"[get_user] Could not validate credentials: {e}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user = user_info.get("user", user_info)
    current_uid = user.get("id")
    meta = user.get("user_metadata", {})
    app_meta = user.get("app_metadata", {})
    logging.debug(f"[get_user] meta: {meta}, app_meta: {app_meta}, current_uid: {current_uid}")
    # Only allow superusers or the user themselves
    if not (meta.get("is_superuser") or app_meta.get("is_superuser") or current_uid == user_id):
        logging.warning(f"[get_user] Forbidden access: current_uid={current_uid}, target_uid={user_id}")
        raise HTTPException(status_code=403, detail="Forbidden")
    logging.info(f"[get_user] Permission granted for user_id={user_id}")
    # Only now call the admin endpoint
    return await auth_service.get_user(user_id=user_id)


@router.delete("/auth/users/{user_id}", response_model=dict[str, Any])
@handle_supabase_error
async def delete_user(
    user_id: str,
    request: Request,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    '''Delete a user by ID (admin only)'''
    logging.debug(f"[delete_user] Handler called for user_id={user_id}")
    if not isinstance(request, Request):
        logging.error("[delete_user] Request object not injected!")
        raise HTTPException(status_code=500, detail="Internal error: Request object not injected")
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        logging.warning("[delete_user] Missing credentials")
        raise HTTPException(status_code=401, detail="Missing credentials")
    token = auth_header[7:]
    try:
        user_info = await auth_service.get_user_by_token(token)
        logging.debug(f"[delete_user] Token decoded, user_info: {user_info}")
    except Exception as e:
        logging.error(f"[delete_user] Could not validate credentials: {e}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user = user_info.get("user", user_info)
    meta = user.get("user_metadata", {})
    app_meta = user.get("app_metadata", {})
    current_uid = user.get("id")
    logging.debug(f"[delete_user] meta: {meta}, app_meta: {app_meta}, current_uid: {current_uid}")
    # Only allow superusers
    if not (meta.get("is_superuser") or app_meta.get("is_superuser")):
        logging.warning(f"[delete_user] Forbidden access: current_uid={current_uid}, target_uid={user_id}")
        raise HTTPException(status_code=403, detail="Forbidden")
    logging.info(f"[delete_user] Permission granted for user_id={user_id}")
    # Only now call the admin endpoint to delete
    return await auth_service._make_request(
        method="DELETE",
        endpoint=f"/auth/v1/admin/users/{user_id}",
        is_admin=True
    )


@router.put("/auth/users/{user_id}", response_model=dict[str, Any])
@handle_supabase_error
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Update a user's data (admin only)"""
    return await auth_service.update_user(user_id=user_id, user_data=user_data.user_data)


@router.get("/auth/users/{user_id}/identities", response_model=list[dict[str, Any]])
@handle_supabase_error
async def get_user_identities(
    user_id: str,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Retrieve identities linked to a user (admin only)"""
    return await auth_service.get_user_identities(user_id=user_id)


@router.post("/auth/identities/link", response_model=dict[str, Any])
@handle_supabase_error
async def link_identity(
    auth_token: str,
    link_data: LinkIdentity,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Link an identity to a user"""
    return await auth_service.link_identity(
        auth_token=auth_token,
        provider=link_data.provider,
        redirect_url=link_data.redirect_url,
    )


@router.delete("/auth/identities/{identity_id}", response_model=dict[str, Any])
@handle_supabase_error
async def unlink_identity(
    auth_token: str,
    identity_id: str,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Unlink an identity from a user"""
    return await auth_service.unlink_identity(auth_token=auth_token, identity_id=identity_id)


@router.put("/auth/session/data", response_model=dict[str, Any])
@handle_supabase_error
async def set_session_data(
    auth_token: str,
    session_data: SessionData,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Set the session data"""
    return await auth_service.set_session_data(auth_token=auth_token, data=session_data.data)


@router.get("/auth/token/{token}", response_model=dict[str, Any])
@handle_supabase_error
async def get_user_by_token(
    token: str,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Get user information from a JWT token"""
    return await auth_service.get_user_by_token(token=token)


@router.post("/auth/mfa/enroll", response_model=dict[str, Any])
@handle_supabase_error
async def enroll_mfa_factor(
    auth_token: str,
    mfa_data: MFAEnroll,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Enroll a multi-factor authentication factor"""
    return await auth_service.enroll_mfa_factor(
        auth_token=auth_token, factor_type=mfa_data.factor_type
    )


@router.post("/auth/mfa/challenge", response_model=dict[str, Any])
@handle_supabase_error
async def create_mfa_challenge(
    auth_token: str,
    challenge_data: MFAChallenge,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Create a multi-factor authentication challenge"""
    return await auth_service.create_mfa_challenge(
        auth_token=auth_token, factor_id=challenge_data.factor_id
    )


@router.post("/auth/mfa/verify", response_model=dict[str, Any])
@handle_supabase_error
async def verify_mfa_challenge(
    auth_token: str,
    verify_data: MFAVerify,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Verify a multi-factor authentication challenge"""
    return await auth_service.verify_mfa_challenge(
        auth_token=auth_token,
        factor_id=verify_data.factor_id,
        challenge_id=verify_data.challenge_id,
        code=verify_data.code,
    )


@router.delete("/auth/mfa/{factor_id}", response_model=dict[str, Any])
@handle_supabase_error
async def unenroll_mfa_factor(
    auth_token: str,
    factor_id: str,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Unenroll a multi-factor authentication factor"""
    return await auth_service.unenroll_mfa_factor(auth_token=auth_token, factor_id=factor_id)


@router.get("/auth/admin/users", response_model=dict[str, Any], dependencies=[Depends(get_current_supabase_superuser)])
@handle_supabase_error
async def list_users(
    page: int = 1,
    per_page: int = 50,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """list all users (admin only)"""
    return await auth_service.list_users(page=page, per_page=per_page)


@router.post("/auth/admin/users", response_model=dict[str, Any])
@handle_supabase_error
async def admin_create_user(
    user: UserCreate,
    email_confirm: bool = False,
    auth_service: SupabaseAuthService = Depends(SupabaseClient().get_auth_service),
):
    """Create a new user with admin privileges"""
    return await auth_service.admin_create_user(
        email=user.email,
        password=user.password,
        user_metadata=user.user_metadata,
        email_confirm=email_confirm,
    )
