from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def list_subscriptions(
    access_token: str,
    alt_id: str,
    alt_type: str,
    contact_id: Optional[str] = None,
    end_at: Optional[str] = None,
    entity_id: Optional[str] = None,
    entity_source_type: Optional[str] = None,
    subscription_id: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    payment_mode: Optional[str] = None,
    search: Optional[str] = None,
    start_at: Optional[str] = None
) -> Dict[str, Any]:
    """
    List subscriptions from the Go High Level API.

    Args:
        access_token: The access token for authentication
        alt_id: AltId is the unique identifier e.g: location id
        alt_type: AltType is the type of identifier (must be 'location')
        contact_id: Contact ID for the subscription
        end_at: Closing interval of subscriptions
        entity_id: Entity id for filtering of subscriptions
        entity_source_type: Source of the subscriptions
        subscription_id: Subscription id for filtering of subscriptions
        limit: The maximum number of items to be included in a single page of results
        offset: The starting index of the page
        payment_mode: Mode of payment
        search: The name of the subscription for searching
        start_at: Starting interval of subscriptions

    Returns:
        Dictionary containing the subscriptions data

    Raises:
        httpx.HTTPStatusError: If the API request fails
    """
    url = f"{API_BASE_URL}/payments/subscriptions"

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
        "entityId": entity_id,
        "entitySourceType": entity_source_type,
        "id": subscription_id,
        "limit": limit,
        "offset": offset,
        "paymentMode": payment_mode,
        "search": search,
        "startAt": start_at
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()