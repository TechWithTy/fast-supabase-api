
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Labels(BaseModel):
    singular: str
    plural: str

class UserMetadata(BaseModel):
    pass  # Placeholder for future fields

class ObjectSchemaUpdate(BaseModel):
    id: str
    labels: Labels
    description: str
    searchableProperties: List[str]
    primaryDisplayProperty: str
    key: str
    locationId: str
    createdBy: Optional[UserMetadata]
    updatedBy: Optional[UserMetadata]
    timestamp: datetime
    objectType: str = Field(default="USER_DEFINED")
    updatedAt: datetime
    createdAt: datetime

    class Config:
        allow_population_by_field_name = True

# Example usage
# Example usage
example_payload = {
    "id": "6798a1a18fc746e0eba2ccfe",
    "labels": {
        "singular": "pet",
        "plural": "pets"
    },
    "description": "Pet's Description",
    "searchableProperties": [
        "custom_objects.pets.pet_name"
    ],
    "primaryDisplayProperty": "custom_objects.pets.pet_name",
    "key": "custom_objects.pets",
    "locationId": "eHy2cOSZxMQzQ6Yyvl8P",
    "updatedAt": "2025-01-28T09:21:37.311Z",
    "createdAt": "2025-01-28T09:21:37.311Z",
    "objectType": "USER_DEFINED",
    "timestamp": "2025-02-10T08:26:05.961Z"
}

schema_create = ObjectSchemaUpdate(**example_payload)

# Additional Notes:
# 1. Ensure your webhook listener is set up to handle POST requests.
# 2. The payload format may change in future versions; check for updates regularly.
# 3. The key field should be unique within a given locationId.
