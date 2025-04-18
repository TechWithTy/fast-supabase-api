import logging
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/vapi/calls", tags=["VAPI Webhooks"])

class CallEndWebhookPayload(BaseModel):
    call_id: str
    summary: Any = None
    outcome: str = None
    data: dict[str, Any] = None

@router.post("/end-webhook")
async def call_end_webhook(payload: CallEndWebhookPayload):
    """
    Handle call result webhook from VAPI (call ended, summary, outcome, etc).
    """
    logging.info(f"Received call end webhook: {payload}")
    # TODO: Implement business logic (update call record, notify user, etc)
    # Example: update_call_status(payload.call_id, 'ended', payload.outcome, payload.summary)
    return {"status": "received", "call_id": payload.call_id}

class CallStatusWebhookPayload(BaseModel):
    call_id: str
    status: str
    data: dict[str, Any] = None

@router.post("/status-webhook")
async def call_status_webhook(payload: CallStatusWebhookPayload):
    """
    Handle live call status updates from VAPI (ringing, voicemail, error, etc).
    """
    logging.info(f"Received call status webhook: {payload}")
    # TODO: Implement business logic (update call status, notify user, retry, etc)
    # Example: update_call_status(payload.call_id, payload.status, payload.data)
    return {"status": "received", "call_id": payload.call_id, "current_status": payload.status}
