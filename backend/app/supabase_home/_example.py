import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .client import supabase

app = FastAPI()

logger = logging.getLogger("apps.supabase_home")


@app.get("/api/supabase/example/")
async def example_supabase_view():
    """
    Example endpoint demonstrating how to use the Supabase client in FastAPI.

    This endpoint shows how to:
    1. Use the Supabase database service to fetch data
    2. Handle errors properly
    3. Return JSON responses

    Returns:
        JSONResponse: JSON response with data or error message
    """
    try:
        db_service = supabase.get_database_service()
        table_name = "example_table"  # Replace with your actual table name

        try:
            data = db_service.fetch_data(table=table_name, limit=10)
            return JSONResponse(
                {
                    "success": True,
                    "data": data,
                    "message": f"Successfully fetched data from {table_name}",
                }
            )
        except Exception as e:
            logger.warning(f"Error fetching data: {str(e)}")
            return JSONResponse(
                {
                    "success": True,
                    "data": None,
                    "message": "Supabase client is configured correctly, but could not fetch data. "
                    "This is expected if the example table does not exist.",
                }
            )

    except Exception as e:
        logger.exception(f"Unexpected error in example_supabase_view: {str(e)}")
        raise HTTPException(
            status_code=500, detail="An error occurred while connecting to Supabase."
        )


@app.get("/api/supabase/health/")
async def supabase_health_check():
    """
    Health check endpoint for Supabase connection.

    This endpoint attempts to initialize the Supabase client and reports
    whether the connection is working properly.

    Returns:
        JSONResponse: JSON response with connection status
    """
    try:
        raw_client = supabase.get_raw_client()
        return JSONResponse(
            {
                "status": "ok",
                "message": "Supabase client is configured correctly",
                "supabase_url": raw_client.supabase_url,
            }
        )
    except Exception as e:
        logger.exception(f"Supabase health check failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Supabase client configuration error"
        )
