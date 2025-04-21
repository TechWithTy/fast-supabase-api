import httpx
from typing import Dict, Any

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_business(business_id: str, headers: Dict[str, str]) -> Dict[str, bool]:
    """
    Delete a business by ID using the Go High Level API.
    
    :param business_id: The ID of the business to delete.
    :param headers: Dictionary containing Authorization and Version headers.
    :return: JSON response data from the API.
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    url = f"{API_BASE_URL}/businesses/{business_id}"
    
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=request_headers)
    
    if not response.is_success:
        raise Exception(f"Error deleting business: {response.text}")
        
    return response.json()