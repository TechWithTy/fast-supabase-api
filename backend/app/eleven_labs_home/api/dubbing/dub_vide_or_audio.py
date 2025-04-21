from ..client import get_client


def dub_video_or_audio(api_key: str, file_path: str, target_language: str):
    client = get_client()

    with open(file_path, "rb") as file:
        response = client.dubbing.dub(audio=file, target_language=target_language)

    return response.dubbing_id
