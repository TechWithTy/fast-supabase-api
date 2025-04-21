from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def get_location_stripe_id(
    headers: Dict[str, str],
    company_id: str,
    customer_id: Optional[str] = None,
    subscription_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get locations by stripeId with companyId.

    Args:
        headers (Dict[str, str]): The headers containing the authorization token.
        company_id (str): The ID of the company.
        customer_id (str, optional): The Stripe customer ID.
        subscription_id (str, optional): The Stripe subscription ID.

    Returns:
        Dict[str, Any]: The API response containing location information.

    Raises:
        httpx.HTTPStatusError: If the API request fails.
    """
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Invalid or missing Authorization header")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": API_VERSION,
        "channel": "OAUTH",
        "source": "INTEGRATION"
    }

    params = {"companyId": company_id}
    if customer_id:
        params["customerId"] = customer_id
    if subscription_id:
        params["subscriptionId"] = subscription_id

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/saas-api/public-api/locations",
            headers=request_headers,
            params=params
        )
        response.raise_for_status()
        return response.json()