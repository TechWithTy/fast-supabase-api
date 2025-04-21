from pydantic import BaseModel, Field
from typing import Optional

class RelationCreate(BaseModel):
    """
    Represents a webhook response triggered when a relation between objects is created.

    For example, in a business management system, a company may want to establish an
    association between a custom object record and a contact. In this case:
    - The second object (contact) would represent a person associated with the custom object record.
    - The first object (custom object) could represent an entity such as a project or a transaction.
    - The system allows for dynamic relationships between entities, facilitating better data management.
    """

    id: str = Field(..., description="Unique identifier for the created association.")
    firstObjectKey: str = Field(..., description="Key representing the first object in the association.")
    firstRecordId: str = Field(..., description="Identifier of the first object's specific record.")
    secondObjectKey: str = Field(..., description="Key representing the second object in the association.")
    secondRecordId: str = Field(..., description="Identifier of the second object's specific record.")
    associationId: str = Field(..., description="Unique identifier for the association that was created.")
    locationId: str = Field(..., description="Identifies the location associated with the created association.")

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

relation_create = RelationCreate(**example_data)

# Additional Notes:
# - The firstObjectKey and secondObjectKey define the relationship between the created entities.
# - Ensure your webhook listener is set up to handle POST requests for this event.
