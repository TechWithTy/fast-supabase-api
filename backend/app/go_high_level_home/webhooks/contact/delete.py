from typing import Dict, Union, List

class Contact:
    """Called whenever a contact is deleted"""

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