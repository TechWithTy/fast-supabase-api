from typing import Dict
from ...client import get_client

def get_agent_link(agent_id: str) -> Dict:
    client = get_client()
    response = client.conversational_ai.get_agent_link(agent_id=agent_id)
    return response
