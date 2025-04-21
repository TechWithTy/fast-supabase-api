from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def upload_csv(headers: Dict[str, str], location_id: str, file_path: str) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/social-media-posting/{location_id}/csv"

    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION)
    }

    async with httpx.AsyncClient() as client:
        with open(file_path, "rb") as file:
            files = {"file": file}
            response = await client.post(url, headers=request_headers, files=files)

    response.raise_for_status()
    return response.json()