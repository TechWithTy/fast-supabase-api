from typing import Dict, List
from ...client import get_client


def list_studio_projects() -> List[Dict]:
    """
    List all studio projects.

    Returns:
        A list of dictionaries containing project details.
    """
    client = get_client()
    
    return client.studio.projects.list()