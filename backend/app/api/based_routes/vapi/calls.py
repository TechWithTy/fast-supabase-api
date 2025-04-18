from backend.app.vapi_home.api.calls.create import create_call
from backend.app.vapi_home.api.calls.delete import delete_call
from backend.app.vapi_home.api.calls.get import get_call
from backend.app.vapi_home.api.calls.list import list_calls
from backend.app.vapi_home.api.calls.update import update_call
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/vapi/calls", tags=["VAPI Calls"])


@router.post("")
def api_create_call():
    resp = create_call()
    if resp is None:
        raise HTTPException(status_code=500, detail="Failed to create call.")
    return resp


@router.get("")
def api_list_calls():
    resp = list_calls()
    if resp is None:
        raise HTTPException(status_code=500, detail="Failed to list calls.")
    return resp


@router.get("/{call_id}")
def api_get_call(call_id: str):
    resp = get_call(call_id)
    if resp is None:
        raise HTTPException(status_code=404, detail="Call not found.")
    return resp


@router.patch("/{call_id}")
def api_update_call(call_id: str):
    resp = update_call(call_id)
    if resp is None:
        raise HTTPException(status_code=500, detail="Failed to update call.")
    return resp


@router.delete("/{call_id}")
def api_delete_call(call_id: str):
    resp = delete_call(call_id)
    if resp is None:
        raise HTTPException(status_code=500, detail="Failed to delete call.")
    return resp
