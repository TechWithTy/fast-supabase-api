from pydantic import BaseModel, Field
from typing import List, Optional
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
    type: str
    currency: str
    amount: int
    recurring: Optional[Recurring]
    createdAt: datetime
    updatedAt: datetime
    compareAtPrice: Optional[int]
    trackInventory: Optional[bool]
    availableQuantity: Optional[int]
    allowOutOfStockPurchases: bool

def handle_price_delete(price: Price):
    """
    Called whenever a price is deleted
    """
    # Add your logic here to handle the deleted price
    print(f"Price {price.name} with ID {price._id} has been deleted.")
    # You might want to update related records, notify systems, etc.

# Example usage
example_price = Price(
    _id="655b33aa2209e60b6adb87a7",
    membershipOffers=[
        MembershipOffer(label="top_50", value="50", _id="655b33aa2209e60b6adb87a7")
    ],
    variantOptionIds=["h4z7u0im2q8", "h3nst2ltsnn"],
    locationId="3SwdhCsvxI8Au3KsPJt6",
    product="655b33a82209e60b6adb87a5",
    userId="6YAtzfzpmHAdj0e8GkKp",
    name="Red / S",
    type="one_time",
    currency="INR",
    amount=199999,
    recurring=Recurring(interval="day", intervalCount=1),
    createdAt=datetime.fromisoformat("2023-11-20T10:23:38.645Z"),
    updatedAt=datetime.fromisoformat("2024-01-23T09:57:04.852Z"),
    compareAtPrice=2000000,
    trackInventory=None,
    availableQuantity=5,
    allowOutOfStockPurchases=True
)

handle_price_delete(example_price)