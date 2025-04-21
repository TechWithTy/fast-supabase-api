from typing import Dict
from ...client import get_client

def delete_agent(agent_id: str) -> Dict:
    client = get_client()
    response = client.conversational_ai.delete_agent(agent_id=agent_id)
    return response
