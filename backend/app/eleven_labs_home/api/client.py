# backend/apps/eleven_labs/api/client.py
from elevenlabs import Client
import os

ELEVENLABS_API_KEY = api_key=os.getenv("ELEVENLABS_API_KEY")

_client = None

def initialize_client(api_key: str) -> None:
    global _client
    _client = Client(api_key=api_key)

def get_client() -> Client:
    global _client
    if _client is None:
        if ELEVENLABS_API_KEY is None:
            raise ValueError("Client not initialized. Call initialize_client first or provide an api_key.")
        initialize_client(ELEVENLABS_API_KEY)
    return _client