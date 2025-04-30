from vapi import Vapi
from typing import Optional
from ..client import get_client


def delete_squad(squad_id: str) -> Optional[dict]:
    """
    Delete a squad using the Vapi SDK.

    Args:
        squad_id (str): The ID of the squad to delete.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.squads.delete(id=squad_id)
    except Exception as e:
        print(f"Error deleting squad: {e}")
        return None

# # Example usage:
# client = Vapi(
#     token="YOUR_TOKEN",
# )
# delete_squad("id")
