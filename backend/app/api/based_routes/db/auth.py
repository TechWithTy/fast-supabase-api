from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

from ...supabase_home.auth import SupabaseAuthService
from ...supabase_home.client import SupabaseClient

app = FastAPI(title="Supabase Auth API", description="API for Supabase Authentication")



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
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                raise HTTPException(status_code=401, detail="Unauthorized")
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
@app.post("/auth/users", response_model=dict[str, Any])
@handle_supabase_error
async def create_user(
    user: UserCreate,
    auth_service: SupabaseAuthService = Depends(
        SupabaseClient.SupabaseClient.get_auth_service
    ),
):
    """Create a new user with email and password"""
    return auth_service.create_user(
        email=user.email, password=user.password, user_metadata=user.user_metadata
    )


@app.post("/auth/anonymous", response_model=dict[str, Any])
@handle_supabase_error
async def create_anonymous_user(
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Create an anonymous user"""
    return auth_service.create_anonymous_user()


@app.post("/auth/signin", response_model=dict[str, Any])
@handle_supabase_error
async def sign_in_with_email(
    user: UserSignIn,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Sign in a user with email and password"""
    return auth_service.sign_in_with_email(email=user.email, password=user.password)


@app.post("/auth/signin/otp", response_model=dict[str, Any])
@handle_supabase_error
async def sign_in_with_otp(
    user: UserOTP,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Send a one-time password to the user's email"""
    return auth_service.sign_in_with_otp(email=user.email)


@app.post("/auth/verify", response_model=dict[str, Any])
@handle_supabase_error
async def verify_otp(
    verify_data: OTPVerify,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Verify a one-time password and log in the user"""
    return auth_service.verify_otp(
        email=verify_data.email, token=verify_data.token, type=verify_data.type
    )


@app.post("/auth/oauth", response_model=dict[str, Any])
@handle_supabase_error
async def sign_in_with_oauth(
    oauth_data: OAuth,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Get the URL to redirect the user for OAuth sign-in"""
    return auth_service.sign_in_with_oauth(
        provider=oauth_data.provider, redirect_url=oauth_data.redirect_url
    )


@app.post("/auth/sso", response_model=dict[str, Any])
@handle_supabase_error
async def sign_in_with_sso(
    sso_data: SSO,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Sign in a user through SSO with a domain"""
    return auth_service.sign_in_with_sso(
        domain=sso_data.domain, redirect_url=sso_data.redirect_url
    )


@app.post("/auth/signout", response_model=dict[str, Any])
@handle_supabase_error
async def sign_out(
    auth_token: str,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Sign out a user"""
    return auth_service.sign_out(auth_token=auth_token)


@app.post("/auth/reset-password", response_model=dict[str, Any])
@handle_supabase_error
async def reset_password(
    reset_data: PasswordReset,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Send a password reset email to the user"""
    return auth_service.reset_password(
        email=reset_data.email, redirect_url=reset_data.redirect_url
    )


@app.get("/auth/session", response_model=dict[str, Any])
@handle_supabase_error
async def get_session(
    auth_token: str,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Retrieve the user's session"""
    return auth_service.get_session(auth_token=auth_token)


@app.post("/auth/refresh", response_model=dict[str, Any])
@handle_supabase_error
async def refresh_session(
    refresh_data: RefreshToken,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Refresh the user's session with a refresh token"""
    return auth_service.refresh_session(refresh_token=refresh_data.refresh_token)


@app.get("/auth/users/{user_id}", response_model=dict[str, Any])
@handle_supabase_error
async def get_user(
    user_id: str,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Retrieve a user by ID (admin only)"""
    return auth_service.get_user(user_id=user_id)


@app.put("/auth/users/{user_id}", response_model=dict[str, Any])
@handle_supabase_error
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Update a user's data (admin only)"""
    return auth_service.update_user(user_id=user_id, user_data=user_data.user_data)


@app.get("/auth/users/{user_id}/identities", response_model=list[dict[str, Any]])
@handle_supabase_error
async def get_user_identities(
    user_id: str,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Retrieve identities linked to a user (admin only)"""
    return auth_service.get_user_identities(user_id=user_id)


@app.post("/auth/identities/link", response_model=dict[str, Any])
@handle_supabase_error
async def link_identity(
    auth_token: str,
    link_data: LinkIdentity,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Link an identity to a user"""
    return auth_service.link_identity(
        auth_token=auth_token,
        provider=link_data.provider,
        redirect_url=link_data.redirect_url,
    )


@app.delete("/auth/identities/{identity_id}", response_model=dict[str, Any])
@handle_supabase_error
async def unlink_identity(
    auth_token: str,
    identity_id: str,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Unlink an identity from a user"""
    return auth_service.unlink_identity(auth_token=auth_token, identity_id=identity_id)


@app.put("/auth/session/data", response_model=dict[str, Any])
@handle_supabase_error
async def set_session_data(
    auth_token: str,
    session_data: SessionData,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Set the session data"""
    return auth_service.set_session_data(auth_token=auth_token, data=session_data.data)


@app.get("/auth/token/{token}", response_model=dict[str, Any])
@handle_supabase_error
async def get_user_by_token(
    token: str,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Get user information from a JWT token"""
    return auth_service.get_user_by_token(token=token)


@app.post("/auth/mfa/enroll", response_model=dict[str, Any])
@handle_supabase_error
async def enroll_mfa_factor(
    auth_token: str,
    mfa_data: MFAEnroll,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Enroll a multi-factor authentication factor"""
    return auth_service.enroll_mfa_factor(
        auth_token=auth_token, factor_type=mfa_data.factor_type
    )


@app.post("/auth/mfa/challenge", response_model=dict[str, Any])
@handle_supabase_error
async def create_mfa_challenge(
    auth_token: str,
    challenge_data: MFAChallenge,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Create a multi-factor authentication challenge"""
    return auth_service.create_mfa_challenge(
        auth_token=auth_token, factor_id=challenge_data.factor_id
    )


@app.post("/auth/mfa/verify", response_model=dict[str, Any])
@handle_supabase_error
async def verify_mfa_challenge(
    auth_token: str,
    verify_data: MFAVerify,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Verify a multi-factor authentication challenge"""
    return auth_service.verify_mfa_challenge(
        auth_token=auth_token,
        factor_id=verify_data.factor_id,
        challenge_id=verify_data.challenge_id,
        code=verify_data.code,
    )


@app.delete("/auth/mfa/{factor_id}", response_model=dict[str, Any])
@handle_supabase_error
async def unenroll_mfa_factor(
    auth_token: str,
    factor_id: str,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Unenroll a multi-factor authentication factor"""
    return auth_service.unenroll_mfa_factor(auth_token=auth_token, factor_id=factor_id)


@app.get("/auth/admin/users", response_model=dict[str, Any])
@handle_supabase_error
async def list_users(
    page: int = 1,
    per_page: int = 50,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """list all users (admin only)"""
    return auth_service.list_users(page=page, per_page=per_page)


@app.post("/auth/admin/users", response_model=dict[str, Any])
@handle_supabase_error
async def admin_create_user(
    user: UserCreate,
    email_confirm: bool = False,
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    """Create a new user with admin privileges"""
    return auth_service.admin_create_user(
        email=user.email,
        password=user.password,
        user_metadata=user.user_metadata,
        email_confirm=email_confirm,
    )
