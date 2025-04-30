from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from app.vapi_home.api.assistants.create import create_assistant
from app.vapi_home.api.assistants.delete import delete_assistant
from app.vapi_home.api.assistants.get import get_assistant
from app.vapi_home.api.assistants.list import list_assistants
from app.vapi_home.api.assistants.update import update_assistant

router = APIRouter(prefix="/vapi/assistants", tags=["VAPI Assistants"])


class AssistantCreateRequest(BaseModel):
    payload: dict[str, Any]


@router.post("")
async def api_create_assistant(req: AssistantCreateRequest, request: Request, current_user=Depends(None), db=Depends(None)):
    resp = create_assistant(req.payload)
    if resp is None:
        raise HTTPException(status_code=500, detail="Failed to create assistant.")
    return resp


@router.get("")
def api_list_assistants():
    resp = list_assistants()
    if resp is None:
        raise HTTPException(status_code=500, detail="Failed to list assistants.")
    return resp


@router.get("/{assistant_id}")
def api_get_assistant(assistant_id: str):
    resp = get_assistant(assistant_id)
    if resp is None:
        raise HTTPException(status_code=404, detail="Assistant not found.")
    return resp


class AssistantUpdateRequest(BaseModel):
    update_data: dict[str, Any]


@router.patch("/{assistant_id}")
async def api_update_assistant(assistant_id: str, req: AssistantUpdateRequest, request: Request, current_user=Depends(None), db=Depends(None)):
    resp = update_assistant(assistant_id, req.update_data)
    if resp is None:
        raise HTTPException(status_code=500, detail="Failed to update assistant.")
    return resp


@router.delete("/{assistant_id}")
async def api_delete_assistant(assistant_id: str, request: Request, current_user=Depends(None), db=Depends(None)):
    resp = delete_assistant(assistant_id)
    if resp is None:
        raise HTTPException(status_code=500, detail="Failed to delete assistant.")
    return resp
