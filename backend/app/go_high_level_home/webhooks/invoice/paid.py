from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class BusinessDetails(BaseModel):
    name: str
    address: str
    phoneNo: str
    website: str
    logoUrl: str
    customValues: List[str]

class Address(BaseModel):
    countryCode: str
    addressLine1: str
    addressLine2: str
    city: str
    state: str
    postalCode: str

class AdditionalEmail(BaseModel):
    email: str

class ContactDetails(BaseModel):
    id: str
    phoneNo: str
    email: str
    customFields: List[str]
    name: str
    address: Address
    additionalEmails: List[AdditionalEmail]
    companyName: str

class Discount(BaseModel):
    type: str
    value: float

class InvoiceItem(BaseModel):
    taxes: List[Dict]
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

class Invoice(BaseModel):
    _id: str
    status: str
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

def handle_paid_invoice(invoice: Invoice):
    """
    Called whenever an invoice is paid
    """
    # Process the paid invoice here
    print(f"Invoice {invoice.invoiceNumber} has been paid.")
    print(f"Amount paid: {invoice.amountPaid} {invoice.currency}")
    print(f"Customer: {invoice.contactDetails.name}")

# Example usage
example_invoice = Invoice(
    _id="6578278e879ad2646715ba9c",
    status="paid",
    liveMode=False,
    amountPaid=999,
    altId="6578278e879ad2646715ba9c",
    altType="location",
    name="New Invoice",
    businessDetails=BusinessDetails(
        name="ABC Corp.",
        address="9931 Beechwood, TX",
        phoneNo="+1-214-559-6993",
        website="wwww.example.com",
        logoUrl="https://example.com/logo.png",
        customValues=["string"]
    ),
    invoiceNumber="19",
    currency="USD",
    contactDetails=ContactDetails(
        id="6578278e879ad2646715ba9c",
        phoneNo="+1-214-559-6993",
        email="alex@example.com",
        customFields=["string"],
        name="Alex",
        address=Address(
            countryCode="US",
            addressLine1="9931 Beechwood",
            addressLine2="Beechwood",
            city="St. Houston",
            state="TX",
            postalCode="559-6993"
        ),
        additionalEmails=[AdditionalEmail(email="alex@example.com")],
        companyName="ABC Corp."
    ),
    issueDate="2023-01-01",
    dueDate="2023-01-01",
    discount=Discount(type="percentage", value=10),
    invoiceItems=[
        InvoiceItem(
            taxes=[],
            _id="c6tZZU0rJBf30ZXx9Gli",
            productId="c6tZZU0rJBf30ZXx9Gli",
            priceId="c6tZZU0rJBf30ZXx9Gli",
            currency="USD",
            name="Macbook Pro",
            qty=1,
            amount=999
        )
    ],
    total=999,
    title="INVOICE",
    amountDue=0,
    createdAt=datetime.fromisoformat("2023-12-12T09:27:42.355Z"),
    updatedAt=datetime.fromisoformat("2023-12-12T09:27:42.355Z"),
    totalSummary=TotalSummary(subTotal=999, discount=0)
)

handle_paid_invoice(example_invoice)