from typing import Dict
from ...client import get_client


def convert_project(project_id: str) -> Dict:
    """
    Convert a studio project.

    Args:
        project_id: The ID of the project to convert.

    Returns:
        A dictionary containing the conversion details.
    """
    client = get_client()
    
    return client.studio.projects.convert(
        project_id=project_id,
    )
