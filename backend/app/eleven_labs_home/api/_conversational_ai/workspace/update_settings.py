from typing import Dict
from ...client import get_client

def update_settings(settings: Dict) -> Dict:
    """
    Updates the workspace settings.

    Args:
        settings (Dict): The new settings to apply.

    Returns:
        Dict: The updated workspace settings.
    """
    client = get_client()
    return client.conversational_ai.update_settings(settings=settings)
