import aiohttp
import json
from typing import Dict, Any, Optional, List

async def create_invoice_template(
    headers: Dict[str, str],
    alt_id: str,
    alt_type: str = "location",
    internal: bool = True,
    name: str = "New Template",
    business_details: Optional[Dict[str, Any]] = None,
    currency: str = "USD",
    items: Optional[List[Dict[str, Any]]] = None,
    automatic_taxes_enabled: bool = True,
    discount: Optional[Dict[str, Any]] = None,
    terms_notes: Optional[str] = None,
    title: Optional[str] = None,
    tips_configuration: Optional[Dict[str, Any]] = None,
    late_fees_configuration: Optional[Dict[str, Any]] = None,
    invoice_number_prefix: Optional[str] = None,
    payment_methods: Optional[Dict[str, Any]] = None,
    attachments: Optional[List[str]] = None
) -> Dict[str, Any]:
    url = "https://services.leadconnectorhq.com/invoices/template"
    
    payload = {
        "altId": alt_id,
        "altType": alt_type,
        "internal": internal,
        "name": name,
        "businessDetails": business_details or {},
        "currency": currency,
        "items": items or [],
        "automaticTaxesEnabled": automatic_taxes_enabled,
        "discount": discount or {},
        "termsNotes": terms_notes,
        "title": title,
        "tipsConfiguration": tips_configuration or {},
        "lateFeesConfiguration": late_fees_configuration or {},
        "invoiceNumberPrefix": invoice_number_prefix,
        "paymentMethods": payment_methods or {},
        "attachments": attachments or []
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()