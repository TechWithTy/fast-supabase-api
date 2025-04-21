from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def update_saas_subscription(
    location_id: str,
    headers: Dict[str, str],
    subscription_id: str,
    customer_id: str,
    company_id: str
) -> Dict[str, Any]:
    """
    Update SaaS subscription for given locationId and customerId.

    Args:
        location_id (str): The ID of the location.
        headers (Dict[str, str]): The headers containing the authorization token.
        subscription_id (str): The ID of the subscription to update.
        customer_id (str): The ID of the customer.
        company_id (str): The ID of the company.

    Returns:
        Dict[str, Any]: The response from the API.

    Raises:
        httpx.HTTPStatusError: If the API request fails.
        ValueError: If the Authorization header is missing or invalid.
    """
    url = f"{API_BASE_URL}/saas-api/public-api/update-saas-subscription/{location_id}"

    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": API_VERSION,
        "channel": "OAUTH",
        "source": "INTEGRATION"
    }

    data = {
        "subscriptionId": subscription_id,
        "customerId": customer_id,
        "companyId": company_id
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=request_headers, json=data)
        response.raise_for_status()
        return response.json()