from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_invoice_templates(
    headers: Dict[str, str],
    alt_id: str,
    alt_type: str = "location",
    limit: int = 10,
    offset: int = 0,
    end_at: Optional[str] = None,
    payment_mode: Optional[str] = None,
    search: Optional[str] = None,
    start_at: Optional[str] = None,
    status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of invoice templates.
    
    Args:
        headers: Dictionary containing Authorization and Version headers
        alt_id: Location ID / company ID based on altType
        alt_type: Alt Type, defaults to "location"
        limit: Limit the number of items to return
        offset: Number of items to skip
        end_at: End date in YYYY-MM-DD format
        payment_mode: Payment mode (default/live/test)
        search: Search for a template by id / name / email / phoneNo
        start_at: Start date in YYYY-MM-DD format
        status: Status to be filtered
        
    Returns:
        Dictionary containing the invoice templates and total count
        
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
        "altType": alt_type,
        "limit": limit,
        "offset": offset
    }
    
    if end_at:
        params["endAt"] = end_at
    if payment_mode:
        params["paymentMode"] = payment_mode
    if search:
        params["search"] = search
    if start_at:
        params["startAt"] = start_at
    if status:
        params["status"] = status

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/invoices/template",
            headers=request_headers,
            params=params
        )
    
    if response.status_code != 200:
        logging.error(f"API request failed with status code {response.status_code}")
        raise Exception(f"API request failed: {response.text}")

    return response.json()