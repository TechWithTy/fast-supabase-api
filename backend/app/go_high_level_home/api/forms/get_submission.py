from typing import Dict, Any, Optional, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_form_submissions(
    location_id: str,
    headers: Dict[str, str],
    form_id: Optional[str] = None,
    start_at: Optional[str] = None,
    end_at: Optional[str] = None,
    q: Optional[str] = None,
    limit: Optional[int] = 20,
    page: Optional[int] = 1
) -> Dict[str, Any]:
    """
    Get form submissions from the Go High Level API.
    
    Args:
        location_id: The ID of the location (required)
        headers: Dictionary containing Authorization and Version headers
        form_id: Filter submission by form id
        start_at: Get submissions starting from this date (YYYY-MM-DD)
        end_at: Get submissions ending at this date (YYYY-MM-DD)
        q: Filter by contactId, name, email or phone number
        limit: Maximum number of records to return (default: 20, max: 100)
        page: Page number (default: 1)
        
    Returns:
        Dictionary containing the form submissions data
        
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
    
    # Prepare query parameters
    params = {"locationId": location_id}
    if form_id:
        params["formId"] = form_id
    if start_at:
        params["startAt"] = start_at
    if end_at:
        params["endAt"] = end_at
    if q:
        params["q"] = q
    if limit:
        params["limit"] = limit
    if page:
        params["page"] = page
    
    logging.info(f"Making request to get form submissions for location: {location_id}")
    
    try:
        # Make the API request to get form submissions
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/forms/submissions",
                headers=request_headers,
                params=params
            )
            
        # Handle the API response
        if response.status_code != 200:
            error_detail = response.text
            logging.error(f"API request failed with status {response.status_code}: {error_detail}")
            raise Exception(f"API request failed with status {response.status_code}: {error_detail}")
        
        return response.json()
        
    except Exception as e:
        logging.error(f"Error fetching form submissions: {str(e)}")
        raise