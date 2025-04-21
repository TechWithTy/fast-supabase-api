from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils
from app.core.config import settings

# VAPI routers
from app.api.based_routes.vapi.assistants import router as vapi_assistants_router
from app.api.based_routes.vapi.calls import router as vapi_calls_router
from app.api.based_routes.vapi.webhooks import router as vapi_webhooks_router
from app.api.based_routes.vapi.voice import router as vapi_voice_router

# OSINT & MLS routers
from app.api.based_routes.osint.email import router as osint_email_router
from app.api.based_routes.osint.phone import router as osint_phone_router
from app.api.based_routes.osint.mls import router as mls_router

# ElevenLabs routers
from app.api.based_routes.eleven_labs.voice import router as elevenlabs_voice_router

# GHL routers (assuming your GHL endpoints are in these files)
from app.api.routes.ghl.create_subaccount import router as ghl_create_subaccount_router
from app.api.routes.ghl.upload_contact import router as ghl_upload_contact_router
from app.api.routes.ghl.apply_tag import router as ghl_apply_tag_router
from app.api.routes.ghl.schedule_appointment import router as ghl_schedule_appointment_router

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)

# VAPI endpoints
api_router.include_router(vapi_assistants_router)
api_router.include_router(vapi_calls_router)
api_router.include_router(vapi_webhooks_router)
api_router.include_router(vapi_voice_router)

# ElevenLabs endpoints
api_router.include_router(elevenlabs_voice_router)

# OSINT & MLS endpoints
api_router.include_router(osint_email_router)
api_router.include_router(osint_phone_router)
api_router.include_router(mls_router)

# GHL endpoints
api_router.include_router(ghl_create_subaccount_router)
api_router.include_router(ghl_upload_contact_router)
api_router.include_router(ghl_apply_tag_router)
api_router.include_router(ghl_schedule_appointment_router)

if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
