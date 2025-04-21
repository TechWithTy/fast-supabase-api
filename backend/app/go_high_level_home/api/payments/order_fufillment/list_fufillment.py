from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def list_fulfillment(
    order_id: str,
    alt_id: str,
    alt_type: str,
    access_token: str,
) -> Dict[str, Any]:
    """
    List all fulfillment history of an order.

    Args:
        order_id: ID of the order that needs to be returned
        alt_id: Location Id or Agency Id
        alt_type: Type of alt_id (must be 'location')
        access_token: Access Token for authentication

    Returns:
        Dictionary containing the fulfillment data

    Raises:
        httpx.HTTPStatusError: If the API request fails
    """
    url = f"{API_BASE_URL}/payments/orders/{order_id}/fulfillments"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Version": API_VERSION
    }

    params = {
        "altId": alt_id,
        "altType": alt_type
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()