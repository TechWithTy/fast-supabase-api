from typing import List, Dict, Union

class Contact:
    """Called whenever a contact is created"""

    def __init__(self, data: Dict[str, Union[str, bool, List, Dict]]):
        self.type: str = data["type"]
        self.location_id: str = data["locationId"]
        self.id: str = data["id"]
        self.address1: str = data["address1"]
        self.city: str = data["city"]
        self.company_name: str = data["companyName"]
        self.country: str = data["country"]
        self.source: str = data["source"]
        self.date_added: str = data["dateAdded"]
        self.date_of_birth: str = data["dateOfBirth"]
        self.dnd: bool = data["dnd"]
        self.email: str = data["email"]
        self.name: str = data["name"]
        self.first_name: str = data["firstName"]
        self.last_name: str = data["lastName"]
        self.phone: str = data["phone"]
        self.postal_code: str = data["postalCode"]
        self.state: str = data["state"]
        self.tags: List[str] = data["tags"]
        self.website: str = data["website"]
        self.attachments: List = data["attachments"]
        self.assigned_to: str = data["assignedTo"]
        self.custom_fields: List[Dict[str, Union[str, int, List, Dict]]] = data["customFields"]

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, bool, List, Dict]]) -> 'Contact':
        return cls(data)

# Example usage
example_data = {
    "type": "ContactCreate",
    "locationId": "ve9EPM428h8vShlRW1KT",
    "id": "nmFmQEsNgz6AVpgLVUJ0",
    "address1": "3535 1st St N",
    "city": "ruDolomitebika",
    "state": "AL",
    "companyName": "Loram ipsum",
    "country": "DE",
    "source": "xyz form",
    "dateAdded": "2021-11-26T12:41:02.193Z",
    "dateOfBirth": "2000-01-05T00:00:00.000Z",
    "dnd": True,
    "email": "JohnDeo@gmail.comm",
    "name": "John Deo",
    "firstName": "John",
    "lastName": "Deo",
    "phone": "+919509597501",
    "postalCode": "452001",
    "tags": ["id magna sed Lorem", "Duis dolor commodo aliqua"],
    "website": "https://www.google.com/",
    "attachments": [],
    "assignedTo": "nmFmQEsNgz6AVpgLVUJ0",
    "customFields": [
        {
            "id": "BcdmQEsNgz6AVpgLVUJ0",
            "value": "XYZ Corp"
        }
    ]
}

contact = Contact.from_dict(example_data)