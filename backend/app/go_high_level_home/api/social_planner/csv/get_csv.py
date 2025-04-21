from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_csv_post(
    access_token: str,
    location_id: str,
    csv_id: str,
    limit: Optional[int] = None,
    skip: Optional[int] = None
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/social-media-posting/{location_id}/csv/{csv_id}"
    
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Version": API_VERSION
    }
    
    params = {}
    if limit is not None:
        params["limit"] = str(limit)
    if skip is not None:
        params["skip"] = str(skip)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()