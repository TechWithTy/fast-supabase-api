import os
from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# SUPABASE
from app.api.based_routes.db.auth import router as db_auth_router
from app.api.based_routes.db.client import router as db_client_router
from app.api.based_routes.db.database import router as db_database_router
from app.api.based_routes.db.edge_functions import router as db_edge_functions_router
from app.api.based_routes.db.real_time import router as db_real_time_router
from app.api.based_routes.db.storage import router as db_storage_router

# ElevenLabs routers
from app.api.based_routes.eleven_labs.voice import router as elevenlabs_voice_router
from app.api.based_routes.ghl.apply_tag import router as ghl_apply_tag_router

# GHL routers (assuming your GHL endpoints are in these files)
from app.api.based_routes.ghl.create_subaccount import (
    router as ghl_create_subaccount_router,
)
from app.api.based_routes.ghl.schedule_appointment import (
    router as ghl_schedule_appointment_router,
)
from app.api.based_routes.ghl.upload_contact import router as ghl_upload_contact_router
from app.api.based_routes.osint.mls import router as mls_router
from app.api.based_routes.osint.phone import router as osint_phone_router

# OSINT & MLS routers
from app.api.based_routes.osint.zehef import router as zehef_router

# VAPI routers
from app.api.based_routes.vapi.assistants import router as vapi_assistants_router
from app.api.based_routes.vapi.calls import router as vapi_calls_router
from app.api.based_routes.vapi.voice import router as vapi_voice_router
from app.api.based_routes.vapi.webhooks import router as vapi_webhooks_router
from app.api.routes.db import items, login, private, users, utils
from app.core.config import settings

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


@asynccontextmanager
async def lifespan(app):
    print("LIFESPAN: Starting up, connecting to Redis...")
    app.state.redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    yield
    print("LIFESPAN: Shutting down, closing Redis...")
    await app.state.redis_client.close()


class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Only enforce CSRF on state-changing methods
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            # Allow exceptions for authentication endpoints (sign-in, login, etc.)
            if request.url.path.startswith("/api/v1/supabase/auth/signin") or request.url.path.startswith("/api/v1/supabase/auth/login"):
                return await call_next(request)
            csrf_token = request.headers.get("x-csrf-token")
            if not csrf_token or not await self.validate_csrf_token(csrf_token, request):
                return JSONResponse(
                    status_code=403, content={"detail": "CSRF token missing or invalid"}
                )
        return await call_next(request)

    async def validate_csrf_token(self, token, request):
        # For now, accept a static token for test, but allow override for future real validation
        # In production, tie token to session/user and store in httpOnly cookie or server-side
        return token == "test-csrf-token"


app = FastAPI(lifespan=lifespan)
app.add_middleware(CSRFMiddleware)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback

    print("EXCEPTION:", exc)
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"error": "An internal error occurred. Please contact support."},
    )


api_router = APIRouter()


# SUPABASE/POSTGRES endpoints conditional inclusion
if getattr(settings, "SUPABASE_URL", False):
    api_router.include_router(db_auth_router, prefix="/supabase")
    api_router.include_router(db_client_router, prefix="/supabase")
    api_router.include_router(db_database_router, prefix="/supabase")
    api_router.include_router(db_edge_functions_router, prefix="/supabase")
    api_router.include_router(db_real_time_router, prefix="/supabase")
    api_router.include_router(db_storage_router, prefix="/supabase")
elif getattr(settings, "POSTGRES_SERVER", None):
    api_router.include_router(login.router)
    api_router.include_router(users.router)
    api_router.include_router(utils.router)
    api_router.include_router(items.router)
    pass
else:
    raise RuntimeError(
        "No database backend configured. Set either Postgres or Supabase environment variables."
    )

# VAPI endpoints
api_router.include_router(vapi_assistants_router)
api_router.include_router(vapi_calls_router)
api_router.include_router(vapi_webhooks_router)
api_router.include_router(vapi_voice_router)

# ElevenLabs endpoints
api_router.include_router(elevenlabs_voice_router)

# OSINT & MLS endpoints
api_router.include_router(zehef_router, prefix="/osint/zehef")
api_router.include_router(osint_phone_router)
api_router.include_router(mls_router)

# GHL endpoints
api_router.include_router(ghl_create_subaccount_router)
api_router.include_router(ghl_upload_contact_router)
api_router.include_router(ghl_apply_tag_router)
api_router.include_router(ghl_schedule_appointment_router)

if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)

app.include_router(api_router, prefix="/api/v1")
