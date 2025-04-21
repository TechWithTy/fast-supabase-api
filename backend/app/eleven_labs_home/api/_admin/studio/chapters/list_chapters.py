from typing import Dict, List
from ...client import get_client


def list_chapters(project_id: str) -> List[Dict]:
    """
    List all chapters in a studio project.

    Args:
        project_id: The ID of the project.

    Returns:
        A list of dictionaries containing chapter details.
    """
    client = get_client()
    
    return client.studio.chapters.list(
        project_id=project_id,
    )
