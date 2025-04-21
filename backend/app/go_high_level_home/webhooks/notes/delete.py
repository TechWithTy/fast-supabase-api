from typing import Dict, Any
from datetime import datetime

class NoteDelete:
    def __init__(self, data: Dict[str, Any]):
        self.type: str = data['type']
        self.location_id: str = data['locationId']
        self.id: str = data['id']
        self.body: str = data['body']
        self.contact_id: str = data['contactId']
        self.date_added: datetime = datetime.fromisoformat(data['dateAdded'].replace('Z', '+00:00'))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NoteDelete':
        return cls(data)

    def __str__(self) -> str:
        return (f"NoteDelete(type={self.type}, location_id={self.location_id}, "
                f"id={self.id}, body={self.body}, contact_id={self.contact_id}, "
                f"date_added={self.date_added})")

# Example usage:
example_data = {
    "type": "NoteDelete",
    "locationId": "ve9EPM428h8vShlRW1KT",
    "id": "otg8dTQqGLh3Q6iQI55w",
    "body": "Loram ipsum",
    "contactId": "CWBf1PR9LvvBkcYqiXlc",
    "dateAdded": "2021-11-26T12:41:02.193Z"
}

note_delete = NoteDelete.from_dict(example_data)
print(note_delete)