from typing import List, Dict, Union

class ContactDndUpdate:
    """
    Represents a contact's DND (Do Not Disturb) update.
    Called whenever a contact's dnd field is updated.
    """

    def __init__(self, data: Dict[str, Union[str, bool, Dict, List]]):
        self.type: str = data["type"]
        self.location_id: str = data["locationId"]
        self.id: str = data["id"]
        self.address1: str = data.get("address1", "")
        self.city: str = data.get("city", "")
        self.state: str = data.get("state", "")
        self.company_name: str = data.get("companyName", "")
        self.country: str = data.get("country", "")
        self.source: str = data.get("source", "")
        self.date_added: str = data["dateAdded"]
        self.date_of_birth: str = data.get("dateOfBirth", "")
        self.dnd: bool = data["dnd"]
        self.dnd_settings: Dict[str, Dict[str, str]] = data["dndSettings"]
        self.email: str = data.get("email", "")
        self.name: str = data.get("name", "")
        self.first_name: str = data.get("firstName", "")
        self.last_name: str = data.get("lastName", "")
        self.phone: str = data.get("phone", "")
        self.postal_code: str = data.get("postalCode", "")
        self.tags: List[str] = data.get("tags", [])
        self.website: str = data.get("website", "")
        self.attachments: List = data.get("attachments", [])
        self.assigned_to: str = data.get("assignedTo", "")
        self.custom_fields: List[Dict[str, Union[str, int, List, Dict]]] = data.get("customFields", [])

    def __str__(self):
        return f"ContactDndUpdate(id={self.id}, name={self.name}, dnd={self.dnd})"

# Example usage:
example_data = {
    "type": "ContactDndUpdate",
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
    "dndSettings": {
        "SMS": {"status": "inactive", "message": "Some message", "code": "101"},
        "Call": {"status": "inactive", "message": "Some message", "code": "101"},
        "Email": {"status": "active", "message": "Some message", "code": "101"},
        "GMB": {"status": "active", "message": "Some message", "code": "101"},
        "FB": {"status": "active", "message": "Some message", "code": "101"},
        "WhatsApp": {"status": "active", "message": "Some message", "code": "101"}
    },
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

contact_update = ContactDndUpdate(example_data)
print(contact_update)