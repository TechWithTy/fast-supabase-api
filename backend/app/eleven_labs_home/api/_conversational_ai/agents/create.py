from typing import Dict, Any
from ...client import get_client

def create_agent(conversation_config: Dict[str, Any] = {}) -> Dict[str, Any]:
    client = get_client()
    response = client.conversational_ai.create_agent(
        conversation_config=conversation_config,
    )
    return response
