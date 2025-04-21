from typing import Dict, Any
from ...client import get_client

def get_agents() -> Dict[str, Any]:
    client = get_client()
    return client.conversational_ai.get_agents()
