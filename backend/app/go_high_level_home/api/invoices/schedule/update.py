import httpx
from typing import List, Dict, Optional
from datetime import datetime

async def update_schedule(schedule_id: str, headers: Dict[str, str], alt_id: str, alt_type: str, name: str,
                          contact_details: Dict, schedule: Dict, live_mode: bool, business_details: Dict,
                          currency: str, items: List[Dict], discount: Optional[Dict] = None,
                          terms_notes: Optional[str] = None, title: Optional[str] = None,
                          attachments: Optional[List[Dict]] = None) -> Dict:
    url = f"https://services.leadconnectorhq.com/invoices/schedule/{schedule_id}"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")
    
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", "2021-07-28"),
        "Accept": "application/json"
    }
    
    payload = {
        "altId": alt_id,
        "altType": alt_type,
        "name": name,
        "contactDetails": contact_details,
        "schedule": schedule,
        "liveMode": live_mode,
        "businessDetails": business_details,
        "currency": currency,
        "items": items
    }
    
    if discount:
        payload["discount"] = discount
    if terms_notes:
        payload["termsNotes"] = terms_notes
    if title:
        payload["title"] = title
    if attachments:
        payload["attachments"] = attachments
    
    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=request_headers, json=payload)
        response.raise_for_status()
    
    return response.json()