from typing import Dict
from ...client import get_client


def create_segment_for_speaker(dubbing_id: str, speaker_id: str, start_time: float, end_time: float) -> Dict:
    """
    Create a segment for a speaker in a dubbing resource.

    Args:
        dubbing_id: The ID of the dubbing resource.
        speaker_id: The ID of the speaker.
        start_time: The start time of the segment.
        end_time: The end time of the segment.

    Returns:
        A dictionary containing the segment details.
    """
    client = get_client()
    
    return client.dubbing.create_segment_for_speaker(
        dubbing_id=dubbing_id,
        speaker_id=speaker_id,
        start_time=start_time,
        end_time=end_time,
    )
