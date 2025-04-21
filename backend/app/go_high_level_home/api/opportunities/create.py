from typing import Dict, Any, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_opportunity(
    headers: Dict[str, str],
    pipeline_id: str,
    location_id: str,
    name: str,
    status: str,
    contact_id: str,
    pipeline_stage_id: str = None,
    monetary_value: float = None,
    assigned_to: str = None,
    custom_fields: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create an opportunity in Go High Level.

    Args:
        headers: Dictionary containing Authorization and Version headers
        pipeline_id: The ID of the pipeline
        location_id: The ID of the location
        name: The name of the opportunity
        status: The status of the opportunity (open, won, lost, abandoned, all)
        contact_id: The ID of the associated contact
        pipeline_stage_id: The ID of the pipeline stage (optional)
        monetary_value: The monetary value of the opportunity (optional)
        assigned_to: The ID of the user the opportunity is assigned to (optional)
        custom_fields: List of custom fields (optional)

    Returns:
        Dictionary containing the created opportunity data

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

    data = {
        "pipelineId": pipeline_id,
        "locationId": location_id,
        "name": name,
        "status": status,
        "contactId": contact_id
    }

    if pipeline_stage_id:
        data["pipelineStageId"] = pipeline_stage_id
    if monetary_value is not None:
        data["monetaryValue"] = monetary_value
    if assigned_to:
        data["assignedTo"] = assigned_to
    if custom_fields:
        data["customFields"] = custom_fields

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/opportunities/",
                headers=request_headers,
                json=data
            )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise Exception(f"Failed to create opportunity: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise Exception(f"An error occurred while creating opportunity: {e}")