from pydantic import BaseModel, Field
from typing import List, Optional

class UserPermissions(BaseModel):
    adwordsReportingEnabled: bool = Field(default=False)
    affiliateManagerEnabled: bool = Field(default=False)
    agentReportingEnabled: bool = Field(default=False)
    appointmentsEnabled: bool = Field(default=False)
    assignedDataOnly: bool = Field(default=False)
    attributionsReportingEnabled: bool = Field(default=False)
    bloggingEnabled: bool = Field(default=False)
    botService: bool = Field(default=False)
    bulkRequestsEnabled: bool = Field(default=False)
    campaignsEnabled: bool = Field(default=False)
    campaignsReadOnly: bool = Field(default=False)
    cancelSubscriptionEnabled: bool = Field(default=False)
    communitiesEnabled: bool = Field(default=False)
    contactsEnabled: bool = Field(default=False)
    contentAiEnabled: bool = Field(default=False)
    conversationsEnabled: bool = Field(default=False)
    dashboardStatsEnabled: bool = Field(default=False)
    facebookAdsReportingEnabled: bool = Field(default=False)
    funnelsEnabled: bool = Field(default=False)
    invoiceEnabled: bool = Field(default=False)
    leadValueEnabled: bool = Field(default=False)
    marketingEnabled: bool = Field(default=False)
    membershipEnabled: bool = Field(default=False)
    onlineListingsEnabled: bool = Field(default=False)
    opportunitiesEnabled: bool = Field(default=False)
    paymentsEnabled: bool = Field(default=False)
    phoneCallEnabled: bool = Field(default=False)
    recordPaymentEnabled: bool = Field(default=False)
    refundsEnabled: bool = Field(default=False)
    reviewsEnabled: bool = Field(default=False)
    settingsEnabled: bool = Field(default=False)
    socialPlanner: bool = Field(default=False)
    tagsEnabled: bool = Field(default=False)
    triggersEnabled: bool = Field(default=False)
    websitesEnabled: bool = Field(default=False)
    workflowsEnabled: bool = Field(default=False)
    workflowsReadOnly: bool = Field(default=False)

class UserCreate(BaseModel):
    type: str = Field(..., description="Type of the webhook event")
    locationId: Optional[str] = Field(None, description="ID of the location (for sub-account user)")
    companyId: Optional[str] = Field(None, description="ID of the company (for agency user)")
    id: str = Field(..., description="Unique identifier for the user")
    firstName: str = Field(..., description="First name of the user")
    lastName: str = Field(..., description="Last name of the user")
    email: str = Field(..., description="Email of the user")
    phone: str = Field(..., description="Phone number of the user")
    extension: str = Field(..., description="Extension of the user's phone number")
    role: str = Field(..., description="Role of the user")
    permissions: UserPermissions = Field(..., description="Permissions of the user")
    locations: Optional[List[str]] = Field(None, description="List of location IDs (for agency user)")

    class Config:
        allow_population_by_field_name = True

# Example usage for sub-account user
sub_account_data = {
    "type": "UserCreate",
    "locationId": "ve9EPM428h8vShlRW1KT",
    "id": "ve9EPM428h8vShlRW1KT",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe+2@example.com",
    "phone": "+13235559998",
    "extension": "111",
    "role": "user",
    "permissions": {
        "adwordsReportingEnabled": True,
        "affiliateManagerEnabled": False,
        "agentReportingEnabled": True,
        # ... other permissions ...
    }
}

sub_account_user = UserCreate(**sub_account_data)

# Example usage for agency user
agency_data = {
    "type": "UserCreate",
    "companyId": "ve9EPM428h8vShlRW1KT",
    "id": "ve9EPM428h8vShlRW1KT",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe+3@example.com",
    "phone": "+13235559997",
    "extension": "1112",
    "role": "admin",
    "permissions": {
        "adwordsReportingEnabled": True,
        "affiliateManagerEnabled": False,
        "agentReportingEnabled": True,
        # ... other permissions ...
    },
    "locations": ["ve9EPM428h8vShlRW1KT"]
}

agency_user = UserCreate(**agency_data)