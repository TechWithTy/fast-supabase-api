import logging
from typing import Any

from backend.app.go_high_level_home.api.business.create import create_contact
from fastapi import HTTPException
from pydantic import BaseModel


class ContactUploadRequest(BaseModel):
    headers: dict[str, str]
    contact_data: dict[str, Any]

async def upload_contact_logic(req: ContactUploadRequest):
    try:
        result = await create_contact(req.headers, **req.contact_data)
        return result
    except Exception as e:
        logging.error(f"Error uploading contact: {e}")
        raise HTTPException(status_code=400, detail=str(e))
