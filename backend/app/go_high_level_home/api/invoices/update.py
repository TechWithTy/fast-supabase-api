import httpx
from typing import Dict, Any

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_invoice(headers: Dict[str, str], invoice_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    url = f"{API_BASE_URL}/invoices/{invoice_id}"
    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": headers.get("Version", API_VERSION)
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=request_headers, json=data)
        response.raise_for_status()
        return response.json()

# Example usage
invoice_id = "6578278e879ad2646715ba9c"
headers = {
    "Authorization": "Bearer your_access_token_here",
    "Version": "2021-07-28"
}

data = {
    "altId": "6578278e879ad2646715ba9c",
    "altType": "location",
    "name": "New Invoice",
    "title": "INVOICE",
    "currency": "USD",
    "description": "ABC Corp payments",
    "businessDetails": {
        "name": "ABC Corp.",
        "address": "9931 Beechwood, TX",
        "phoneNo": "+1-214-559-6993",
        "website": "wwww.example.com",
        "logoUrl": "https://example.com/logo.png",
        "customValues": ["string"]
    },
    "invoiceNumber": "1001",
    "contactId": "6578278e879ad2646715ba9c",
    "contactDetails": {
        "id": "6578278e879ad2646715ba9c",
        "name": "Alex",
        "phoneNo": "+1234567890",
        "email": "alex@example.com",
        "additionalEmails": [{"email": "alex@example.com"}],
        "companyName": "ABC Corp.",
        "address": {
            "addressLine1": "9931 Beechwood",
            "addressLine2": "Beechwood",
            "city": "St. Houston",
            "state": "TX",
            "countryCode": "US",
            "postalCode": "559-6993"
        },
        "customFields": ["string"]
    },
    "termsNotes": "<p>This is a default terms.</p>",
    "discount": {
        "value": 10,
        "type": "percentage",
        "validOnProductIds": "['6579751d56f60276e5bd4154']"
    },
    "invoiceItems": [{
        "name": "ABC Product",
        "description": "ABC Corp.",
        "productId": "6578278e879ad2646715ba9c",
        "priceId": "6578278e879ad2646715ba9c",
        "currency": "USD",
        "amount": 999,
        "qty": 1,
        "taxes": [{
            "_id": "string",
            "name": "string",
            "rate": 0,
            "calculation": "exclusive",
            "description": "string",
            "taxId": "string"
        }],
        "automaticTaxCategoryId": "6578278e879ad2646715ba9c",
        "isSetupFeeItem": True,
        "type": "one_time",
        "taxInclusive": True
    }],
    "automaticTaxesEnabled": True,
    "liveMode": True,
    "issueDate": "2023-01-01",
    "dueDate": "2023-01-14",
    "paymentSchedule": {
        "type": "percentage",
        "schedules": ["string"]
    },
    "tipsConfiguration": {
        "tipsPercentage": [5, 10, 15],
        "tipsEnabled": True
    },
    "xeroDetails": {},
    "invoiceNumberPrefix": "INV-",
    "paymentMethods": {
        "stripe": {
            "enableBankDebitOnly": False
        }
    },
    "attachments": [{
        "id": "6241712be68f7a98102ba272",
        "name": "Electronics.pdf",
        "url": "https://example.com/digital-delivery",
        "type": "string",
        "size": 10000
    }]
}

import asyncio

async def main():
    result = await update_invoice(headers, invoice_id, data)
    print(result)

asyncio.run(main())