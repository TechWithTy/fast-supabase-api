from vapi import Vapi
from typing import Optional
from ..client import get_client


def get_squad(squad_id: str) -> Optional[dict]:
    """
    Get a squad using the Vapi SDK.

    Args:
        squad_id (str): The ID of the squad to retrieve.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.squads.get(id=squad_id)
    except Exception as e:
        print(f"Error getting squad: {e}")
        return None
