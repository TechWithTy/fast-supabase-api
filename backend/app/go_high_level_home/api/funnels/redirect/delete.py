from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_redirect_by_id(
    redirect_id: str,
    location_id: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Delete a URL redirect by its ID.

    Args:
        redirect_id: The ID of the redirect to delete
        location_id: The location ID
        headers: Dictionary containing Authorization and Version headers

    Returns:
        A dictionary containing the status of the delete operation
    """
    url = f"{API_BASE_URL}/funnels/lookup/redirect/{redirect_id}"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }
    
    params = {
        "locationId": location_id
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=request_headers, params=params)
        response.raise_for_status()
        return response.json()