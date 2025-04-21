from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_subscription(
    subscription_id: str,
    alt_id: str,
    alt_type: str,
    access_token: str
) -> Dict[str, Any]:
    """
    Get Subscription by ID.

    This function retrieves information for a specific subscription using its unique identifier.

    Args:
        subscription_id (str): ID of the subscription that needs to be returned.
        alt_id (str): AltId is the unique identifier e.g: location id.
        alt_type (str): AltType is the type of identifier (should be 'location').
        access_token (str): Access Token for authentication.

    Returns:
        Dict[str, Any]: A dictionary containing the subscription details.

    Raises:
        httpx.HTTPStatusError: If the API request fails.
    """
    url = f"{API_BASE_URL}/payments/subscriptions/{subscription_id}"
    
    params = {
        "altId": alt_id,
        "altType": alt_type
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Version": API_VERSION,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()