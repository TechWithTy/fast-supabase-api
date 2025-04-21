from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_invoice_schedule(
    schedule_id: str,
    alt_id: str,
    headers: Dict[str, str],
    alt_type: str = "location"
) -> Dict[str, Any]:
    """
    Delete an invoice schedule by schedule ID.

    Args:
        schedule_id: The ID of the schedule to delete
        alt_id: Location ID or company ID based on altType
        headers: Dictionary containing Authorization and Version headers
        alt_type: Alt Type, defaults to "location"

    Returns:
        Dictionary containing the success status

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    auth_token = headers.get("Authorization")
    if not auth_token or not auth_token.startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    version = headers.get("Version", API_VERSION)

    request_headers = {
        "Authorization": auth_token,
        "Version": version,
        "Accept": "application/json"
    }

    params = {
        "altId": alt_id,
        "altType": alt_type
    }

    url = f"{API_BASE_URL}/invoices/schedule/{schedule_id}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=request_headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise