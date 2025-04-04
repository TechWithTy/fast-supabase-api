from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from ...supabase_home.client import SupabaseClient
from ...supabase_home.functions.storage import SupabaseStorageService

app = FastAPI(title="SupabaseStorageAPI", description="API to interact with current storage functions")

class BucketCreate(BaseModel):
    bucket_id: str
    public: bool = False
    file_size_limit: int | None = None
    allowed_mime_types: list[str] | None = None

class BucketUpdate(BaseModel):
    public: bool | None = None
    file_size_limit: int | None = None
    allowed_mime_types: list[str] | None = None

@app.post("/buckets")
async def create_bucket(bucket: BucketCreate, storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)):
    try:
        result = storage_service.create_bucket(
            bucket_id=bucket.bucket_id,
            public=bucket.public,
            file_size_limit=bucket.file_size_limit,
            allowed_mime_types=bucket.allowed_mime_types
        )
        return JSONResponse(content=result, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/buckets/{bucket_id}")
async def get_bucket(bucket_id: str, storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)):
    try:
        result = storage_service.get_bucket(bucket_id)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/buckets")
async def list_buckets(storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)):
    try:
        result = storage_service.list_buckets()
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/buckets/{bucket_id}")
async def update_bucket(bucket_id: str, bucket: BucketUpdate, storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)):
    try:
        result = storage_service.update_bucket(
            bucket_id=bucket_id,
            public=bucket.public,
            file_size_limit=bucket.file_size_limit,
            allowed_mime_types=bucket.allowed_mime_types
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/buckets/{bucket_id}")
async def delete_bucket(bucket_id: str, storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)):
    try:
        result = storage_service.delete_bucket(bucket_id)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/buckets/{bucket_id}/empty")
async def empty_bucket(bucket_id: str, storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)):
    try:
        result = storage_service.empty_bucket(bucket_id)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/buckets/{bucket_id}/upload")
async def upload_file(
    bucket_id: str,
    path: str = Query(...),
    file: UploadFile = File(...),
    storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)
):
    try:
        file_content = await file.read()
        result = storage_service.upload_file(
            bucket_id=bucket_id,
            path=path,
            file_data=file_content,
            content_type=file.content_type
        )
        return JSONResponse(content=result, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/buckets/{bucket_id}/download")
async def download_file(
    bucket_id: str,
    path: str = Query(...),
    storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)
):
    try:
        file_content, content_type = storage_service.download_file(
            bucket_id=bucket_id,
            path=path
        )
        return StreamingResponse(iter([file_content]), media_type=content_type)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/buckets/{bucket_id}/files")
async def list_files(
    bucket_id: str,
    path: str = Query(""),
    limit: int = Query(100),
    offset: int = Query(0),
    storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)
):
    try:
        result = storage_service.list_files(
            bucket_id=bucket_id,
            path=path,
            limit=limit,
            offset=offset
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/buckets/{bucket_id}/move")
async def move_file(
    bucket_id: str,
    source_path: str = Query(...),
    destination_path: str = Query(...),
    storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)
):
    try:
        result = storage_service.move_file(
            bucket_id=bucket_id,
            source_path=source_path,
            destination_path=destination_path
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/buckets/{bucket_id}/copy")
async def copy_file(
    bucket_id: str,
    source_path: str = Query(...),
    destination_path: str = Query(...),
    storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)
):
    try:
        result = storage_service.copy_file(
            bucket_id=bucket_id,
            source_path=source_path,
            destination_path=destination_path
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/buckets/{bucket_id}/files")
async def delete_files(
    bucket_id: str,
    paths: list[str] = Query(...),
    storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)
):
    try:
        result = storage_service.delete_file(
            bucket_id=bucket_id,
            paths=paths
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/buckets/{bucket_id}/sign")
async def create_signed_url(
    bucket_id: str,
    path: str = Query(...),
    expires_in: int = Query(60),
    storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)
):
    try:
        result = storage_service.create_signed_url(
            bucket_id=bucket_id,
            path=path,
            expires_in=expires_in
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/buckets/{bucket_id}/sign-bulk")
async def create_signed_urls(
    bucket_id: str,
    paths: list[str] = Query(...),
    expires_in: int = Query(60),
    storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)
):
    try:
        result = storage_service.create_signed_urls(
            bucket_id=bucket_id,
            paths=paths,
            expires_in=expires_in
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/buckets/{bucket_id}/upload/sign")
async def create_signed_upload_url(
    bucket_id: str,
    path: str = Query(...),
    storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)
):
    try:
        result = storage_service.create_signed_upload_url(
            bucket_id=bucket_id,
            path=path
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/buckets/{bucket_id}/public")
async def get_public_url(
    bucket_id: str,
    path: str = Query(...),
    storage_service: SupabaseStorageService = Depends(SupabaseClient.get_storage_service)
):
    try:
        result = storage_service.get_public_url(
            bucket_id=bucket_id,
            path=path
        )
        return JSONResponse(content={"public_url": result})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
