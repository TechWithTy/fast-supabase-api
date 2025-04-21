from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def list_orders(
    access_token: str,
    alt_id: str,
    alt_type: str,
    contact_id: Optional[str] = None,
    end_at: Optional[str] = None,
    funnel_product_ids: Optional[str] = None,
    limit: int = 10,
    location_id: Optional[str] = None,
    offset: int = 0,
    payment_mode: Optional[str] = None,
    search: Optional[str] = None,
    start_at: Optional[str] = None,
    status: Optional[str] = None
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/payments/orders"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Version": API_VERSION,
        "Accept": "application/json"
    }
    
    params = {
        "altId": alt_id,
        "altType": alt_type,
        "contactId": contact_id,
        "endAt": end_at,
        "funnelProductIds": funnel_product_ids,
        "limit": limit,
        "locationId": location_id,
        "offset": offset,
        "paymentMode": payment_mode,
        "search": search,
        "startAt": start_at,
        "status": status
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()