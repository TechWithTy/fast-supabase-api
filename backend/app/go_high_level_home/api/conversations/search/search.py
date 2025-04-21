from typing import Dict, Any, Optional, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"

async def search_conversations(
    location_id: str,
    headers: Dict[str, str],
    assigned_to: Optional[str] = None,
    contact_id: Optional[str] = None,
    followers: Optional[str] = None,
    conversation_id: Optional[str] = None,
    last_message_action: Optional[str] = None,
    last_message_direction: Optional[str] = None,
    last_message_type: Optional[str] = None,
    limit: Optional[int] = 20,
    mentions: Optional[str] = None,
    query: Optional[str] = None,
    score_profile: Optional[str] = None,
    score_profile_max: Optional[int] = None,
    score_profile_min: Optional[int] = None,
    sort: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_score_profile: Optional[str] = None,
    start_after_date: Optional[Any] = None,
    status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search conversations based on various filters.
    
    Args:
        location_id: Location ID (required)
        headers: Dictionary containing Authorization and Version headers
        assigned_to: User IDs that conversations are assigned to (comma-separated)
        contact_id: Contact ID
        followers: User IDs of followers (comma-separated)
        conversation_id: ID of the conversation
        last_message_action: Action of the last outbound message (automated/manual)
        last_message_direction: Direction of the last message (inbound/outbound)
        last_message_type: Type of the last message
        limit: Maximum number of results to return (default: 20)
        mentions: User IDs of mentions (comma-separated)
        query: Search parameter string
        score_profile: ID of score profile for filtering
        score_profile_max: Maximum value for score
        score_profile_min: Minimum value for score
        sort: Sort parameter (asc/desc)
        sort_by: Field to sort by
        sort_score_profile: ID of score profile for sorting
        start_after_date: Search to begin after the specified date
        status: Status filter (all/read/unread/starred/recents)
        
    Returns:
        Dictionary containing conversations and total count
        
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
        "locationId": location_id
    }
    
    # Add optional parameters if provided
    if assigned_to:
        params["assignedTo"] = assigned_to
    if contact_id:
        params["contactId"] = contact_id
    if followers:
        params["followers"] = followers
    if conversation_id:
        params["id"] = conversation_id
    if last_message_action:
        params["lastMessageAction"] = last_message_action
    if last_message_direction:
        params["lastMessageDirection"] = last_message_direction
    if last_message_type:
        params["lastMessageType"] = last_message_type
    if limit:
        params["limit"] = limit
    if mentions:
        params["mentions"] = mentions
    if query:
        params["query"] = query
    if score_profile:
        params["scoreProfile"] = score_profile
    if score_profile_max:
        params["scoreProfileMax"] = score_profile_max
    if score_profile_min:
        params["scoreProfileMin"] = score_profile_min
    if sort:
        params["sort"] = sort
    if sort_by:
        params["sortBy"] = sort_by
    if sort_score_profile:
        params["sortScoreProfile"] = sort_score_profile
    if start_after_date:
        params["startAfterDate"] = start_after_date
    if status:
        params["status"] = status
    
    logging.info(f"Searching conversations with parameters: {params}")
    
    try:
        # Make the API request
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/conversations/search",
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
        logging.error(f"Error searching conversations: {str(e)}")
        raise