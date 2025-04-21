from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_invoice_template(
    template_id: str,
    headers: Dict[str, str],
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update an invoice template by template ID.

    Args:
        template_id (str): The ID of the template to update.
        headers (Dict[str, str]): Headers containing Authorization and Version.
        data (Dict[str, Any]): The data to update the template with.

    Returns:
        Dict[str, Any]: The updated template data.

    Raises:
        ValueError: If required headers are missing.
        httpx.HTTPStatusError: If the API request fails.
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    url = f"{API_BASE_URL}/invoices/template/{template_id}"
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(url, json=data, headers=request_headers)
        response.raise_for_status()
        return response.json()