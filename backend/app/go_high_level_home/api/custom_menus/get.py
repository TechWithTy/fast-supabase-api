from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_custom_menu(custom_menu_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Fetch a single custom menu based on its ID from the Go High Level API.

    Args:
        custom_menu_id: The unique identifier of the custom menu
        headers: Dictionary containing Authorization and Version headers

    Returns:
        Dictionary containing the custom menu data

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }

    logging.info(f"Making request to get custom menu: {custom_menu_id}")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/custom-menus/{custom_menu_id}",
                headers=request_headers
            )

        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")

        return response.json()
    except httpx.RequestError as e:
        logging.error(f"An error occurred while making the request: {str(e)}")
        raise Exception(f"An error occurred while making the request: {str(e)}")