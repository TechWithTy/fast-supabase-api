from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_user(user_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Get user details from the Go High Level API.

    Args:
        user_id (str): The ID of the user to retrieve.
        headers (Dict[str, str]): The headers containing the authorization token.

    Returns:
        Dict[str, Any]: The user details.

    Raises:
        ValueError: If the Authorization header is missing or invalid.
        httpx.HTTPStatusError: If the API request fails.
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json"
    }

    logging.info(f"Making request to get user details for user ID: {user_id}")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/users/{user_id}", headers=request_headers)
        response.raise_for_status()
        return response.json()