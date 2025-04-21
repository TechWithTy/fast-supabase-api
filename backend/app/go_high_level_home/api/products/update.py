from typing import Dict, Any
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_product(
    product_id: str,
    product_data: Dict[str, Any],
    headers: Dict[str, str]
) -> Dict[str, Any]:
    """
    Update a product by ID using the Go High Level API.

    Args:
        product_id: The ID of the product to update
        product_data: Dictionary containing product details to update
        headers: Dictionary containing Authorization and Version headers

    Returns:
        Dictionary containing the updated product data

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = API_VERSION

    url = f"{API_BASE_URL}/products/{product_id}"

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    logging.info(f"Updating product with ID: {product_id}")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.put(url, headers=request_headers, json=product_data)

        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"API request failed with status {e.response.status_code}: {e.response.text}")
        raise Exception(f"Failed to update product: {e}")