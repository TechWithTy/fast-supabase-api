from vapi import Vapi
from typing import Optional
from ..client import get_client


def delete_tool(tool_id: str) -> Optional[dict]:
    """
    Delete a tool using the Vapi SDK.

    Args:
        tool_id (str): The ID of the tool to delete.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.tools.delete(id=tool_id)
    except Exception as e:
        print(f"Error deleting tool: {e}")
        return None

client = get_client()
response = delete_tool("id")
