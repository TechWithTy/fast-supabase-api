from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def import_courses(
    location_id: str,
    user_id: str,
    products: List[Dict[str, Any]],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Import courses through public channels.
    
    Args:
        location_id: The ID of the location
        user_id: The ID of the user
        products: List of product objects to import
        headers: Dictionary containing Authorization header
        
    Returns:
        Dictionary containing the response data
        
    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    # Validate required headers
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")
    
    # Prepare request headers
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": API_VERSION,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Prepare request payload
    payload = {
        "locationId": location_id,
        "userId": user_id,
        "products": products
    }
    
    # Make API request
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/courses/courses-exporter/public/import",
            headers=request_headers,
            json=payload
        )
        
        if response.status_code != 200:
            logging.error(f"Failed to import courses: {response.text}")
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
        
        return response.json()