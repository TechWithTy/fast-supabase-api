from typing import Dict, Any, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def update_rebilling(
    company_id: str,
    headers: Dict[str, str],
    product: str,
    location_ids: List[str],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update rebilling for given locationIds.

    Args:
        company_id: The ID of the company
        headers: Dictionary containing Authorization and Version headers
        product: The product string
        location_ids: List of location IDs
        config: Configuration object

    Returns:
        Dictionary containing the API response

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    url = f"{API_BASE_URL}/saas-api/public-api/update-rebilling/{company_id}"

    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": headers["Version"],
        "channel": "OAUTH",
        "source": "INTEGRATION"
    }

    data = {
        "product": product,
        "locationIds": location_ids,
        "config": config
    }

    logging.info(f"Updating rebilling for company: {company_id}")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, headers=request_headers, json=data)

        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"API request failed with status {e.response.status_code}: {e.response.text}")
        raise Exception(f"Failed to update rebilling: {e}")