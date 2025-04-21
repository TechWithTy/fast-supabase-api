import os
from dotenv import load_dotenv
from typing import Optional

def load_env(dotenv_path: Optional[str] = None) -> None:
    """
    Utility function to load environment variables from a .env file.
    If no path is provided, defaults to project root .env.
    """
    if dotenv_path is None:
        dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.env'))
    load_dotenv(dotenv_path=dotenv_path, override=True)
