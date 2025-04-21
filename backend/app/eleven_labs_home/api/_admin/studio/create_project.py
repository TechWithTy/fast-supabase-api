from typing import Dict
from ...client import get_client


def create_studio_project(name: str, default_title_voice_id: str, default_paragraph_voice_id: str, default_model_id: str) -> Dict:
    """
    Create a new studio project.

    Args:
        name: The name of the project.
        default_title_voice_id: The ID of the default voice for titles.
        default_paragraph_voice_id: The ID of the default voice for paragraphs.
        default_model_id: The ID of the default model.

    Returns:
        A dictionary containing the project details.
    """
    client = get_client()
    
    return client.studio.projects.add(
        name=name,
        default_title_voice_id=default_title_voice_id,
        default_paragraph_voice_id=default_paragraph_voice_id,
        default_model_id=default_model_id,
    )
