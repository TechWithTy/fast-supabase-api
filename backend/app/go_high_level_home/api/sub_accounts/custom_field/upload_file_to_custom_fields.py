from typing import Dict, Any, BinaryIO
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def upload_file_to_custom_fields(
    location_id: str,
    files: Dict[str, BinaryIO],
    headers: Dict[str, str],
    id: str = None,
    max_files: int = None
) -> Dict[str, Any]:
    """
    Upload files to custom fields in Go High Level.

    Args:
        location_id: The ID of the location
        files: Dictionary of files to upload (field name -> file object)
        headers: Dictionary containing Authorization and Version headers
        id: Contact ID, Opportunity ID, or Custom Field ID (optional)
        max_files: Maximum number of files to upload (optional)

    Returns:
        Dictionary containing the uploaded files data

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

    data = {}
    if id:
        data["id"] = id
    if max_files:
        data["maxFiles"] = str(max_files)

    url = f"{API_BASE_URL}/locations/{location_id}/customFields/upload"

    logging.info(f"Uploading files to custom fields for location: {location_id}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=request_headers,
                data=data,
                files=files
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise