from typing import Dict, Any, Optional, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_custom_field(
    location_id: str,
    name: str,
    data_type: str,
    headers: Dict[str, str],
    placeholder: Optional[str] = None,
    accepted_format: Optional[List[str]] = None,
    is_multiple_file: Optional[bool] = None,
    max_number_of_files: Optional[int] = None,
    text_box_list_options: Optional[List[Dict[str, Any]]] = None,
    position: Optional[int] = None,
    model: Optional[str] = None
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/locations/{location_id}/customFields"

    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "name": name,
        "dataType": data_type
    }

    if placeholder:
        payload["placeholder"] = placeholder
    if accepted_format:
        payload["acceptedFormat"] = accepted_format
    if is_multiple_file is not None:
        payload["isMultipleFile"] = is_multiple_file
    if max_number_of_files:
        payload["maxNumberOfFiles"] = max_number_of_files
    if text_box_list_options:
        payload["textBoxListOptions"] = text_box_list_options
    if position is not None:
        payload["position"] = position
    if model:
        payload["model"] = model

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=request_headers, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise