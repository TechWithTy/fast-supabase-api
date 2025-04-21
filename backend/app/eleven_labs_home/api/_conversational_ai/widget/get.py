from typing import Dict
from ...client import get_client

def get_widget(agent_id: str) -> Dict:
    """
    Retrieves the widget for the specified agent.

    Args:
        agent_id (str): The ID of the agent to retrieve the widget for.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.conversational_ai.get_agent_widget(agent_id=agent_id)
