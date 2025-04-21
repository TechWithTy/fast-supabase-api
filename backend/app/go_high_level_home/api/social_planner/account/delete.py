from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_social_media_account(
    headers: Dict[str, str],
    location_id: str,
    account_id: str,
    company_id: Optional[str] = None,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete a social media account and remove it from the group.

    Args:
        headers: Dictionary containing Authorization and Version headers
        location_id: The ID of the location
        account_id: The ID of the account to delete
        company_id: Optional company ID
        user_id: Optional user ID

    Returns:
        Dictionary containing the API response

    Raises:
        httpx.HTTPStatusError: If the API request fails
        Exception: If required headers are missing
    """
    url = f"{API_BASE_URL}/social-media-posting/{location_id}/accounts/{account_id}"

    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }

    params = {}
    if company_id:
        params["companyId"] = company_id
    if user_id:
        params["userId"] = user_id

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=request_headers, params=params)
        response.raise_for_status()
        return response.json()