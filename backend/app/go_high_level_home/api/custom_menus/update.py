from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_custom_menu(headers: Dict[str, str], custom_menu_id: str) -> Dict[str, Any]:
    """
    Delete a custom menu.

    Args:
        headers (Dict[str, str]): The headers containing the authorization token.
        custom_menu_id (str): The ID of the custom menu to delete.

    Returns:
        Dict[str, Any]: A dictionary containing the API response.

    Raises:
        ValueError: If the Authorization header is missing or invalid.
        httpx.HTTPStatusError: If the API request fails.
    """
    url = f"{API_BASE_URL}/custom-menus/{custom_menu_id}"

    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=request_headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise