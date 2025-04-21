from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class OpportunityUpdate(BaseModel):
    type: str = Field(..., description="Type of the webhook event")
    locationId: str = Field(..., description="Unique identifier for the location")
    id: str = Field(..., description="Unique identifier for the opportunity")
    assignedTo: Optional[str] = Field(None, description="User ID the opportunity is assigned to")
    contactId: Optional[str] = Field(None, description="Associated contact ID")
    monetaryValue: Optional[float] = Field(None, description="Monetary value of the opportunity")
    name: Optional[str] = Field(None, description="Name of the opportunity")
    pipelineId: Optional[str] = Field(None, description="ID of the pipeline")
    pipelineStageId: Optional[str] = Field(None, description="ID of the pipeline stage")
    source: Optional[str] = Field(None, description="Source of the opportunity")
    status: Optional[str] = Field(None, description="Status of the opportunity")
    dateAdded: Optional[datetime] = Field(None, description="Date when the opportunity was added")

    class Config:
        allow_population_by_field_name = True

# Example usage
example_data = {
    "type": "OpportunityUpdate",
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

opportunity_update = OpportunityUpdate(**example_data)