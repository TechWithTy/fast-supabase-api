from vapi import Vapi
from typing import Optional
from ..client import get_client


def update_tool(tool_id: str, update_data: dict) -> Optional[dict]:
    """
    Update a tool using the Vapi SDK.

    Args:
        tool_id (str): The ID of the tool to update.
        update_data (dict): The update configuration.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.tools.update(id=tool_id, **update_data)
    except Exception as e:
        print(f"Error updating tool: {e}")
        return None

# Example usage:
client = Vapi(
    token="YOUR_TOKEN",
)
update_tool("id", {})
