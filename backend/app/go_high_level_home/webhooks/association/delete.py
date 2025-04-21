from pydantic import BaseModel, Field
from typing import Optional

class AssociationDeleted(BaseModel):
    """
    Represents a webhook response triggered when an association is deleted between objects.
    
    Currently supports:
    - Contact-to-contact associations
    - Contact to custom object associations
    - Custom object to custom object associations
    
    Example:
    In a real estate system, an association between a buyer (custom object) and a property (custom object) 
    might be deleted when the buyer is no longer interested in the property.
    """

    id: str = Field(..., description="Unique identifier for the deleted association")
    associationType: str = Field(..., description="Type of association (e.g., USER_DEFINED or SYSTEM_DEFINED)")
    firstObjectKey: str = Field(..., description="Key representing the first object in the association")
    firstObjectLabel: str = Field(..., description="Human-readable label for the first object")
    firstObjectToSecondObjectCardinality: str = Field(..., description="Relationship between first and second object (e.g., MANY_TO_MANY)")
    secondObjectKey: str = Field(..., description="Key representing the second object in the association")
    secondObjectLabel: str = Field(..., description="Human-readable label for the second object")
    secondObjectToFirstObjectCardinality: str = Field(..., description="Reverse relationship between objects")
    key: str = Field(..., description="Unique key assigned to the association")
    locationId: str = Field(..., description="Identifies the location associated with the deleted association")

    class Config:
        schema_extra = {
            "example": {
                "id": "67ade73d1119d2ac7ad0c475",
                "associationType": "USER_DEFINED",
                "firstObjectKey": "custom_objects.real_estate_buyer",
                "firstObjectLabel": "Interested Buyer",
                "firstObjectToSecondObjectCardinality": "MANY_TO_MANY",
                "secondObjectKey": "custom_objects.property",
                "secondObjectLabel": "Property",
                "secondObjectToFirstObjectCardinality": "MANY_TO_MANY",
                "key": "buyer_property_interest",
                "locationId": "eHy2cOSZxMQzQ6Yyvl8P"
            }
        }

# Additional Notes:
# 1. Ensure your webhook listener is set up to handle POST requests for this event.
# 2. The firstObjectKey and secondObjectKey define the relationship between the deleted entities.
# 3. Use the traceId (if available) for debugging and logging purposes.
