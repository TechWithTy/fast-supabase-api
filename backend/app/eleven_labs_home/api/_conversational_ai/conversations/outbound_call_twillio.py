from typing import Dict
from ...client import get_client

def twilio_outbound_call(agent_id: str, agent_phone_number_id: str, to_number: str) -> Dict:
    """
    Initiates an outbound call using Twilio.

    Args:
        agent_id (str): The ID of the agent.
        agent_phone_number_id (str): The ID of the agent's phone number.
        to_number (str): The number to call.

    Returns:
        Dict: The response from the API.
    """
    client = get_client()
    return client.conversational_ai.twilio_outbound_call(
        agent_id=agent_id,
        agent_phone_number_id=agent_phone_number_id,
        to_number=to_number,
    )
