from typing import Optional
from ..client import get_client
from vapi import CreateDtmfToolDto


def create_tool(payload: dict) -> Optional[dict]:
    """
    Create a tool using the Vapi SDK.

    Args:
        payload (dict): The tool configuration.

    Returns:
        Optional[dict]: The response from the API if successful, None otherwise.
    """
    try:
        client = get_client()
        return client.tools.create(request=CreateDtmfToolDto(**payload))
    except Exception as e:
        print(f"Error creating tool: {e}")
        return None
