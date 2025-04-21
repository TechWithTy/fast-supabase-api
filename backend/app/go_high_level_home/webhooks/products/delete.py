from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Option(BaseModel):
    id: str
    name: str

class Variant(BaseModel):
    id: str
    name: str
    options: List[Option]

class Media(BaseModel):
    id: str
    title: str
    url: str
    type: str
    isFeatured: bool

class Product(BaseModel):
    _id: str
    description: Optional[str]
    variants: List[Variant]
    medias: List[Media]
    locationId: str
    name: str
    productType: str
    availableInStore: bool
    userId: str
    createdAt: datetime
    updatedAt: datetime
    statementDescriptor: Optional[str]
    image: Optional[str]

# Example usage
example_data = {
    "_id": "655b33a82209e60b6adb87a5",
    "description": "This is a really awesome product",
    "variants": [
        {
            "id": "38s63qmxfr4",
            "name": "Size",
            "options": [
                {
                    "id": "h4z7u0im2q8",
                    "name": "XL"
                }
            ]
        }
    ],
    "medias": [
        {
            "id": "fzrgusiuu0m",
            "title": "1dd7dcd0-e71d-4cf7-a06b-6d47723d6a29.png",
            "url": "https://storage.googleapis.com/ghl-test/3SwdhCsvxI8Au3KsPJt6/media/sample.png",
            "type": "image",
            "isFeatured": True
        }
    ],
    "locationId": "3SwdhCsvxI8Au3KsPJt6",
    "name": "Awesome Product",
    "productType": "PHYSICAL",
    "availableInStore": True,
    "userId": "6YAtzfzpmHAdj0e8GkKp",
    "createdAt": "2023-11-20T10:23:36.515Z",
    "updatedAt": "2024-01-23T09:57:04.846Z",
    "statementDescriptor": "abcde",
    "image": "https://storage.googleapis.com/ghl-test/3SwdhCsvxI8Au3KsPJt6/media/65af8d5df88bdb4b1022ee90.png"
}

product = Product(**example_data)

def handle_product_delete(product: Product):
    """
    Called whenever a product is deleted
    """
    # Add your logic here to handle the product deletion
    pass