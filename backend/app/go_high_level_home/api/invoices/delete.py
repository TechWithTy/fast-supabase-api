# backend/apps/go_high_level/api/invoices/delete.py
from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_invoice(
    invoice_id: str, 
    alt_id: str, 
    alt_type: str, 
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Delete an invoice by invoice ID.
    
    Args:
        invoice_id: The ID of the invoice to delete
        alt_id: Location ID or company ID based on altType
        alt_type: Alt Type (must be 'location')
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the deleted invoice data
        
    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    # Validate required headers
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")
    
    if not headers.get("Version"):
        # Set default version if not provided
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
    
    # Construct URL
    url = f"{API_BASE_URL}/invoices/{invoice_id}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=request_headers, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"Failed to delete invoice: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise Exception(f"Failed to delete invoice: {e}")