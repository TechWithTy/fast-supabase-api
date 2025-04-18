import logging
from typing import Any

from backend.app.go_high_level_home.api.business.create import create_appointment
from fastapi import HTTPException
from pydantic import BaseModel


class AppointmentScheduleRequest(BaseModel):
    contact_id: str
    appointment_data: dict[str, Any]
    headers: dict[str, str]


async def schedule_appointment_logic(req: AppointmentScheduleRequest):
    try:
        result = await create_appointment(
            req.contact_id, req.appointment_data, req.headers
        )
        return result
    except Exception as e:
        logging.error(f"Error scheduling appointment: {e}")
        raise HTTPException(status_code=400, detail=str(e))
