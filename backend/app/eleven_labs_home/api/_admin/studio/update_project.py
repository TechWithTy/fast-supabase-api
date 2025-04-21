from typing import Dict
from ...client import get_client


def update_project(project_id: str, name: str, default_title_voice_id: str, default_paragraph_voice_id: str) -> Dict:
    """
    Update the metadata of a studio project.

    Args:
        project_id: The ID of the project to update.
        name: The new name of the project.
        default_title_voice_id: The ID of the default voice for titles.
        default_paragraph_voice_id: The ID of the default voice for paragraphs.

    Returns:
        A dictionary containing the updated project metadata.
    """
    client = get_client()
    
    return client.studio.projects.update_metadata(
        project_id=project_id,
        name=name,
        default_title_voice_id=default_title_voice_id,
        default_paragraph_voice_id=default_paragraph_voice_id,
    )
