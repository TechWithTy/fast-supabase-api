from typing import Dict, Any
import httpx

async def update_sub_account(
    location_id: str,
    headers: Dict[str, str],
    data: Dict[str, Any],
    api_version: str = "2021-07-28"
) -> Dict[str, Any]:
    """
    Update a Sub-Account (Formerly Location) based on the data provided.

    Args:
        location_id (str): The ID of the location to update.
        headers (Dict[str, str]): Headers containing the authorization token.
        data (Dict[str, Any]): The data to update the sub-account with.
        api_version (str, optional): The API version to use. Defaults to "2021-07-28".

    Returns:
        Dict[str, Any]: The response from the API containing the updated sub-account information.

    Raises:
        ValueError: If the Authorization header is missing or invalid.
        httpx.HTTPStatusError: If the API request fails.
    """
    url = f"https://services.leadconnectorhq.com/locations/{location_id}"
    
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": api_version,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(url, json=data, headers=request_headers)
        response.raise_for_status()
        return response.json()