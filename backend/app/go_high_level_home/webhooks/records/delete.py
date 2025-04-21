from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Property(BaseModel):
    key: str
    valueString: str

class DeleteRecord(BaseModel):
    id: str
    locationId: str
    timestamp: datetime
    owners: List[str]
    followers: List[str]
    properties: List[Property]

# Example usage
example_payload = {
    "id": "679b8f9bde6a0c356a0311b3",
    "locationId": "eHy2cOSZxMQzQ6Yyvl8P",
    "timestamp": "2025-02-10T08:26:05.961Z",
    "owners": ["60d5ec49f72b2a001f5f9d91"],
    "followers": ["60d5ec49f72b2a001f5f9d93", "60d5ec49f72b2a001f5f9d94"],
    "properties": [
        {
            "key": "pet_name",
            "valueString": "buddy"
        }
    ]
}

delete_record = DeleteRecord(**example_payload)

# Additional Notes:
# 1. Ensure your webhook listener is set up to handle POST requests.
# 2. The payload format may change in future versions; check for updates regularly.
# 3. Handle potential exceptions when parsing the webhook payload.