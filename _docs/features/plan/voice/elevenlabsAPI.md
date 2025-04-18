Cloning a Voice Programmatically with the ElevenLabs API
You can create (clone) a new custom voice via the ElevenLabs API using a simple HTTP request. This is useful for automating voice onboarding or integrating voice creation into your product flows.

1. Prerequisites
   An active ElevenLabs API subscription.
   Your ElevenLabs API key.
2. API Endpoint for Voice Cloning
   Endpoint:
   POST [https://api.elevenlabs.io/v1/voices/add](https://api.elevenlabs.io/v1/voices/add`)
   Headers:
   xi-api-key: <YOUR_API_KEY>
   Content-Type: multipart/form-data
   Required Parameters:
   name: Name for the new voice.
   files: One or more audio sample files (WAV or MP3, ideally clean speech).
   description (optional): Description for the voice.
   Example curl Request
   bash
   CopyInsert
   curl -X POST '[https://api.elevenlabs.io/v1/voices/add'](https://api.elevenlabs.io/v1/voices/add') \
    -H 'xi-api-key: YOUR_API_KEY' \
    -F 'name=MyCustomVoice' \
    -F 'files=@/path/to/voice_sample1.wav' \
    -F 'files=@/path/to/voice_sample2.wav' \
    -F 'description=Cloned from user sample'
   Example Python (requests)
   python
   CopyInsert
   import requests

url = "[https://api.elevenlabs.io/v1/voices/add"](https://api.elevenlabs.io/v1/voices/add")
headers = {"xi-api-key": "YOUR_API_KEY"}
files = [
("files", open("voice_sample1.wav", "rb")),
("files", open("voice_sample2.wav", "rb"))
]
data = {"name": "MyCustomVoice", "description": "Cloned from user sample"}

response = requests.post(url, headers=headers, files=files, data=data)
print(response.json()) 3. Response
The API will return a JSON object with the new voice_id and details about the created voice.

🔗 Integration with Vapi
Once the voice is created, you can use the returned voice_id to reference your cloned voice in Vapi.
In your backend (such as in backend/app/vapi_home/api/), you can automate this process as part of your onboarding or admin flows.
📝 Best Practices
Use high-quality, clean audio samples for best cloning results.
You can upload multiple samples for a more robust voice model.
Store the returned voice_id in your database for later use in TTS or Vapi flows.
