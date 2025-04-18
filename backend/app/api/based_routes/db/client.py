from fastapi import Depends, FastAPI

from ...supabase_home.auth import SupabaseAuthService
from ...supabase_home.client import SupabaseClient
from ...supabase_home.functions.database import SupabaseDatabaseService
from ...supabase_home.functions.edge_functions import SupabaseEdgeFunctionsService
from ...supabase_home.functions.realtime import SupabaseRealtimeService
from ...supabase_home.functions.storage import SupabaseStorageService

app = FastAPI(title="SupabaseClientBase", description="API to interact with current supabase client")


@app.get("/auth")
async def auth_endpoint(auth_service: SupabaseAuthService = Depends(SupabaseClient.get_auth_service)):
    # Implement auth logic here
    pass

@app.get("/database")
async def database_endpoint(db_service: SupabaseDatabaseService = Depends(SupabaseClient.get_database_service)):
    # Implement database logic here
    pass

@app.get("/storage")
async def storage_endpoint(storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)):
    # Implement storage logic here
    pass

@app.get("/edge-functions")
async def edge_functions_endpoint(edge_functions_service: SupabaseEdgeFunctionsService = Depends(SupabaseClient.get_edge_functions_service)):
    # Implement edge functions logic here
    pass

@app.get("/realtime")
async def realtime_endpoint(realtime_service: SupabaseRealtimeService = Depends(SupabaseClient.get_realtime_service)):
    # Implement realtime logic here
    pass
