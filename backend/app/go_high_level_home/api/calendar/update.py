from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def update_calendar(
    calendar_id: str,
    calendar_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Update a calendar by ID in Go High Level.
    
    Args:
        calendar_id: The ID of the calendar to update
        calendar_data: Dictionary containing calendar details to update
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing the updated calendar data
        
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
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    logging.info(f"Updating calendar with ID: {calendar_id}")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.put(
                f"{API_BASE_URL}/calendars/{calendar_id}",
                headers=request_headers,
                json=calendar_data
            )

        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")

        return response.json()
    except Exception as e:
        logging.error(f"Error updating calendar: {str(e)}")
        raise