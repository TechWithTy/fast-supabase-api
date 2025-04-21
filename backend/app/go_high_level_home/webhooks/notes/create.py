from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NoteCreate(BaseModel):
    type: str = Field(..., description="Type of the webhook event")
    location_id: str = Field(..., alias="locationId", description="Unique identifier for the location")
    id: str = Field(..., description="Unique identifier for the note")
    body: str = Field(..., description="Content of the note")
    contact_id: str = Field(..., alias="contactId", description="Unique identifier for the associated contact")
    date_added: datetime = Field(..., alias="dateAdded", description="Date and time when the note was added")

    class Config:
        allow_population_by_field_name = True

# Example usage
example_data = {
    "type": "NoteCreate",
    "locationId": "ve9EPM428h8vShlRW1KT",
    "id": "otg8dTQqGLh3Q6iQI55w",
    "body": "Loram ipsum",
    "contactId": "CWBf1PR9LvvBkcYqiXlc",
    "dateAdded": "2021-11-26T12:41:02.193Z"
}

note_create = NoteCreate(**example_data)
print(note_create)