from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class Address(BaseModel):
    countryCode: str
    addressLine1: str
    addressLine2: str
    city: str
    state: str
    postalCode: str

class BusinessDetails(BaseModel):
    name: str
    address: str
    phoneNo: str
    website: str
    logoUrl: str
    customValues: List[str]

class ContactDetails(BaseModel):
    id: str
    phoneNo: str
    email: str
    customFields: List[str]
    name: str
    address: Address
    additionalEmails: List[Dict[str, str]]
    companyName: str

class Discount(BaseModel):
    type: str
    value: float

class InvoiceItem(BaseModel):
    taxes: List[Any] = []
    _id: str
    productId: str
    priceId: str
    currency: str
    name: str
    qty: int
    amount: float

class TotalSummary(BaseModel):
    subTotal: float
    discount: float

class PartiallyPaidInvoice(BaseModel):
    _id: str
    status: str = Field(..., example="partially_paid")
    liveMode: bool
    amountPaid: float
    altId: str
    altType: str
    name: str
    businessDetails: BusinessDetails
    invoiceNumber: str
    currency: str
    contactDetails: ContactDetails
    issueDate: str
    dueDate: str
    discount: Discount
    invoiceItems: List[InvoiceItem]
    total: float
    title: str
    amountDue: float
    createdAt: datetime
    updatedAt: datetime
    totalSummary: TotalSummary

def handle_partially_paid_invoice(invoice: PartiallyPaidInvoice):
    """
    Called whenever an invoice is partially paid
    """
    # Add your logic here to handle the partially paid invoice
    print(f"Invoice {invoice.invoiceNumber} partially paid. Amount paid: {invoice.amountPaid}")

# Example usage
example_data = {
    "_id": "6578278e879ad2646715ba9c",
    "status": "partially_paid",
    "liveMode": False,
    "amountPaid": 899,
    "altId": "6578278e879ad2646715ba9c",
    "altType": "location",
    "name": "New Invoice",
    "businessDetails": {
        "name": "ABC Corp.",
        "address": "9931 Beechwood, TX",
        "phoneNo": "+1-214-559-6993",
        "website": "wwww.example.com",
        "logoUrl": "https://example.com/logo.png",
        "customValues": ["string"]
    },
    "invoiceNumber": "19",
    "currency": "USD",
    "contactDetails": {
        "id": "6578278e879ad2646715ba9c",
        "phoneNo": "+1-214-559-6993",
        "email": "alex@example.com",
        "customFields": ["string"],
        "name": "Alex",
        "address": {
            "countryCode": "US",
            "addressLine1": "9931 Beechwood",
            "addressLine2": "Beechwood",
            "city": "St. Houston",
            "state": "TX",
            "postalCode": "559-6993"
        },
        "additionalEmails": [
            {"email": "alex@example.com"}
        ],
        "companyName": "ABC Corp."
    },
    "issueDate": "2023-01-01",
    "dueDate": "2023-01-01",
    "discount": {
        "type": "percentage",
        "value": 10
    },
    "invoiceItems": [
        {
            "taxes": [],
            "_id": "c6tZZU0rJBf30ZXx9Gli",
            "productId": "c6tZZU0rJBf30ZXx9Gli",
            "priceId": "c6tZZU0rJBf30ZXx9Gli",
            "currency": "USD",
            "name": "Macbook Pro",
            "qty": 1,
            "amount": 999
        }
    ],
    "total": 999,
    "title": "INVOICE",
    "amountDue": 100,
    "createdAt": "2023-12-12T09:27:42.355Z",
    "updatedAt": "2023-12-12T09:27:42.355Z",
    "totalSummary": {
        "subTotal": 999,
        "discount": 0
    }
}

invoice = PartiallyPaidInvoice(**example_data)
handle_partially_paid_invoice(invoice)