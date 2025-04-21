from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_redirect_by_id(
    redirect_id: str,
    target: str,
    action: str,
    location_id: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Update an existing URL redirect in the system.

    Args:
        redirect_id: Unique identifier of the redirect
        target: Target URL to which the original path will be redirected
        action: Action performed by the redirect (funnel, website, url, all)
        location_id: Identifier of the location associated with the redirect
        headers: Dictionary containing request headers including Authorization

    Returns:
        Dictionary containing details of the updated redirect

    Raises:
        httpx.HTTPStatusError: If the API request fails
        ValueError: If Authorization header is missing or invalid
    """
    url = f"{API_BASE_URL}/funnels/lookup/redirect/{redirect_id}"

    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    headers.update({
        "Version": API_VERSION,
        "Accept": "application/json",
        "Content-Type": "application/json"
    })

    data = {
        "target": target,
        "action": action,
        "locationId": location_id
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=data)
        
        if response.status_code != 200:
            logging.error(f"Failed to update redirect: {response.text}")
            response.raise_for_status()

        return response.json()["data"]