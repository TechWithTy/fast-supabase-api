from typing import Dict, Any, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def remove_opportunity_followers(
    opportunity_id: str,
    followers: List[str],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Remove followers from an opportunity.

    Args:
        opportunity_id: The ID of the opportunity
        followers: List of follower IDs to remove
        headers: Dictionary containing Authorization and Version headers

    Returns:
        Dictionary containing the API response

    Raises:
        ValueError: If required headers are missing
        Exception: If the API request fails
    """
    url = f"{API_BASE_URL}/opportunities/{opportunity_id}/followers"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=request_headers, json={"followers": followers})
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"Failed to remove opportunity followers: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise Exception(f"An error occurred while removing opportunity followers: {e}")