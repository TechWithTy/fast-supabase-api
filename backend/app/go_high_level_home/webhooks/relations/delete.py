from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RelationDelete(BaseModel):
    """
    Represents a relation deletion event in Go High Level.
    Called whenever a relation between objects is deleted.
    """
    id: str = Field(..., description="Unique identifier for the deleted association")
    firstObjectKey: str = Field(..., description="Key representing the first object in the association")
    firstRecordId: str = Field(..., description="Identifier of the first object's specific record")
    secondObjectKey: str = Field(..., description="Key representing the second object in the association")
    secondRecordId: str = Field(..., description="Identifier of the second object's specific record")
    associationId: str = Field(..., description="Unique identifier for the association that was deleted")
    locationId: str = Field(..., description="Identifies the location associated with the deleted association")

# Example usage
example_data = {
    "id": "67ae0d741119d218c9d0c477",
    "firstObjectKey": "custom_objects.mad",
    "firstRecordId": "67a349a79b28947ec1f65bb5",
    "secondObjectKey": "contact",
    "secondRecordId": "emqfhnG3g9D9chy9inTz",
    "associationId": "669e5795add2094075906c65",
    "locationId": "eHy2cOSZxMQzQ6Yyvl8P"
}

relation_delete = RelationDelete(**example_data)

# Additional Notes:
# 1. Ensure your webhook listener is set up to handle POST requests.
# 2. The payload format may change in future versions; check for updates regularly.
# 3. The firstObjectKey and secondObjectKey define the relationship between the deleted entities.
