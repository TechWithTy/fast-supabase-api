from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class OpportunityStatusUpdate(BaseModel):
    """
    Represents an opportunity status update webhook.
    Called whenever an opportunity's status field is updated.
    """
    type: str = Field(..., description="Type of the webhook event")
    location_id: str = Field(..., alias="locationId")
    id: str
    assigned_to: Optional[str] = Field(None, alias="assignedTo")
    contact_id: Optional[str] = Field(None, alias="contactId")
    monetary_value: Optional[float] = Field(None, alias="monetaryValue")
    name: str
    pipeline_id: str = Field(..., alias="pipelineId")
    pipeline_stage_id: str = Field(..., alias="pipelineStageId")
    source: Optional[str] = None
    status: str
    date_added: datetime = Field(..., alias="dateAdded")

    class Config:
        allow_population_by_field_name = True

# Example usage:
example_data = {
    "type": "OpportunityStatusUpdate",
    "locationId": "ve9EPM428h8vShlRW1KT",
    "id": "wWhVuzqpRuOA1ZVWi4FC",
    "assignedTo": "bNl8QNGXhIQJLv8eeASQ",
    "contactId": "cJAWDskpkJHbRbhAT7bs",
    "monetaryValue": 40,
    "name": "Loram ipsu",
    "pipelineId": "VDm7RPYC2GLUvdpKmBfC",
    "pipelineStageId": "e93ba61a-53b3-45e7-985a-c7732dbcdb69",
    "source": "Loram ipsu",
    "status": "open",
    "dateAdded": "2021-11-26T12:41:02.193Z"
}

opportunity_update = OpportunityStatusUpdate(**example_data)