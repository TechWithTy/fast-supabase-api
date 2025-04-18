import logging
from fastapi import HTTPException, Request
from typing import Any

# Example: import your workflow trigger logic here
# from ...vapi.call_queue import queue_vapi_call
# from ...leads.update import update_lead_status

TRIGGER_TAG = "to-call"  # Change as needed

def is_trigger_tag_present(tags: list[str]) -> bool:
    return any(tag.strip().lower() == TRIGGER_TAG for tag in tags)

async def contact_tagged_webhook_logic(request: Request):
    try:
        payload = await request.json()
        logging.info(f"Received ContactTagUpdate webhook payload: {payload}")

        # Extract required fields from the ContactTagUpdate schema
        event_type = payload.get("type")
        location_id = payload.get("locationId")
        contact_id = payload.get("id")
        tags = payload.get("tags", [])

        # Validate payload
        if event_type != "ContactTagUpdate" or not location_id or not contact_id or not isinstance(tags, list):
            logging.error(f"Invalid ContactTagUpdate webhook payload: {payload}")
            raise HTTPException(status_code=422, detail="Invalid ContactTagUpdate webhook payload.")

        # Check for the trigger tag
        triggered = is_trigger_tag_present(tags)
        if triggered:
            logging.info(f"Trigger tag '{TRIGGER_TAG}' present for contact {contact_id} at location {location_id}.")
            # TODO: Call your workflow/queue logic here, e.g.:
            # await queue_vapi_call(contact_id=contact_id, location_id=location_id)
            action_result = {
                "triggered": True,
                "action": f"Workflow triggered for contact {contact_id} (tag '{TRIGGER_TAG}' found)"
            }
        else:
            logging.info(f"Tag '{TRIGGER_TAG}' NOT present for contact {contact_id} at location {location_id}. No action taken.")
            action_result = {
                "triggered": False,
                "action": f"No workflow triggered for contact {contact_id} (tag '{TRIGGER_TAG}' not found)"
            }

        return {
            "status": "processed",
            "event_type": event_type,
            "contact_id": contact_id,
            "location_id": location_id,
            "tags": tags,
            **action_result
        }
    except Exception as e:
        logging.error(f"Error in webhook: {e}")
        raise HTTPException(status_code=400, detail=str(e))
