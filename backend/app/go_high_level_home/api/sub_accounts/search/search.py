from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def search_sub_accounts(
    headers: Dict[str, str],
    company_id: Optional[str] = None,
    email: Optional[str] = None,
    limit: int = 10,
    order: str = "asc",
    skip: int = 0
) -> Dict[str, Any]:
    """
    Search Sub-Accounts (Formerly Locations)

    Args:
        headers: Dictionary containing request headers
        company_id: The company/agency id on which to perform the search
        email: Email to search for
        limit: The value by which the results should be limited (default: 10)
        order: The order in which the results should be returned (asc or desc, default: asc)
        skip: The value by which the results should be skipped (default: 0)

    Returns:
        Dict containing the search results
    """
    url = f"{API_BASE_URL}/locations/search"

    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Invalid or missing Authorization header")

    headers.update({
        "Accept": "application/json",
        "Version": API_VERSION
    })

    params = {
        "companyId": company_id,
        "email": email,
        "limit": limit,
        "order": order,
        "skip": skip
    }

    params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()