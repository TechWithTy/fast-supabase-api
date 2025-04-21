from pydantic import BaseModel, Field
from typing import Optional

class PlanChangeWebhook(BaseModel):
    """
    Called whenever user changes the plan for a paid app.
    """
    type: str = Field(..., description="Type of the webhook event")
    app_id: str = Field(..., alias="appId")
    location_id: str = Field(..., alias="locationId")
    company_id: str = Field(..., alias="companyId")
    user_id: str = Field(..., alias="userId")
    current_plan_id: str = Field(..., alias="currentPlanId")
    new_plan_id: str = Field(..., alias="newPlanId")

    class Config:
        allow_population_by_field_name = True

# Example usage
example_data = {
    "type": "PLAN_CHANGE",
    "appId": "ve9EPM428h8vShlRW1KT",
    "locationId": "otg8dTQqGLh3Q6iQI55w",
    "companyId": "otg8dTQqGLh3Q6iQI55w",
    "userId": "otg8dTQqGLh3Q6iQI55w",
    "currentPlanId": "66a0419a0dffa47fb5f8b22f",
    "newPlanId": "66a0419a0dffa47fb5f8b22f"
}

plan_change_webhook = PlanChangeWebhook(**example_data)