from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_invoice_schedule(
    schedule_id: str,
    alt_id: str,
    headers: Dict[str, str],
    alt_type: str = "location"
) -> Dict[str, Any]:
    """
    Get an invoice schedule by schedule ID.

    Args:
        schedule_id: The ID of the schedule to retrieve
        alt_id: Location ID or company ID based on altType
        headers: Dictionary containing Authorization and Version headers
        alt_type: Alt Type, defaults to "location"

    Returns:
        Dictionary containing the invoice schedule details

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }

    params = {
        "altId": alt_id,
        "altType": alt_type
    }

    url = f"{API_BASE_URL}/invoices/schedule/{schedule_id}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=request_headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise