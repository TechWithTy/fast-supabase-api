import httpx
from typing import Dict, Any

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_estimate(
    estimate_id: str,
    headers: Dict[str, str],
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update an existing estimate with new details.

    Args:
        estimate_id: The ID of the estimate to update
        headers: Dictionary containing Authorization and Version headers
        data: The estimate data to update

    Returns:
        Dictionary containing the updated estimate data

    Raises:
        httpx.HTTPStatusError: If the API request fails
        Exception: If required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    url = f"{API_BASE_URL}/invoices/estimate/{estimate_id}"

    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": headers["Version"]
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=request_headers, json=data)
        response.raise_for_status()
        return response.json()