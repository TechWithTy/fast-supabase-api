from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_order_by_id(
    order_id: str,
    alt_id: str,
    alt_type: str,
    access_token: str,
    location_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get Order by ID

    Retrieves information for a specific order using its unique identifier.

    Args:
        order_id: ID of the order that needs to be returned
        alt_id: AltId is the unique identifier e.g: location id
        alt_type: AltType is the type of identifier
        access_token: Access Token for authentication
        location_id: LocationId is the id of the sub-account (optional)

    Returns:
        Dictionary containing the order details

    Raises:
        httpx.HTTPStatusError: If the API request fails
    """
    url = f"{API_BASE_URL}/payments/orders/{order_id}"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Version": API_VERSION
    }

    params = {
        "altId": alt_id,
        "altType": alt_type
    }

    if location_id:
        params["locationId"] = location_id

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise