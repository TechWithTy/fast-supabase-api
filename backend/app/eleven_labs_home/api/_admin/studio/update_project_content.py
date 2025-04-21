from typing import Dict
from ...client import get_client


def update_project_content(project_id: str, content_file) -> Dict:
    """
    Update the content of a studio project.

    Args:
        project_id: The ID of the project to update.
        content_file: The file containing the new content.

    Returns:
        A dictionary containing the updated project details.
    """
    client = get_client()
    
    return client.studio.projects.update_content(
        project_id=project_id,
        content=content_file,
    )
