from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_redirect(
    headers: Dict[str, str],
    location_id: str,
    domain: str,
    path: str,
    target: str,
    action: str
) -> Dict[str, Any]:
    """
    Create a new URL redirect in the system.

    Args:
        headers: Dictionary containing Authorization and Version headers
        location_id: Identifier of the location associated with the redirect
        domain: Domain where the redirect occurs
        path: Original path that will be redirected
        target: Target URL to which the original path will be redirected
        action: Action performed by the redirect (e.g., 'funnel', 'website', 'url', 'all')

    Returns:
        Dict containing details of the created redirect

    Raises:
        httpx.HTTPStatusError: If the API request fails
        Exception: If required headers are missing
    """
    url = f"{API_BASE_URL}/funnels/lookup/redirect"

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

    data = {
        "locationId": location_id,
        "domain": domain,
        "path": path,
        "target": target,
        "action": action
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=request_headers, json=data)
        response.raise_for_status()
        return response.json()