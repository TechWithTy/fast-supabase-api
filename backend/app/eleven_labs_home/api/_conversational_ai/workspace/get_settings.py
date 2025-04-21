from typing import Dict
from ...client import get_client

def get_settings() -> Dict:
    """
    Retrieves the workspace settings.

    Returns:
        Dict: The workspace settings.
    """
    client = get_client()
    return client.conversational_ai.get_settings()
