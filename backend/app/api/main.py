from fastapi import APIRouter

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

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)

# SUPABASE endpoints
api_router.include_router(db_client_router)

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
