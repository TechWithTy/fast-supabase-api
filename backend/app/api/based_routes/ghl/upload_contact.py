import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.go_high_level_home.api.contacts.bulk.add_remove import (
    bulk_update_contacts_business,
)


class ContactUploadRequest(BaseModel):
    headers: dict[str, str]
    contact_data: dict[str, Any]


router = APIRouter(tags=["GHL Contact"])


async def upload_contact_logic(req: ContactUploadRequest):
    try:
        result = await bulk_update_contacts_business(req.headers, **req.contact_data)
        return result
    except Exception as e:
        logging.error(f"Error uploading contact: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload-contact")
async def upload_contact_endpoint(req: ContactUploadRequest):
    return await upload_contact_logic(req)
