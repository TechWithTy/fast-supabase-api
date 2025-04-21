from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AssociationUpdate(BaseModel):
    id: str = Field(..., description="Unique identifier for the association")
    associationType: str = Field(..., description="Type of association (e.g., USER_DEFINED or SYSTEM_DEFINED)")
    firstObjectKey: str = Field(..., description="Key representing the first object in the association")
    firstObjectLabel: str = Field(..., description="Human-readable label for the first object")
    firstObjectToSecondObjectCardinality: str = Field(..., description="Relationship between the first and second object (e.g., MANY_TO_MANY)")
    secondObjectKey: str = Field(..., description="Key representing the second object in the association")
    secondObjectLabel: str = Field(..., description="Human-readable label for the second object")
    secondObjectToFirstObjectCardinality: str = Field(..., description="Reverse relationship between objects")
    key: str = Field(..., description="Unique key assigned to the association")
    locationId: str = Field(..., description="Location associated with the created association")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the update")

    class Config:
        allow_population_by_field_name = True

# Example usage
example_data = {
    "id": "67ade73d1119d2ac7ad0c475",
    "associationType": "USER_DEFINED",
    "firstObjectKey": "custom_objects.real_estate_buyer",
    "firstObjectLabel": "Interested Buyer",
    "firstObjectToSecondObjectCardinality": "MANY_TO_MANY",
    "secondObjectKey": "custom_objects.property",
    "secondObjectLabel": "Property",
    "secondObjectToFirstObjectCardinality": "MANY_TO_MANY",
    "key": "buyer_property_interest",
    "locationId": "eHy2cOSZxMQzQ6Yyvl8P",
    "timestamp": "2023-05-17T12:34:56.789Z"
}

association_update = AssociationUpdate(**example_data)
print(association_update)

# Additional Notes:
# 1. Ensure your webhook listener is set up to handle POST requests.
# 2. The firstObjectKey and secondObjectKey define relationships between entities.
# 3. Use the id field for debugging and logging purposes.
