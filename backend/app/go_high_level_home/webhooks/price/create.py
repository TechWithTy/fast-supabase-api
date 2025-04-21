from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class MembershipOffer(BaseModel):
    label: str
    value: str
    _id: str

class Recurring(BaseModel):
    interval: str
    intervalCount: int

class Price(BaseModel):
    _id: str
    membershipOffers: List[MembershipOffer]
    variantOptionIds: List[str]
    locationId: str
    product: str
    userId: str
    name: str
    priceType: str
    currency: str
    amount: float
    recurring: Optional[Recurring]
    createdAt: datetime
    updatedAt: datetime
    compareAtPrice: Optional[float]
    trackInventory: Optional[bool]
    availableQuantity: Optional[int]
    allowOutOfStockPurchases: bool

def handle_price_create(price: Price):
    # Handle the price creation event
    print(f"New price created: {price.name}")
    # Add your logic here

# Example usage
example_data = {
    "_id": "655b33aa2209e60b6adb87a7",
    "membershipOffers": [
        {
            "label": "top_50",
            "value": "50",
            "_id": "655b33aa2209e60b6adb87a7"
        }
    ],
    "variantOptionIds": [
        "h4z7u0im2q8",
        "h3nst2ltsnn"
    ],
    "locationId": "3SwdhCsvxI8Au3KsPJt6",
    "product": "655b33a82209e60b6adb87a5",
    "userId": "6YAtzfzpmHAdj0e8GkKp",
    "name": "Red / S",
    "priceType": "one_time",
    "currency": "INR",
    "amount": 199999,
    "recurring": {
        "interval": "day",
        "intervalCount": 1
    },
    "createdAt": "2023-11-20T10:23:38.645Z",
    "updatedAt": "2024-01-23T09:57:04.852Z",
    "compareAtPrice": 2000000,
    "trackInventory": None,
    "availableQuantity": 5,
    "allowOutOfStockPurchases": True
}

price = Price(**example_data)
handle_price_create(price)