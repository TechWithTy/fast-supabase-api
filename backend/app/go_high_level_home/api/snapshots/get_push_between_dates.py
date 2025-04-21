from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_snapshot_push_between_dates(
    snapshot_id: str,
    company_id: str,
    from_date: str,
    to_date: str,
    headers: Dict[str, str],
    last_doc: Optional[str] = None,
    limit: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Get list of sub-accounts snapshot pushed in time period.

    Args:
        snapshot_id (str): The ID of the snapshot.
        company_id (str): The ID of the company.
        from_date (str): Start date in format 'MM-DD-YYYY HH:MM AM/PM'.
        to_date (str): End date in format 'MM-DD-YYYY HH:MM AM/PM'.
        headers (Dict[str, str]): Headers containing Authorization token.
        last_doc (str, optional): ID for last document to skip.
        limit (int, optional): Number of results to return. Defaults to 10.

    Returns:
        Dict[str, Any]: The response data containing snapshot push information.

    Raises:
        httpx.HTTPStatusError: If the API request fails.
        ValueError: If Authorization header is missing or invalid.
    """
    url = f"{API_BASE_URL}/snapshots/snapshot-status/{snapshot_id}"

    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }

    params = {
        "companyId": company_id,
        "from": from_date,
        "to": to_date,
        "limit": str(limit)
    }

    if last_doc:
        params["lastDoc"] = last_doc

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request_headers, params=params)
        response.raise_for_status()

    return response.json()