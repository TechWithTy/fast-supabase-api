from typing import Dict, Any, Optional, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def get_email_campaigns(
    location_id: str,
    headers: Dict[str, str],
    archived: Optional[bool] = None,
    campaigns_only: Optional[bool] = None,
    email_status: Optional[str] = None,
    limit: Optional[int] = 10,
    limited_fields: Optional[bool] = None,
    name: Optional[str] = None,
    offset: Optional[int] = 0,
    parent_id: Optional[str] = None,
    show_stats: Optional[bool] = None,
    status: Optional[str] = "active"
) -> Dict[str, Any]:
    """
    Get email campaigns from the Go High Level API.
    
    Args:
        location_id: Location ID to fetch campaigns from
        headers: Dictionary containing Authorization and Version headers
        archived: Filter archived campaigns
        campaigns_only: Return only campaigns, excluding folders
        email_status: Filter by email delivery status
        limit: Maximum number of campaigns to return
        limited_fields: When true, returns only essential campaign fields
        name: Filter campaigns by name
        offset: Number of campaigns to skip for pagination
        parent_id: Filter campaigns by parent folder ID
        show_stats: When true, returns campaign statistics
        status: Filter by schedule status
        
    Returns:
        Dictionary containing the email campaigns data
        
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
    if archived is not None:
        params["archived"] = archived
    if campaigns_only is not None:
        params["campaignsOnly"] = campaigns_only
    if email_status:
        params["emailStatus"] = email_status
    if limit:
        params["limit"] = limit
    if limited_fields is not None:
        params["limitedFields"] = limited_fields
    if name:
        params["name"] = name
    if offset:
        params["offset"] = offset
    if parent_id:
        params["parentId"] = parent_id
    if show_stats is not None:
        params["showStats"] = show_stats
    if status:
        params["status"] = status
    
    logging.info(f"Making request to get email campaigns for location: {location_id}")
    
    try:
        # Make the API request to get email campaigns
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/emails/schedule",
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
        logging.error(f"Error getting email campaigns: {str(e)}")
        raise