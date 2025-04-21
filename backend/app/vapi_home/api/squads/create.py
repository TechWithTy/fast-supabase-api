from vapi import SquadMemberDto
from typing import Optional
from ..client import get_client

def create_squad(payload: dict) -> Optional[dict]:
    """
    Create a squad using the Vapi SDK.

    Args:
        payload (dict): The squad configuration.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.squads.create(**payload)
    except Exception as e:
        print(f"Error creating squad: {e}")
        return None

# # Example usage:
# payload = {
#     "members": [SquadMemberDto()],
# }
# response = create_squad(payload)
