from ..client import get_client


def save_voice_preview(
    api_key: str, voice_name: str, voice_description: str, generated_voice_id: str
):
    client = get_client()

    response = client.voices.create_from_preview(
        name=voice_name,
        description=voice_description,
        generated_voice_id=generated_voice_id,
    )

    return response


# Usage example:
# api_key = "your_api_key_here"
# result = save_voice_preview(
#     api_key,
#     "Sassy squeaky mouse",
#     "A sassy squeaky mouse",
#     "37HceQefKmEi3bGovXjL"
# )
