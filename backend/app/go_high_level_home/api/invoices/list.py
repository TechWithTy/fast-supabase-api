from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def list_invoices(
    headers: Dict[str, str],
    alt_id: str,
    alt_type: str = "location",
    limit: int = 10,
    offset: int = 0,
    contact_id: Optional[str] = None,
    end_at: Optional[str] = None,
    payment_mode: Optional[str] = None,
    search: Optional[str] = None,
    sort_field: Optional[str] = None,
    sort_order: Optional[str] = None,
    start_at: Optional[str] = None,
    status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of invoices.
    
    Args:
        headers: Dictionary containing Authorization and Version headers
        alt_id: Location ID / company ID based on altType
        alt_type: Alt Type, defaults to "location"
        limit: Limit the number of items to return
        offset: Number of items to skip
        contact_id: Contact ID for the invoice
        end_at: End date in YYYY-MM-DD format
        payment_mode: Payment mode (default/live/test)
        search: Search for an invoice by id / name / email / phoneNo
        sort_field: The field on which sorting should be applied
        sort_order: The order of sort (ascend/descend)
        start_at: Start date in YYYY-MM-DD format
        status: Status to be filtered
        
    Returns:
        Dictionary containing the invoices and total count
        
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
        "altType": alt_type,
        "limit": limit,
        "offset": offset
    }
    
    # Add optional parameters if they exist
    if contact_id:
        params["contactId"] = contact_id
    if end_at:
        params["endAt"] = end_at
    if payment_mode:
        params["paymentMode"] = payment_mode
    if search:
        params["search"] = search
    if sort_field:
        params["sortField"] = sort_field
    if sort_order:
        params["sortOrder"] = sort_order
    if start_at:
        params["startAt"] = start_at
    if status:
        params["status"] = status
    
    # Make the API request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/invoices/",
                headers=request_headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"Failed to fetch invoices: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise Exception(f"An error occurred while fetching invoices: {e}")