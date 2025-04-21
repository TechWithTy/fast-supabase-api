from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def generate_estimate_number(
    headers: Dict[str, str],
    alt_id: str,
    alt_type: str = "location"
) -> Dict[str, Any]:
    """
    Generate the next estimate number for a given location.
    
    Args:
        headers: Dictionary containing Authorization header
        alt_id: Location ID or Agency ID
        alt_type: Alt Type, defaults to "location"
        
    Returns:
        Dictionary containing the generated estimate number and trace ID
        
    Raises:
        httpx.HTTPStatusError: If the API request fails
        ValueError: If Authorization header is missing or invalid
    """
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    url = f"{API_BASE_URL}/invoices/estimate/number/generate"
    
    params = {
        "altId": alt_id,
        "altType": alt_type
    }
    
    headers["Version"] = API_VERSION
    headers["Accept"] = "application/json"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()