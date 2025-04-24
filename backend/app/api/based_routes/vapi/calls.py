from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.based_routes.vapi._schemas import CreateCallRequest, UpdateCallRequest
from app.api.utils.credits import call_function_with_credits
from app.vapi_home.api.calls.create import create_call
from app.vapi_home.api.calls.delete import delete_call
from app.vapi_home.api.calls.get import get_call
from app.vapi_home.api.calls.list import list_calls
from app.vapi_home.api.calls.update import update_call

router = APIRouter(prefix="/vapi/calls", tags=["VAPI Calls"])


@router.post("")
async def api_create_call(
    req: CreateCallRequest,
    request: Request,
    current_user=Depends(None),
    db=Depends(None),
):
    async def endpoint_logic(request, current_user):
        resp = create_call(req.payload)
        if resp is None:
            raise HTTPException(status_code=500, detail="Failed to create call.")
        return resp

    return await call_function_with_credits(
        endpoint_logic,
        request,
        credit_type="ai",
        db=db,
        current_user=current_user,
        credit_amount=5,
    )


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
async def api_update_call(
    call_id: str,
    req: UpdateCallRequest,
    request: Request,
    current_user=Depends(None),
    db=Depends(None),
):
    async def endpoint_logic(request, current_user):
        resp = update_call(call_id, req.update_data)
        if resp is None:
            raise HTTPException(status_code=500, detail="Failed to update call.")
        return resp

    return await call_function_with_credits(
        endpoint_logic,
        request,
        credit_type="ai",
        db=db,
        current_user=current_user,
        credit_amount=0,
    )


@router.delete("/{call_id}")
async def api_delete_call(
    call_id: str, request: Request, current_user=Depends(None), db=Depends(None)
):
    async def endpoint_logic(request, current_user):
        resp = delete_call(call_id)
        if resp is None:
            raise HTTPException(status_code=500, detail="Failed to delete call.")
        return resp

    return await call_function_with_credits(
        endpoint_logic,
        request,
        credit_type="ai",
        db=db,
        current_user=current_user,
        credit_amount=0,
    )
