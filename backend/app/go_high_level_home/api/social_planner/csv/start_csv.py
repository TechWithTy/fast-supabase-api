from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def start_csv_finalize(
    headers: Dict[str, str],
    location_id: str,
    csv_id: str,
    user_id: str
) -> Dict[str, Any]:
    """
    Start CSV finalization process.

    Args:
        headers: Dictionary containing Authorization and Version headers
        location_id: The ID of the location
        csv_id: The ID of the CSV
        user_id: The ID of the user

    Returns:
        Dictionary containing the API response

    Raises:
        httpx.HTTPStatusError: If the API request fails
        ValueError: If required headers are missing
    """
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    url = f"{API_BASE_URL}/social-media-posting/{location_id}/csv/{csv_id}"

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {"userId": user_id}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=request_headers, json=data)
        response.raise_for_status()
        return response.json()