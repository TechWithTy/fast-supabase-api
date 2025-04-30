import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.go_high_level_home.api.sub_accounts.tags.create import create_tag


class TagApplyRequest(BaseModel):
    location_id: str
    tag_name: str
    headers: dict[str, str]


async def apply_tag_logic(req: TagApplyRequest):
    try:
        result = await create_tag(req.location_id, req.tag_name, req.headers)
        return result
    except Exception as e:
        logging.error(f"Error applying tag: {e}")
        raise HTTPException(status_code=400, detail=str(e))


router = APIRouter(tags=["GHL Tag"])


@router.post("/apply-tag")
async def apply_tag_endpoint(req: TagApplyRequest):
    return await apply_tag_logic(req)
