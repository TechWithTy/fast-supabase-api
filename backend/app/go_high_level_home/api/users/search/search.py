from typing import Dict, Any, Optional, List
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def search_users(
    access_token: str,
    company_id: str,
    enabled_2way_sync: Optional[bool] = None,
    ids: Optional[List[str]] = None,
    limit: int = 25,
    location_id: Optional[str] = None,
    query: Optional[str] = None,
    role: Optional[str] = None,
    skip: int = 0,
    sort: Optional[str] = None,
    sort_direction: Optional[str] = None,
    user_type: Optional[str] = None
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/users/search"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Version": API_VERSION,
        "Accept": "application/json"
    }

    params = {
        "companyId": company_id,
        "enabled2waySync": enabled_2way_sync,
        "ids": ",".join(ids) if ids else None,
        "limit": limit,
        "locationId": location_id,
        "query": query,
        "role": role,
        "skip": skip,
        "sort": sort,
        "sortDirection": sort_direction,
        "type": user_type
    }

    params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()