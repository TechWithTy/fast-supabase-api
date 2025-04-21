import httpx
from typing import Dict, Any, Optional

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_scheduled_invoice(
    schedule_id: str,
    headers: Dict[str, str],
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update scheduled recurring invoice.

    Args:
        schedule_id: The ID of the schedule to update
        headers: Headers containing the Authorization token
        data: The invoice data to update

    Returns:
        Dictionary containing the updated invoice data

    Raises:
        httpx.HTTPStatusError: If the API request fails
        ValueError: If Authorization header is missing or invalid
    """
    url = f"{API_BASE_URL}/invoices/schedule/{schedule_id}/updateAndSchedule"

    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    default_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Version": API_VERSION
    }
    default_headers.update(headers)

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=default_headers, json=data)
        response.raise_for_status()
        return response.json()