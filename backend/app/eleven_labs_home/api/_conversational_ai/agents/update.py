from typing import Dict
from ...client import get_client

def update_agent(agent_id: str) -> Dict:
    client = get_client()
    response = client.conversational_ai.update_agent(
        agent_id=agent_id,
    )
    return response
