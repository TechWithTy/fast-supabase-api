from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def list_white_label_integration_providers(
    access_token: str,
    alt_id: str,
    alt_type: str = "location",
    limit: Optional[int] = None,
    offset: Optional[int] = None
) -> Dict[str, Any]:
    """
    Retrieve a paginated list of white-label integration providers.

    Args:
        access_token (str): The access token for authentication.
        alt_id (str): The location ID or company ID based on alt_type.
        alt_type (str, optional): The alt type. Defaults to "location".
        limit (int, optional): The maximum number of items per page.
        offset (int, optional): The starting index of the page.

    Returns:
        Dict[str, Any]: A dictionary containing the list of integration providers.

    Raises:
        httpx.HTTPStatusError: If the API request fails.
    """
    url = f"{API_BASE_URL}/payments/integrations/provider/whitelabel"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Version": API_VERSION,
        "Accept": "application/json"
    }
    
    params = {
        "altId": alt_id,
        "altType": alt_type
    }
    
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        
    return response.json()