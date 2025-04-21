import httpx
from typing import Dict, Any

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_template_payment_method_config(
    template_id: str,
    alt_id: str,
    alt_type: str,
    enable_bank_debit_only: bool,
    headers: Dict[str, str]
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/invoices/template/{template_id}/payment-methods-configuration"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")

    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": headers.get("Version", API_VERSION)
    }
    
    payload = {
        "altId": alt_id,
        "altType": alt_type,
        "paymentMethods": {
            "stripe": {
                "enableBankDebitOnly": enable_bank_debit_only
            }
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.patch(url, json=payload, headers=request_headers)
        response.raise_for_status()
        return response.json()