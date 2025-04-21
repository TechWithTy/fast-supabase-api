from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_media_files(
    headers: Dict[str, str],
    alt_id: str,
    alt_type: str,
    sort_by: str,
    sort_order: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    parent_id: Optional[str] = None,
    query: Optional[str] = None,
    file_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch list of files and folders from the media library.

    Args:
        headers: Dictionary containing Authorization and Version headers
        alt_id: Location or agency ID
        alt_type: AltType (must be 'location' or 'agency')
        sort_by: Field to sort the file listing by
        sort_order: Direction in which files need to be sorted ('asc' or 'desc')
        limit: Number of files to show in the listing
        offset: Number of files to skip in listing
        parent_id: Parent id or folder id
        query: Query text
        file_type: Type of file

    Returns:
        Dictionary containing the media files data

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    headers["Accept"] = "application/json"

    params = {
        "altId": alt_id,
        "altType": alt_type,
        "sortBy": sort_by,
        "sortOrder": sort_order
    }

    if limit:
        params["limit"] = str(limit)
    if offset:
        params["offset"] = str(offset)
    if parent_id:
        params["parentId"] = parent_id
    if query:
        params["query"] = query
    if file_type:
        params["type"] = file_type

    url = f"{API_BASE_URL}/medias/files"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

    if response.status_code != 200:
        logging.error(f"Error fetching media files: {response.text}")
        raise Exception(f"Error fetching media files: {response.status_code}")

    return response.json()