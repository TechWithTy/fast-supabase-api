from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .client import SupabaseClient
from .database import SupabaseDatabaseService

app = FastAPI(title="SupabaseDatabaseAPI", description="API to interact with current database")

class DataFilter(BaseModel):
    filters: dict[str, Any] | None = None
    order: str | None = None
    limit: int | None = None
    offset: int | None = None

class InsertData(BaseModel):
    data: dict[str, Any] | list[dict[str, Any]]
    upsert: bool = False

class UpdateData(BaseModel):
    data: dict[str, Any]
    filters: dict[str, Any]

class DeleteFilter(BaseModel):
    filters: dict[str, Any]

class FunctionCall(BaseModel):
    params: dict[str, Any] | None = None

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": f"An error occurred: {str(exc)}"}
    )

@app.get("/data/{table}")
async def fetch_data(
    table: str,
    select: str = "*",
    filter_data: DataFilter = Depends(),
    db_service: SupabaseDatabaseService = Depends(SupabaseClient.get_database_service)
):
    try:
        return db_service.fetch_data(
            table,
            select=select,
            filters=filter_data.filters,
            order=filter_data.order,
            limit=filter_data.limit,
            offset=filter_data.offset
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/data/{table}")
async def insert_data(
    table: str,
    insert_data: InsertData,
    db_service: SupabaseDatabaseService = Depends(SupabaseClient.get_database_service)
):
    try:
        return db_service.insert_data(
            table,
            data=insert_data.data,
            upsert=insert_data.upsert
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/data/{table}")
async def update_data(
    table: str,
    update_data: UpdateData,
    db_service: SupabaseDatabaseService = Depends(SupabaseClient.get_database_service)
):
    try:
        return db_service.update_data(
            table,
            data=update_data.data,
            filters=update_data.filters
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/data/{table}")
async def delete_data(
    table: str,
    delete_filter: DeleteFilter,
    db_service: SupabaseDatabaseService = Depends(SupabaseClient.get_database_service)
):
    try:
        return db_service.delete_data(
            table,
            filters=delete_filter.filters
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/function/{function_name}")
async def call_function(
    function_name: str,
    function_call: FunctionCall,
    db_service: SupabaseDatabaseService = Depends(SupabaseClient.get_database_service)
):
    try:
        return db_service.call_function(
            function_name,
            params=function_call.params
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/table/{table}")
async def create_test_table(
    table: str,
    db_service: SupabaseDatabaseService = Depends(SupabaseClient.get_database_service)
):
    try:
        return db_service.create_test_table(table)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/table/{table}")
async def delete_table(
    table: str,
    db_service: SupabaseDatabaseService = Depends(SupabaseClient.get_database_service)
):
    try:
        return db_service.delete_table(table)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
