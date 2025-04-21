from typing import Dict, Any, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def set_accounts(
    headers: Dict[str, str],
    location_id: str,
    account_ids: List[str],
    file_path: str,
    rows_count: int,
    file_name: str,
    approver: str = None,
    user_id: str = None
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/social-media-posting/{location_id}/set-accounts"

    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": headers.get("Version", API_VERSION)
    }

    data = {
        "accountIds": account_ids,
        "filePath": file_path,
        "rowsCount": rows_count,
        "fileName": file_name
    }

    if approver:
        data["approver"] = approver
    if user_id:
        data["userId"] = user_id

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=request_headers, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise