from vapi import Vapi
from typing import Optional
from ..client import get_client

def get_tool(tool_id: str) -> Optional[dict]:
    """
    Get a tool using the Vapi SDK.

    Args:
        tool_id (str): The ID of the tool to retrieve.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.tools.get(id=tool_id)
    except Exception as e:
        print(f"Error getting tool: {e}")
        return None

# Example usage:
tool_id = "id"
tool = get_tool(tool_id)
