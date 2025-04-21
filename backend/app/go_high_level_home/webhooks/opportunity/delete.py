from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class OpportunityDelete(BaseModel):
    """
    Represents an opportunity deletion event in Go High Level.
    Called whenever an opportunity is deleted.
    """
    type: str = Field(..., description="Event type")
    locationId: str = Field(..., description="Location ID")
    id: str = Field(..., description="Opportunity ID")
    assignedTo: str = Field(..., description="Assigned user ID")
    contactId: str = Field(..., description="Associated contact ID")
    monetaryValue: float = Field(..., description="Monetary value of the opportunity")
    name: str = Field(..., description="Name of the opportunity")
    pipelineId: str = Field(..., description="Pipeline ID")
    pipelineStageId: str = Field(..., description="Pipeline stage ID")
    source: Optional[str] = Field(None, description="Source of the opportunity")
    status: str = Field(..., description="Status of the opportunity")
    dateAdded: datetime = Field(..., description="Date the opportunity was added")

# Example usage:
example_data = {
    "type": "OpportunityDelete",
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

opportunity_delete = OpportunityDelete(**example_data)