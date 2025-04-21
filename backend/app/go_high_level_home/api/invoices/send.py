from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def send_invoice(
    invoice_id: str,
    alt_id: str,
    alt_type: str,
    user_id: str,
    action: str,
    live_mode: bool,
    headers: Dict[str, str],
    sent_from: Optional[Dict[str, str]] = None,
    auto_payment: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Send an invoice by invoice ID.

    Args:
        invoice_id: The ID of the invoice to send
        alt_id: Location ID or company ID based on altType
        alt_type: Alt Type (must be 'location')
        user_id: User ID for authorization
        action: Action to perform (sms_and_email, send_manually, email, sms)
        live_mode: Whether to use live mode
        headers: Dictionary containing Authorization and Version headers
        sent_from: Optional dictionary with sender details (fromName, fromEmail)
        auto_payment: Optional dictionary with auto-payment configuration

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

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=request_headers, json=payload)
        response.raise_for_status()
        return response.json()