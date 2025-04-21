from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_invoice(
    invoice_id: str,
    alt_id: str,
    headers: Dict[str, str],
    alt_type: str = "location"
) -> Dict[str, Any]:
    """
    Get invoice by invoice ID.

    Args:
        invoice_id: The ID of the invoice
        alt_id: Location ID or company ID based on altType
        headers: Dictionary containing Authorization and Version headers
        alt_type: Alt Type, defaults to "location"

    Returns:
        Dictionary containing the invoice data

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    # Validate required headers
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    # Prepare request headers
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }

    # Prepare query parameters
    params = {
        "altId": alt_id,
        "altType": alt_type
    }

    logging.info(f"Getting invoice with ID: {invoice_id}")

    try:
        # Make the API request
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/invoices/{invoice_id}",
                headers=request_headers,
                params=params
            )

        # Handle the API response
        if response.status_code == 200:
            return response.json()
        else:
            error_message = f"Failed to get invoice. Status code: {response.status_code}. Response: {response.text}"
            logging.error(error_message)
            raise Exception(error_message)

    except httpx.RequestError as e:
        error_message = f"An error occurred while making the request: {str(e)}"
        logging.error(error_message)
        raise Exception(error_message)