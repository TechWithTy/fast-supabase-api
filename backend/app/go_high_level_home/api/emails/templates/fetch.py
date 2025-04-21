from typing import Dict, Any, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def fetch_email_templates(
    location_id: str,
    headers: Dict[str, str],
    archived: Optional[bool] = False,
    builder_version: Optional[str] = "2",
    limit: Optional[int] = 10,
    name: Optional[str] = None,
    offset: Optional[int] = 0,
    origin_id: Optional[str] = None,
    parent_id: Optional[str] = None,
    search: Optional[str] = None,
    sort_by_date: Optional[str] = "desc",
    templates_only: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Fetch email templates from Go High Level.
    
    Args:
        location_id: The ID of the location
        headers: Dictionary containing Authorization and Version headers
        archived: Filter archived templates
        builder_version: Builder version (1 or 2)
        limit: Maximum number of templates to return
        name: Filter templates by name
        offset: Number of templates to skip for pagination
        origin_id: Filter templates by origin ID
        parent_id: Filter templates by parent folder ID
        search: Search term for templates
        sort_by_date: Sort order for templates by date
        templates_only: Return only templates, excluding folders
        
    Returns:
        Dictionary containing the email templates data
        
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
    params = {
        "locationId": location_id,
        "archived": str(archived).lower(),
        "builderVersion": builder_version,
        "limit": limit,
        "offset": offset,
        "sortByDate": sort_by_date,
        "templatesOnly": str(templates_only).lower()
    }
    
    # Add optional parameters if provided
    if name:
        params["name"] = name
    if origin_id:
        params["originId"] = origin_id
    if parent_id:
        params["parentId"] = parent_id
    if search:
        params["search"] = search
    
    logging.info(f"Fetching email templates for location: {location_id}")
    
    try:
        # Make the API request to fetch email templates
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/emails/builder",
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
        logging.error(f"Error fetching email templates: {str(e)}")
        raise