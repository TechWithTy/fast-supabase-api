from typing import Dict, Any
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_white_label_integration_provider(
    access_token: str,
    alt_id: str,
    alt_type: str,
    unique_name: str,
    title: str,
    provider: str,
    description: str,
    image_url: str
) -> Dict[str, Any]:
    """
    Create a White-label Integration Provider.

    Args:
        access_token (str): The access token for authentication.
        alt_id (str): Location Id / company Id based on altType.
        alt_type (str): Alt Type (e.g., 'location').
        unique_name (str): A unique name for the integration provider.
        title (str): The title or name of the integration provider.
        provider (str): The type of payment provider (e.g., 'authorize-net' or 'nmi').
        description (str): A brief description of the integration provider.
        image_url (str): The URL to an image representing the integration provider.

    Returns:
        Dict[str, Any]: The response data from the API.

    Raises:
        httpx.HTTPStatusError: If the API request fails.
    """
    url = f"{API_BASE_URL}/payments/integrations/provider/whitelabel"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Version": API_VERSION,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "altId": alt_id,
        "altType": alt_type,
        "uniqueName": unique_name,
        "title": title,
        "provider": provider,
        "description": description,
        "imageUrl": image_url
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()