import os

from dotenv import load_dotenv


def load_env(dotenv_path: str | None = None, required_vars: list[str] | None = None) -> None:
    """
    Loads environment variables from the .env file in project root (local/dev) and verifies
    that required variables are present (for cloud/hosted envs like Hetzner, Coolify, Railway, Vercel, etc).
    Prints a warning if any required variables are missing.

    Usage:
    - Local/Dev: Simply call `load_env()` to load .env from project root.
    - Cloud/Hosted: Call `load_env(required_vars=["VARIABLE_1", "VARIABLE_2"])` to load .env and check for required variables.
    """
    if dotenv_path is None:
        # Use the absolute path to the .env in the project root
        dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../.env'))
    load_dotenv(dotenv_path=dotenv_path, override=True)

    # Check for required variables in os.environ (for hosted/cloud environments)
    if required_vars:
        missing = [var for var in required_vars if not os.environ.get(var)]
        if missing:
            print(f"[env_loader] Warning: Missing env variables: {missing}. Check your deployment provider's env config.")
