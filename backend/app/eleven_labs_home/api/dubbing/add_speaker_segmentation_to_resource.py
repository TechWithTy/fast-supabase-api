from ..client import get_client


def add_speaker_segment(
    api_key: str, dubbing_id: str, speaker_id: str, start_time: float, end_time: float
):
    client = get_client()

    response = client.dubbing.add_speaker_segment(
        dubbing_id=dubbing_id,
        speaker_id=speaker_id,
        start_time=start_time,
        end_time=end_time,
    )

    return response


# Usage example:
# api_key = "your_api_key_here"
# result = add_speaker_segment(api_key, "dubbing_id", "speaker_id", 1.1, 1.1)
# print(result)
