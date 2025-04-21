import aiohttp
import json
from typing import Dict, Any, Optional

async def create_price_for_product(
    product_id: str,
    headers: Dict[str, str],
    name: str,
    price_type: str,
    currency: str,
    amount: float,
    location_id: str,
    recurring: Optional[Dict[str, Any]] = None,
    description: Optional[str] = None,
    membership_offers: Optional[list] = None,
    trial_period: Optional[int] = None,
    total_cycles: Optional[int] = None,
    setup_fee: Optional[float] = None,
    variant_option_ids: Optional[list] = None,
    compare_at_price: Optional[float] = None,
    user_id: Optional[str] = None,
    meta: Optional[Dict[str, Any]] = None,
    track_inventory: Optional[bool] = None,
    available_quantity: Optional[int] = None,
    allow_out_of_stock_purchases: Optional[bool] = None
) -> Dict[str, Any]:
    url = f"https://services.leadconnectorhq.com/products/{product_id}/price"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")
    
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", "2021-07-28"),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "name": name,
        "type": price_type,
        "currency": currency,
        "amount": amount,
        "locationId": location_id
    }

    optional_fields = {
        "recurring": recurring,
        "description": description,
        "membershipOffers": membership_offers,
        "trialPeriod": trial_period,
        "totalCycles": total_cycles,
        "setupFee": setup_fee,
        "variantOptionIds": variant_option_ids,
        "compareAtPrice": compare_at_price,
        "userId": user_id,
        "meta": meta,
        "trackInventory": track_inventory,
        "availableQuantity": available_quantity,
        "allowOutOfStockPurchases": allow_out_of_stock_purchases
    }

    payload.update({k: v for k, v in optional_fields.items() if v is not None})

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=request_headers, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()