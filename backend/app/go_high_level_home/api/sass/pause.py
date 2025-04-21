from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def pause_sub_account(location_id: str, headers: Dict[str, str], paused: bool, company_id: str) -> Dict[str, Any]:
    """
    Pause Sub account for given locationId.

    Args:
        location_id (str): The ID of the location to pause.
        headers (Dict[str, str]): The headers containing the authorization token.
        paused (bool): Whether to pause the sub account.
        company_id (str): The ID of the company.

    Returns:
        Dict[str, Any]: The response from the API.

    Raises:
        httpx.HTTPStatusError: If the API request fails.
        ValueError: If the Authorization header is missing or invalid.
    """
    url = f"{API_BASE_URL}/saas-api/public-api/pause/{location_id}"
    
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": API_VERSION,
        "channel": "OAUTH",
        "source": "INTEGRATION",
        "Content-Type": "application/json"
    }
    
    data = {
        "paused": paused,
        "companyId": company_id
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=request_headers, json=data)
        response.raise_for_status()
        return response.json()