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
    poll_interval: float = 2.0,
    timeout: float = 180.0,
):
    """
    Create a call, wait until it finishes, then return call data and credits used.
    Credits are calculated based on call duration (1 credit per 60 seconds, rounded up).
    """
    import asyncio
    import math
    from time import time
    # Phase 1: Create call
    call_resp = create_call(req.payload)
    if not call_resp or 'id' not in call_resp:
        raise HTTPException(status_code=500, detail="Failed to create call.")
    call_id = call_resp['id']

    # Phase 2: Poll for call completion
    start_time = time()
    call_data = None
    while time() - start_time < timeout:
        call_data = get_call(call_id)
        if not call_data:
            await asyncio.sleep(poll_interval)
            continue
        status = call_data.get("status")
        if status in ("completed", "ended", "finished"):  # support all possible finished statuses
            break
        await asyncio.sleep(poll_interval)
    else:
        raise HTTPException(status_code=504, detail="Call did not finish in allotted time.")

    # Phase 3: Calculate credits by duration
    duration = call_data.get("duration") or call_data.get("duration_seconds") or 0
    try:
        duration = int(duration)
    except Exception:
        duration = 0
    credits_used = max(1, math.ceil(duration / 60))
    call_data["credits_used"] = credits_used

    # Phase 4: Charge actual credits
    async def endpoint_logic(_request, _current_user):
        return call_data

    return await call_function_with_credits(
        endpoint_logic,
        request,
        credit_type="ai",
        db=db,
        current_user=current_user,
        credit_amount=credits_used,
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
    resp = update_call(call_id, req.update_data)
    if resp is None:
        raise HTTPException(status_code=500, detail="Failed to update call.")
    return resp


@router.delete("/{call_id}")
async def api_delete_call(
    call_id: str, request: Request, current_user=Depends(None), db=Depends(None)
):
    resp = delete_call(call_id)
    if resp is None:
        raise HTTPException(status_code=500, detail="Failed to delete call.")
    return resp
