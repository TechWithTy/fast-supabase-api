from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_opportunity_status(
    opportunity_id: str,
    status: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Update the status of an opportunity in Go High Level.

    Args:
        opportunity_id: The ID of the opportunity to update
        status: The new status of the opportunity (open, won, lost, abandoned, or all)
        headers: Dictionary containing Authorization and Version headers

    Returns:
        Dictionary containing the API response

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {"status": status}

    logging.info(f"Updating status for opportunity: {opportunity_id}")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.put(
                f"{API_BASE_URL}/opportunities/{opportunity_id}/status",
                headers=request_headers,
                json=data
            )

        response.raise_for_status()
        return response.json()

    except httpx.HTTPStatusError as e:
        logging.error(f"API request failed with status {e.response.status_code}: {e.response.text}")
        raise Exception(f"Failed to update opportunity status: {e}")