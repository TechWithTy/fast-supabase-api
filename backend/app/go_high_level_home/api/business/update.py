from typing import Dict, Any
import httpx
import logging

async def update_business(
    business_id: str,
    business_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Update a business in Go High Level API.
    
    Args:
        business_id: The ID of the business to update
        business_data: Dictionary containing business details to update
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the updated business data
        
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
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    logging.info(f"Making request to update business: {business_id}")
    
    try:
        # Make the API request to update business
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.put(
                f"{API_BASE_URL}/businesses/{business_id}",
                headers=request_headers,
                json=business_data
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error updating business: {str(e)}")
        raise