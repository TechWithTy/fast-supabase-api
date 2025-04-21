from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_product(
    headers: Dict[str, str],
    name: str,
    location_id: str,
    product_type: str,
    description: str = None,
    image: str = None,
    statement_descriptor: str = None,
    available_in_store: bool = None,
    medias: list = None,
    variants: list = None
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/products/"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": headers.get("Version", API_VERSION)
    }
    
    payload = {
        "name": name,
        "locationId": location_id,
        "productType": product_type
    }
    
    optional_fields = {
        "description": description,
        "image": image,
        "statementDescriptor": statement_descriptor,
        "availableInStore": available_in_store,
        "medias": medias,
        "variants": variants
    }
    
    payload.update({k: v for k, v in optional_fields.items() if v is not None})
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=request_headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise