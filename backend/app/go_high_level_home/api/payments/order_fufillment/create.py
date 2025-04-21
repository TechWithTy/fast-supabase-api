from typing import Dict, Any, List
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_order_fulfillment(
    order_id: str,
    access_token: str,
    alt_id: str,
    alt_type: str,
    trackings: List[Dict[str, str]],
    items: List[Dict[str, Any]],
    notify_customer: bool
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/payments/orders/{order_id}/fulfillments"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Version": API_VERSION
    }

    payload = {
        "altId": alt_id,
        "altType": alt_type,
        "trackings": trackings,
        "items": items,
        "notifyCustomer": notify_customer
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()