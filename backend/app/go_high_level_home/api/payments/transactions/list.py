from typing import Dict, Any, Optional
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def list_transactions(
    access_token: str,
    alt_id: str,
    alt_type: str,
    contact_id: Optional[str] = None,
    end_at: Optional[str] = None,
    entity_id: Optional[str] = None,
    entity_source_sub_type: Optional[str] = None,
    entity_source_type: Optional[str] = None,
    limit: int = 10,
    location_id: Optional[str] = None,
    offset: int = 0,
    payment_mode: Optional[str] = None,
    search: Optional[str] = None,
    start_at: Optional[str] = None,
    subscription_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    List Transactions API

    Retrieves a paginated list of transactions with optional filtering.

    Args:
        access_token (str): The access token for authentication.
        alt_id (str): The unique identifier (e.g., location id).
        alt_type (str): The type of identifier.
        contact_id (str, optional): Contact id for filtering transactions.
        end_at (str, optional): Closing interval of transactions (format: YYYY-MM-DD).
        entity_id (str, optional): Entity id for filtering transactions.
        entity_source_sub_type (str, optional): Source sub-type of the transactions.
        entity_source_type (str, optional): Source of the transactions.
        limit (int, optional): Maximum number of items per page. Defaults to 10.
        location_id (str, optional): ID of the sub-account.
        offset (int, optional): Starting index of the page. Defaults to 0.
        payment_mode (str, optional): Mode of payment.
        search (str, optional): Name of the transaction for searching.
        start_at (str, optional): Starting interval of transactions (format: YYYY-MM-DD).
        subscription_id (str, optional): Subscription id for filtering transactions.

    Returns:
        Dict[str, Any]: A dictionary containing the list of transactions and total count.
    """
    url = f"{API_BASE_URL}/payments/transactions"

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
        "entitySourceSubType": entity_source_sub_type,
        "entitySourceType": entity_source_type,
        "limit": limit,
        "locationId": location_id,
        "offset": offset,
        "paymentMode": payment_mode,
        "search": search,
        "startAt": start_at,
        "subscriptionId": subscription_id
    }

    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()