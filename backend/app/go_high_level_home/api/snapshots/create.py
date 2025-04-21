from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_snapshot_share_link(
    headers: Dict[str, str],
    snapshot_id: str,
    share_type: str,
    company_id: str,
    relationship_number: Optional[str] = None,
    share_location_id: Optional[str] = None
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/snapshots/share/link"

    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    params = {"companyId": company_id}

    data = {
        "snapshot_id": snapshot_id,
        "share_type": share_type
    }

    if relationship_number:
        data["relationship_number"] = relationship_number
    if share_location_id:
        data["share_location_id"] = share_location_id

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=request_headers, params=params, json=data)
        response.raise_for_status()
        return response.json()