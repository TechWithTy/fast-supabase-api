from ..client import get_client


def create_audio_native_project(api_key: str, name: str, file_path: str):
    client = get_client()

    with open(file_path, "rb") as file:
        response = client.audio_native.create(name=name, file=file)

    return {
        "project_id": response.project_id,
        "converting": response.converting,
        "html_snippet": response.html_snippet,
    }


# Usage example:
# api_key = "your_api_key_here"
# name = "My Audio Project"
# file_path = "path/to/your/audio/file.mp3"
# result = create_audio_native_project(api_key, name, file_path)
# print(result)
