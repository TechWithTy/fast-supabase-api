from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def void_invoice(
    invoice_id: str,
    alt_id: str,
    headers: Dict[str, str],
    alt_type: str = "location"
) -> Dict[str, Any]:
    """
    Void an invoice by invoice ID.

    Args:
        invoice_id: The ID of the invoice to void
        alt_id: Location ID or company ID based on altType
        headers: Dictionary containing Authorization and Version headers
        alt_type: Alt Type, defaults to "location"

    Returns:
        Dictionary containing the voided invoice data

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
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "altId": alt_id,
        "altType": alt_type
    }

    url = f"{API_BASE_URL}/invoices/{invoice_id}/void"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=request_headers, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise