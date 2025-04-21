from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class NoteUpdate:
    type: str
    locationId: str
    id: str
    body: str
    contactId: str
    dateAdded: datetime
    
    @classmethod
    def from_dict(cls, data: dict) -> 'NoteUpdate':
        return cls(
            type=data['type'],
            locationId=data['locationId'],
            id=data['id'],
            body=data['body'],
            contactId=data['contactId'],
            dateAdded=datetime.fromisoformat(data['dateAdded'].rstrip('Z'))
        )

# Example usage
example_data = {
    "type": "NoteUpdate",
    "locationId": "ve9EPM428h8vShlRW1KT",
    "id": "otg8dTQqGLh3Q6iQI55w",
    "body": "Loram ipsum",
    "contactId": "CWBf1PR9LvvBkcYqiXlc",
    "dateAdded": "2021-11-26T12:41:02.193Z"
}

note_update = NoteUpdate.from_dict(example_data)
print(note_update)