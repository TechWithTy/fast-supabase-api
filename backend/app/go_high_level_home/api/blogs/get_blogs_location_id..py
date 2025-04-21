from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_blogs_by_location_id(
    location_id: str,
    headers: Dict[str, str],
    limit: int = 4,
    skip: int = 0,
    search_term: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get blogs by location ID from the Go High Level API.

    Args:
        location_id: The ID of the location to get blogs for
        headers: Dictionary containing Authorization and Version headers
        limit: Maximum number of blogs to return (default: 4)
        skip: Number of blogs to skip for pagination (default: 0)
        search_term: Optional search term to filter blogs by name

    Returns:
        Dictionary containing the blogs data

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

    params = {
        "locationId": location_id,
        "limit": limit,
        "skip": skip
    }

    if search_term:
        params["searchTerm"] = search_term

    logging.info(f"Getting blogs for location: {location_id}")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/blogs/site/all",
                headers=request_headers,
                params=params
            )

        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")

        return response.json()

    except httpx.RequestError as e:
        logging.error(f"An error occurred while making the request: {str(e)}")
        raise Exception(f"An error occurred while making the request: {str(e)}")