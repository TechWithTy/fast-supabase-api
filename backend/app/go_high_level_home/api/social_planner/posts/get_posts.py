from typing import Dict, Any, Optional
import httpx
import json

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_posts(
    location_id: str,
    headers: Dict[str, str],
    post_type: str = "all",
    accounts: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    include_users: bool = True,
    post_type_filter: str = "post"
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/social-media-posting/{location_id}/posts/list"
    
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")
    
    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": headers.get("Version", API_VERSION)
    }
    
    params = {
        "type": post_type,
        "skip": str(skip),
        "limit": str(limit),
        "includeUsers": str(include_users).lower(),
        "postType": post_type_filter
    }
    
    if accounts:
        params["accounts"] = accounts
    if from_date:
        params["fromDate"] = from_date
    if to_date:
        params["toDate"] = to_date
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=request_headers, json=params)
    
    response.raise_for_status()
    return response.json()