from fastapi import APIRouter, Depends, FastAPI
from fastapi_limiter.depends import RateLimiter

from app.supabase_home.client import SupabaseClient
from app.supabase_home.functions.auth import SupabaseAuthService
from app.supabase_home.functions.database import SupabaseDatabaseService
from app.supabase_home.functions.edge_functions import SupabaseEdgeFunctionsService
from app.supabase_home.functions.realtime import SupabaseRealtimeService
from app.supabase_home.functions.storage import SupabaseStorageService

app = FastAPI(
    title="SupabaseClientBase",
    description="API to interact with current supabase client",
)

router = APIRouter(tags=["Supabase Client"])


@app.get("/auth")
async def auth_endpoint(
    auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service),
):
    # Implement auth logic here
    pass


@app.get("/database")
async def database_endpoint(
    db_service: SupabaseDatabaseService = Depends(SupabaseClient.get_database_service),
):
    # Implement database logic here
    pass


@app.get("/storage")
async def storage_endpoint(
    storage_service: SupabaseStorageService = Depends(
        SupabaseClient.get_storage_service
    ),
):
    # Implement storage logic here
    pass


@app.get("/realtime")
async def realtime_endpoint(
    realtime_service: SupabaseRealtimeService = Depends(
        SupabaseClient.get_realtime_service
    ),
):
    # Implement realtime logic here
    pass


@router.get("/edge-functions", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def edge_functions_endpoint():
    """
    Public endpoint for testing rate limiting and security headers.
    Returns a simple JSON response.
    """
    return {"status": "ok"}
