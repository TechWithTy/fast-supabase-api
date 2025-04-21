from typing import Dict, Union

class ConversationUnreadUpdate:
    """Called whenever a conversation's unread status is updated"""

    def __init__(self, data: Dict[str, Union[str, int, bool]]):
        self.type: str = data["type"]
        self.location_id: str = data["locationId"]
        self.id: str = data["id"]
        self.contact_id: str = data["contactId"]
        self.unread_count: int = data["unreadCount"]
        self.inbox: bool = data["inbox"]
        self.starred: bool = data["starred"]
        self.deleted: bool = data["deleted"]

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int, bool]]) -> 'ConversationUnreadUpdate':
        return cls(data)

# Example usage
example_data = {
    "type": "ConversationUnreadUpdate",
    "locationId": "ADVlSQnPsdq3hinusd6C3",
    "id": "MzKIpg0rEIH2ZUGKf6BS",
    "contactId": "zsYhPBOUsEHtrK508Wm9",
    "deleted": False,
    "inbox": False,
    "starred": True,
    "unreadCount": 0
}

conversation_unread_update = ConversationUnreadUpdate.from_dict(example_data)