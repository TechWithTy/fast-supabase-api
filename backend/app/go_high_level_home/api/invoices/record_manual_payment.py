from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def send_invoice(
    invoice_id: str,
    alt_id: str,
    alt_type: str,
    user_id: str,
    action: str,
    headers: Dict[str, str],
    live_mode: bool = True,
    sent_from: Optional[Dict[str, str]] = None,
    auto_payment: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Send an invoice using GoHighLevel API
    
    Args:
        invoice_id: The ID of the invoice to send
        alt_id: Location ID or company ID
        alt_type: Alt type (must be 'location')
        user_id: User ID for authorization
        action: Action to perform (e.g., 'sms_and_email')
        headers: Dictionary containing Authorization and Version headers
        live_mode: Live mode flag
        sent_from: Sender details for invoice
        auto_payment: Auto-payment configuration
    
    Returns:
        Dictionary containing the sent invoice data
    
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
        "altType": alt_type,
        "userId": user_id,
        "action": action,
        "liveMode": live_mode
    }

    if sent_from:
        payload["sentFrom"] = sent_from

    if auto_payment:
        payload["autoPayment"] = auto_payment

    url = f"{API_BASE_URL}/invoices/{invoice_id}/send"

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