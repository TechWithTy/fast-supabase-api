from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def generate_invoice_number(
    headers: Dict[str, str],
    alt_id: str,
    alt_type: str = "location"
) -> Dict[str, Any]:
    """
    Generate the next invoice number for a given location.
    
    Args:
        headers: Dictionary containing Authorization and Version headers
        alt_id: Location ID
        alt_type: Alt Type, defaults to "location"
        
    Returns:
        Dictionary containing the generated invoice number
        
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
    
    logging.info(f"Generating invoice number for {alt_type} ID: {alt_id}")
    
    try:
        # Make the API request
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/invoices/generate-invoice-number",
                headers=request_headers,
                params=params
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"Failed to generate invoice number: {error_detail}")
            
        return response.json()
        
    except httpx.RequestError as e:
        logging.error(f"Request error: {str(e)}")
        raise Exception(f"Network error when generating invoice number: {str(e)}")