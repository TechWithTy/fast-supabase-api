from typing import Dict, List
from ...client import get_client


def list_chapters_snapshot(project_id: str, chapter_id: str) -> List[Dict]:
    """
    List all snapshots for a specific chapter.

    Args:
        project_id: The ID of the project.
        chapter_id: The ID of the chapter.

    Returns:
        A list of dictionaries containing snapshot details.
    """
    client = get_client()
    
    return client.studio.chapters.list_snapshots(
        project_id=project_id,
        chapter_id=chapter_id,
    )
