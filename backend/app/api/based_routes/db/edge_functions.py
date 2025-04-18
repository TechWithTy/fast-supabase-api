from typing import Any

from fastapi import Depends, FastAPI, HTTPException

from .client import SupabaseClient
from .edge_functions import SupabaseEdgeFunctionsService

app = FastAPI(title="SupabaseEdgeFunctionsAPI", description="API to interact with current edge functions")

@app.post("/functions/{function_name}")
async def invoke_function(
    function_name: str,
    body: dict[str, Any] | None = None,
    edge_functions_service: SupabaseEdgeFunctionsService = Depends(SupabaseClient.get_edge_functions_service)
):
    try:
        response = edge_functions_service.invoke_function(
            function_name=function_name,
            body=body
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/functions")
async def list_functions(
    edge_functions_service: SupabaseEdgeFunctionsService = Depends(SupabaseClient.get_edge_functions_service)
):
    try:
        functions = edge_functions_service.list_functions()
        return functions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/functions")
async def create_function(
    name: str,
    source_code: str,
    verify_jwt: bool = True,
    import_map: dict[str, str] | None = None,
    edge_functions_service: SupabaseEdgeFunctionsService = Depends(SupabaseClient.get_edge_functions_service)
):
    try:
        response = edge_functions_service.create_function(
            name=name,
            source_code=source_code,
            verify_jwt=verify_jwt,
            import_map=import_map
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/functions/{function_name}")
async def delete_function(
    function_name: str,
    edge_functions_service: SupabaseEdgeFunctionsService = Depends(SupabaseClient.get_edge_functions_service)
):
    try:
        response = edge_functions_service.delete_function(function_name)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/functions/{function_name}")
async def get_function(
    function_name: str,
    edge_functions_service: SupabaseEdgeFunctionsService = Depends(SupabaseClient.get_edge_functions_service)
):
    try:
        function = edge_functions_service.get_function(function_name)
        return function
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/functions/{function_name}")
async def update_function(
    function_name: str,
    source_code: str | None = None,
    verify_jwt: bool | None = None,
    import_map: dict[str, str] | None = None,
    edge_functions_service: SupabaseEdgeFunctionsService = Depends(SupabaseClient.get_edge_functions_service)
):
    try:
        response = edge_functions_service.update_function(
            function_name=function_name,
            source_code=source_code,
            verify_jwt=verify_jwt,
            import_map=import_map
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
