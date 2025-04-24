"""
ASGI entrypoint for FastAPI application.

Exposes the ASGI callable as a module-level variable named `app`.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file (optional, but common)
env_path = Path(__file__).resolve().parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# Import your FastAPI app
from app.main import app  # Adjust if your FastAPI app is elsewhere

# Optionally, alias for some ASGI servers
application = app
