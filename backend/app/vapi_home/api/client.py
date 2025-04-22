from vapi import Vapi

from app.core.config import settings

VAPI_PRIVATE_TOKEN = settings.VAPI_PRIVATE_TOKEN

_client = None

def initialize_client(token: str) -> None:
    global _client
    _client = Vapi(token=token)

def get_client() -> Vapi:
    global _client
    if _client is None:
        if VAPI_PRIVATE_TOKEN is None:
            raise ValueError("Client not initialized. VAPI_PRIVATE_TOKEN is missing from settings.")
        initialize_client(VAPI_PRIVATE_TOKEN)
    return _client