from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def attach_tiktok_profile(
    headers: Dict[str, str],
    location_id: str,
    account_id: str,
    profile_type: str,
    origin_id: str,
    name: str,
    avatar: str,
    verified: bool,
    username: str,
    company_id: str
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/social-media-posting/oauth/{location_id}/tiktok/accounts/{account_id}"

    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": headers.get("Version", API_VERSION)
    }

    data = {
        "type": profile_type,
        "originId": origin_id,
        "name": name,
        "avatar": avatar,
        "verified": verified,
        "username": username,
        "companyId": company_id
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=request_headers, json=data)
        response.raise_for_status()
        return response.json()