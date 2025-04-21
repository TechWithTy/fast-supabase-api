from typing import Dict, Any, Optional, List
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_estimate_template(
    headers: Dict[str, str],
    alt_id: str,
    name: str,
    business_details: Dict[str, Any],
    currency: str,
    items: List[Dict[str, Any]],
    live_mode: bool = True,
    discount: Optional[Dict[str, Any]] = None,
    terms_notes: Optional[str] = None,
    title: Optional[str] = None,
    automatic_taxes_enabled: bool = False,
    meta: Optional[Dict[str, Any]] = None,
    send_estimate_details: Optional[Dict[str, Any]] = None,
    estimate_number_prefix: Optional[str] = None,
    attachments: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/invoices/estimate/template"
    
    if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header")
    
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "altId": alt_id,
        "altType": "location",
        "name": name,
        "businessDetails": business_details,
        "currency": currency,
        "items": items,
        "liveMode": live_mode
    }
    
    if discount:
        payload["discount"] = discount
    if terms_notes:
        payload["termsNotes"] = terms_notes
    if title:
        payload["title"] = title
    if automatic_taxes_enabled is not None:
        payload["automaticTaxesEnabled"] = automatic_taxes_enabled
    if meta:
        payload["meta"] = meta
    if send_estimate_details:
        payload["sendEstimateDetails"] = send_estimate_details
    if estimate_number_prefix:
        payload["estimateNumberPrefix"] = estimate_number_prefix
    if attachments:
        payload["attachments"] = attachments
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=request_headers)
    
    response.raise_for_status()
    return response.json()