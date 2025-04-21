from typing import Dict, Any, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def disable_saas_for_locations(
    headers: Dict[str, str],
    company_id: str,
    location_ids: List[str]
) -> Dict[str, Any]:
    """
    Disable SaaS for locations for given locationIds.

    Args:
        headers: Dictionary containing Authorization and Version headers
        company_id: The company ID
        location_ids: List of location IDs to disable SaaS for

    Returns:
        Dict containing the API response

    Raises:
        Exception: If the Authorization header is missing or invalid
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    url = f"{API_BASE_URL}/saas-api/public-api/bulk-disable-saas/{company_id}"

    request_headers = {
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": headers.get("Version", API_VERSION),
        "channel": "OAUTH",
        "source": "INTEGRATION"
    }

    data = {"locationIds": location_ids}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=request_headers, json=data)
        response.raise_for_status()
        return response.json()