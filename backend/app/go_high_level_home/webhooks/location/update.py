from typing import Optional
from pydantic import BaseModel, Field

class LocationUpdate(BaseModel):
    type: str = Field(..., description="Type of the webhook event")
    id: str = Field(..., description="Unique identifier for the location")
    company_id: str = Field(..., alias="companyId", description="Unique identifier for the company")
    name: str = Field(..., description="Name of the location")
    email: str = Field(..., description="Email associated with the location")
    stripe_product_id: Optional[str] = Field(None, alias="stripeProductId", description="Stripe product ID if applicable")

    class Config:
        allow_population_by_field_name = True

# Example usage
example_data = {
    "type": "LocationUpdate",
    "id": "ve9EPM428h8vShlRW1KT",
    "companyId": "otg8dTQqGLh3Q6iQI55w",
    "name": "Loram ipsum",
    "email": "mailer@example.com",
    "stripeProductId": "prod_xyz123abc"
}

location_update = LocationUpdate(**example_data)