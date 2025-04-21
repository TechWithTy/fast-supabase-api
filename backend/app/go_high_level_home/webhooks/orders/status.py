from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ContactSnapshot(BaseModel):
    id: str
    locationId: str
    firstName: str
    lastName: str
    email: str
    phone: str
    dnd: bool
    source: str
    address1: str
    city: str
    state: str
    postalCode: str
    tags: List[str]
    country: str
    dateAdded: datetime

class TaxSummary(BaseModel):
    _id: str
    name: str
    calculation: str
    rate: float
    amount: float

class AmountSummary(BaseModel):
    subtotal: float
    discount: float
    tax: float
    shipping: float

class SourceMeta(BaseModel):
    stepId: str
    pageId: str
    domain: str
    pageUrl: str

class Source(BaseModel):
    type: str
    subType: str
    id: str
    name: str
    meta: SourceMeta

class VariantOption(BaseModel):
    id: str
    name: str

class Variant(BaseModel):
    id: str
    name: str
    options: List[VariantOption]

class Product(BaseModel):
    _id: str
    name: str
    availableInStore: bool
    taxes: List[dict] = []
    variants: List[Variant]
    description: Optional[str] = None

class Price(BaseModel):
    _id: str
    name: str
    type: str
    currency: str
    amount: float
    variantOptionIds: List[str]

class OrderItem(BaseModel):
    name: str
    qty: int
    product: Product
    price: Price

class OrderStatusUpdate(BaseModel):
    type: str
    locationId: str
    _id: str
    altId: str
    altType: str
    status: str
    taxSummary: List[TaxSummary]
    fulfillmentStatus: str
    contactId: str
    currency: str
    amount: float
    liveMode: bool
    amountSummary: AmountSummary
    source: Source
    createdAt: datetime
    updatedAt: datetime
    contactSnapshot: ContactSnapshot
    items: List[OrderItem]

    class Config:
        allow_population_by_field_name = True

# Example usage:
# order_data = {...}  # Your JSON data here
# order = OrderStatusUpdate(**order_data)