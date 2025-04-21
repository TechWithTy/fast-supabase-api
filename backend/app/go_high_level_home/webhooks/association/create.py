from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AssociationCreate(BaseModel):
    """
    Represents a webhook response triggered when a new association is created between objects.
    
    Currently supports:
    - Contact-to-contact associations
    - Contact to custom object associations
    - Custom object to custom object associations
    
    Example:
    In a real estate system, associating potential buyers with specific properties:
    - First object (buyer): Custom object representing the interested person
    - Second object (property): Custom object representing the real estate listing
    - Association label: "Interested Buyer"
    - Relationship: Many-to-many (multiple buyers per property)
    """

    id: str = Field(..., description="Unique identifier for the association")
    associationType: str = Field(..., description="Type of association (e.g., USER_DEFINED or SYSTEM_DEFINED)")
    firstObjectKey: str = Field(..., description="Key representing the first object in the association")
    firstObjectLabel: str = Field(..., description="Readable label for the first object")
    secondObjectKey: str = Field(..., description="Key representing the second object in the association")
    secondObjectLabel: str = Field(..., description="Readable label for the second object")
    key: str = Field(..., description="Unique key assigned to the association")
    locationId: str = Field(..., description="Identifies the location associated with the created association")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the association creation")

    class Config:
        allow_population_by_field_name = True

# Example usage
example_data = {
    "id": "67ade73d1119d2ac7ad0c475",
    "associationType": "USER_DEFINED",
    "firstObjectKey": "custom_objects.real_estate_buyer",
    "firstObjectLabel": "Interested Buyer",
    "secondObjectKey": "custom_objects.property",
    "secondObjectLabel": "Property",
    "key": "buyer_property_interest",
    "locationId": "eHy2cOSZxMQzQ6Yyvl8P",
    "timestamp": "2023-05-17T12:34:56.789Z"
}

association_create = AssociationCreate(**example_data)
print(association_create)

# Additional Notes:
# 1. Ensure your webhook listener is set up to handle POST requests.
# 2. The firstObjectKey and secondObjectKey define relationships between entities.
# 3. Use the id field for debugging and logging purposes.
