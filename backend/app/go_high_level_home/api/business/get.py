import httpx
import logging
from typing import Dict, Any

async def get_business(business_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Get business information from Go High Level API.
    
    Args:
        business_id: The ID of the business to retrieve
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the business data
        
    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    API_BASE_URL = "https://services.leadconnectorhq.com"
    
    # Validate required headers
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        # Set default version if not provided
        headers["Version"] = "2021-07-28"
    
    # Prepare request headers
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }
    
    logging.info(f"Making request to get business: {business_id}")
    
    try:
        # Make the API request to get business
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/businesses/{business_id}",
                headers=request_headers
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error getting business: {str(e)}")
        raise