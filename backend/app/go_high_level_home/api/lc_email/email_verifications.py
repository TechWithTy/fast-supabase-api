import httpx
import logging
from typing import Dict, Any

async def verify_email(
    headers: Dict[str, str],
    location_id: str,
    email: str
) -> Dict[str, Any]:
    """
    Verify an email address using the Go High Level API.

    Args:
        headers: Dictionary containing Authorization and Version headers
        location_id: The location ID for billing purposes
        email: The email address to verify

    Returns:
        Dictionary containing the email verification result

    Raises:
        Exception: If the API request fails or if required headers are missing
    """
    API_BASE_URL = "https://services.leadconnectorhq.com"

    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    if not headers.get("Version"):
        headers["Version"] = "2021-07-28"

    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers["Version"],
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    params = {"locationId": location_id}
    payload = {"type": "email", "verify": email}

    logging.info(f"Verifying email: {email}")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{API_BASE_URL}/email/verify",
                headers=request_headers,
                params=params,
                json=payload
            )

        response.raise_for_status()
        return response.json()

    except httpx.HTTPStatusError as e:
        logging.error(f"API request failed with status {e.response.status_code}: {e.response.text}")
        raise Exception(f"API request failed: {str(e)}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise