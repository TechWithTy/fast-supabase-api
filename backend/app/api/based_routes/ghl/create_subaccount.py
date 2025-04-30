import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.go_high_level_home.api.sub_accounts.sub_account.put import (
    update_sub_account,
)


class SubAccountCreateRequest(BaseModel):
    location_id: str
    headers: dict[str, str]
    sub_account_data: dict[str, Any]


router = APIRouter(tags=["GHL Subaccount"])


async def create_subaccount_logic(req: SubAccountCreateRequest):
    try:
        result = await update_sub_account(
            req.location_id, req.headers, req.sub_account_data
        )
        return result
    except Exception as e:
        logging.error(f"Error creating subaccount: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create-subaccount")
async def create_subaccount_endpoint(req: SubAccountCreateRequest):
    return await create_subaccount_logic(req)
