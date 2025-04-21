from typing import Optional
from ..client import get_client
from vapi import SquadMemberDto


def update_squad(squad_id: str, members: list) -> Optional[dict]:
    """
    Update a squad using the Vapi SDK.

    Args:
        squad_id (str): The ID of the squad to update.
        members (list): The list of squad members to update.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.squads.update(id=squad_id, members=[SquadMemberDto(**member) for member in members])
    except Exception as e:
        print(f"Error updating squad: {e}")
        return None
