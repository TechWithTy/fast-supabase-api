from typing import Dict, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def upload_media_file(
    headers: Dict[str, str],
    file: Optional[bytes] = None,
    hosted: Optional[bool] = None,
    file_url: Optional[str] = None,
    name: Optional[str] = None,
    parent_id: Optional[str] = None
) -> dict:
    """
    Upload a file to the Media Library.

    Args:
        headers: Dictionary containing Authorization and Version headers
        file: The file to upload (max 25MB)
        hosted: Boolean indicating if the file is hosted externally
        file_url: URL of the hosted file (required if hosted is True)
        name: Name of the file
        parent_id: ID of the parent folder

    Returns:
        Dictionary containing the uploaded file data

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    headers["Accept"] = "application/json"

    data = {}
    files = {}

    if hosted:
        data["hosted"] = "true"
        data["fileUrl"] = file_url
    elif file:
        files["file"] = file
    else:
        raise ValueError("Either 'file' or 'hosted' with 'file_url' must be provided")

    if name:
        data["name"] = name
    if parent_id:
        data["parentId"] = parent_id

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/medias/upload-file",
            headers=headers,
            data=data,
            files=files
        )

    if response.status_code != 200:
        logging.error(f"Error uploading file: {response.text}")
        raise Exception(f"Failed to upload file: {response.status_code}")

    return response.json()