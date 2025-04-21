from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def delete_record(
    schema_key: str,
    record_id: str,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Delete a record by ID from the Go High Level API.
    
    Args:
        schema_key: The key of the Custom Object / Standard Object Schema. 
                   For custom objects, include the "custom_objects." prefix.
        record_id: ID of the record to be deleted.
        headers: Dictionary containing Authorization and Version headers
        
    Returns:
        Dictionary containing success status and ID of deleted object
        
    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    # Validate required headers
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        # Set default version if not provided
        headers["Version"] = API_VERSION
    
    # Prepare request headers
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json"
    }
    
    logging.info(f"Making request to delete record {record_id} from schema: {schema_key}")
    
    try:
        # Make the API request to delete record
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.delete(
                f"{API_BASE_URL}/objects/{schema_key}/records/{record_id}",
                headers=request_headers
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
            
        return response.json()
        
    except Exception as e:
        logging.error(f"Error deleting record: {str(e)}")
        raise