from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def enable_saas_for_sub_account(
    location_id: str,
    headers: Dict[str, str],
    company_id: str,
    is_saas_v2: bool,
    stripe_account_id: Optional[str] = None,
    name: Optional[str] = None,
    email: Optional[str] = None,
    stripe_customer_id: Optional[str] = None,
    contact_id: Optional[str] = None,
    provider_location_id: Optional[str] = None,
    description: Optional[str] = None,
    saas_plan_id: Optional[str] = None,
    price_id: Optional[str] = None
) -> Dict[str, Any]:
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Invalid or missing Authorization header")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "channel": "OAUTH",
        "source": "INTEGRATION",
        "Content-Type": "application/json"
    }

    payload = {
        "companyId": company_id,
        "isSaaSV2": is_saas_v2
    }

    optional_fields = {
        "stripeAccountId": stripe_account_id,
        "name": name,
        "email": email,
        "stripeCustomerId": stripe_customer_id,
        "contactId": contact_id,
        "providerLocationId": provider_location_id,
        "description": description,
        "saasPlanId": saas_plan_id,
        "priceId": price_id
    }

    payload.update({k: v for k, v in optional_fields.items() if v is not None})

    url = f"{API_BASE_URL}/saas-api/public-api/enable-saas/{location_id}"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=request_headers)
        response.raise_for_status()
        return response.json()