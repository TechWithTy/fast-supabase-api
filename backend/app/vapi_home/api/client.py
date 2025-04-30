from vapi import Vapi
import os

VAPI_PRIVATE_TOKEN = os.getenv("VAPI_PRIVATE_TOKEN")

_client = None

def initialize_client(token: str) -> None:
    global _client
    _client = Vapi(token=token)

def get_client() -> Vapi:
    global _client
    if _client is None:
        if VAPI_PRIVATE_TOKEN is None:
            raise ValueError("Client not initialized. Call initialize_client first or provide a token.")
        initialize_client(VAPI_PRIVATE_TOKEN)
    return _client