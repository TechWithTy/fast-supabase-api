import requests
import json

def create_send_invoice(headers, invoice_data):
    url = "https://services.leadconnectorhq.com/invoices/text2pay"
    headers.update({
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Version": "2021-07-28"
    })
    
    response = requests.post(url, headers=headers, json=invoice_data)
    return response.json()

# Example usage
headers = {
    "Authorization": "Bearer your_access_token_here"
}
invoice_data = {
    "altId": "6578278e879ad2646715ba9c",
    "altType": "location",
    "name": "New Invoice",
    "currency": "USD",
    "items": [
        {
            "name": "ABC Product",
            "description": "ABC Corp.",
            "productId": "6578278e879ad2646715ba9c",
            "priceId": "6578278e879ad2646715ba9c",
            "currency": "USD",
            "amount": 999,
            "qty": 1,
            "taxes": [
                {
                    "_id": "string",
                    "name": "string",
                    "rate": 0,
                    "calculation": "exclusive",
                    "description": "string",
                    "taxId": "string"
                }
            ],
            "automaticTaxCategoryId": "6578278e879ad2646715ba9c",
            "isSetupFeeItem": True,
            "type": "one_time",
            "taxInclusive": True
        }
    ],
    # ... (rest of the invoice data)
}

result = create_send_invoice(headers, invoice_data)
print(json.dumps(result, indent=2))