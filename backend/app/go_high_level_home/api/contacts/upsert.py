from typing import Dict, Any, List, Optional
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def upsert_contact(
    headers: Dict[str, str],
    location_id: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    name: Optional[str] = None,
    email: Optional[str] = None,
    gender: Optional[str] = None,
    phone: Optional[str] = None,
    address1: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    postal_code: Optional[str] = None,
    website: Optional[str] = None,
    timezone: Optional[str] = None,
    dnd: Optional[bool] = None,
    dnd_settings: Optional[Dict[str, Any]] = None,
    inbound_dnd_settings: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
    custom_fields: Optional[List[Dict[str, str]]] = None,
    source: Optional[str] = None,
    country: Optional[str] = None,
    company_name: Optional[str] = None,
    assigned_to: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Upsert a contact in Go High Level.
    
    If Allow Duplicate Contact is disabled under Settings, the global unique identifier 
    will be used for de-duplication. If the setting is enabled, a new contact will 
    get created with the shared details.
    """
    url = f"{API_BASE_URL}/contacts/upsert"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "locationId": location_id
    }
    
    optional_fields = {
        "firstName": first_name,
        "lastName": last_name,
        "name": name,
        "email": email,
        "gender": gender,
        "phone": phone,
        "address1": address1,
        "city": city,
        "state": state,
        "postalCode": postal_code,
        "website": website,
        "timezone": timezone,
        "dnd": dnd,
        "dndSettings": dnd_settings,
        "inboundDndSettings": inbound_dnd_settings,
        "tags": tags,
        "customFields": custom_fields,
        "source": source,
        "country": country,
        "companyName": company_name,
        "assignedTo": assigned_to
    }
    
    payload.update({k: v for k, v in optional_fields.items() if v is not None})
    
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