from typing import Dict, List, Union

class Invoice:
    """Called whenever an invoice is updated"""

    def __init__(self, data: Dict[str, Union[str, bool, int, float, Dict, List]]):
        self._id: str = data["_id"]
        self.status: str = data["status"]
        self.live_mode: bool = data["liveMode"]
        self.amount_paid: float = data["amountPaid"]
        self.alt_id: str = data["altId"]
        self.alt_type: str = data["altType"]
        self.name: str = data["name"]
        self.business_details: Dict[str, Union[str, List[str]]] = data["businessDetails"]
        self.invoice_number: str = data["invoiceNumber"]
        self.currency: str = data["currency"]
        self.contact_details: Dict[str, Union[str, List[str], Dict]] = data["contactDetails"]
        self.issue_date: str = data["issueDate"]
        self.due_date: str = data["dueDate"]
        self.discount: Dict[str, Union[str, float]] = data["discount"]
        self.invoice_items: List[Dict[str, Union[str, int, float, List]]] = data["invoiceItems"]
        self.total: float = data["total"]
        self.title: str = data["title"]
        self.amount_due: float = data["amountDue"]
        self.created_at: str = data["createdAt"]
        self.updated_at: str = data["updatedAt"]
        self.total_summary: Dict[str, float] = data["totalSummary"]

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, bool, int, float, Dict, List]]) -> 'Invoice':
        return cls(data)

# Example usage
example_data = {
    "_id": "6578278e879ad2646715ba9c",
    "status": "draft",
    "liveMode": False,
    "amountPaid": 0,
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
            {
                "email": "alex@example.com"
            }
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
    "amountDue": 999,
    "createdAt": "2023-12-12T09:27:42.355Z",
    "updatedAt": "2023-12-12T09:27:42.355Z",
    "totalSummary": {
        "subTotal": 999,
        "discount": 0
    }
}

invoice = Invoice.from_dict(example_data)