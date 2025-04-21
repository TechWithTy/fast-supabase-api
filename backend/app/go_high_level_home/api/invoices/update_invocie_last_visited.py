from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_invoice_last_visited(
    invoice_id: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Update invoice last visited at by invoice ID.

    Args:
        invoice_id: The ID of the invoice
        headers: Dictionary containing Authorization and Version headers

    Returns:
        Dictionary containing the response data

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

    request_body = {
        "invoiceId": invoice_id
    }

    url = f"{API_BASE_URL}/invoices/stats/last-visited-at"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, headers=request_headers, json=request_body)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise