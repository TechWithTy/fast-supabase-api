from typing import Optional
from pydantic import BaseModel, Field

class LocationCreate(BaseModel):
    """
    Represents a location creation event.
    
    Available only to Agency Level Apps.
    Called whenever a location is created.
    """
    type: str = Field(..., description="Event type")
    id: str = Field(..., description="Location ID")
    companyId: str = Field(..., description="Company ID")
    name: str = Field(..., description="Location name")
    email: str = Field(..., description="Location email")
    stripeProductId: Optional[str] = Field(None, description="Stripe Product ID")

# Example usage
example_data = {
    "type": "LocationCreate",
    "id": "ve9EPM428h8vShlRW1KT",
    "companyId": "otg8dTQqGLh3Q6iQI55w",
    "name": "Loram ipsum",
    "email": "mailer@example.com",
    "stripeProductId": "prod_xyz123abc"
}

location_create = LocationCreate(**example_data)