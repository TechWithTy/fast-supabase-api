from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_media(
    headers: Dict[str, str],
    media_id: str,
    alt_id: str,
    alt_type: str
) -> Dict[str, Any]:
    """
    Delete a specific file or folder from the media library.

    Args:
        headers: Dictionary containing Authorization and Version headers
        media_id: The ID of the media to delete
        alt_id: Location or agency ID
        alt_type: AltType (must be 'location' or 'agency')

    Returns:
        Dictionary containing the deletion response

    Raises:
        ValueError: If required headers are missing
        Exception: If the API request fails
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }

    params = {
        "altId": alt_id,
        "altType": alt_type
    }

    logging.info(f"Deleting media with ID: {media_id}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{API_BASE_URL}/medias/{media_id}",
                headers=request_headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"Failed to delete media: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise Exception(f"An error occurred while deleting media: {e}")