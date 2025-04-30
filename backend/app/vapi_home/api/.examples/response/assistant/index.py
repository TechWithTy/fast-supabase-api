example_updated_assistant_response = {
    'id': 'assistant-id-123',
    'name': 'Updated Assistant Name',
    'status': 'active',
    'createdAt': '2023-01-01T12:00:00Z',
    'updatedAt': '2023-09-08T10:00:00Z',
    'transcriber': {
        'provider': 'deepgram',
        'model': 'nova-2',
        'language': 'en',
        'smartFormat': True,
        'keywords': ['support', 'account'],
        'endpointing': 250
    },
    'model': {
        'provider': 'openai',
        'model': 'gpt-4',
        'temperature': 0.8,  # Updated field
        'maxTokens': 1024,
        'emotionRecognitionEnabled': True,
        'numFastTurns': 2
    },
    'voice': {
        'provider': 'azure',
        'voiceId': 'andrew',
        'speed': 1.25,
        'fillerInjectionEnabled': False
    },
    'firstMessageMode': 'assistant-speaks-first',
    'recordingEnabled': True,
    'hipaaEnabled': False,
    'backgroundSound': 'office',
    'backchannelingEnabled': False,
    'silenceTimeoutSeconds': 30,
    'maxDurationSeconds': 3600
}
example_get_response_data = {
    'id': 'assistant-id-123',
    'name': 'Customer Support Assistant',
    'status': 'active',
    'createdAt': '2023-01-01T12:00:00Z',
    'updatedAt': '2023-09-01T15:00:00Z',
    'transcriber': {
        'provider': 'deepgram',
        'model': 'nova-2',
        'language': 'en',
        'smartFormat': True,
        'keywords': ['support', 'account'],
        'endpointing': 250
    },
    'model': {
        'provider': 'openai',
        'model': 'gpt-4',
        'temperature': 0.8,
        'maxTokens': 1024,
        'emotionRecognitionEnabled': True,
        'numFastTurns': 2
    },
    'voice': {
        'provider': 'azure',
        'voiceId': 'andrew',
        'speed': 1.25,
        'fillerInjectionEnabled': False
    },
    'firstMessageMode': 'assistant-speaks-first',
    'recordingEnabled': True,
    'hipaaEnabled': False,
    'backgroundSound': 'office',
    'backchannelingEnabled': False,
    'silenceTimeoutSeconds': 30,
    'maxDurationSeconds': 3600,
    'assistantOverrides': {
        'model': {
            'temperature': 0.7,
            'maxTokens': 512
        }
    }
}



example_list_response = {
    "assistants": [
        {
            "id": "assistant-id-001",
            "name": "Customer Support Assistant",
            "status": "active",
            "createdAt": "2023-01-01T12:00:00Z",
            "updatedAt": "2023-06-01T15:00:00Z",
            "transcriber": {
                "provider": "deepgram",
                "model": "nova-2",
                "language": "en",
                "smartFormat": True,
                "keywords": ["support", "account"],
                "endpointing": 250
            },
            "model": {
                "provider": "openai",
                "model": "gpt-4",
                "temperature": 0.8,
                "maxTokens": 1024,
                "emotionRecognitionEnabled": True,
                "numFastTurns": 2
            },
            "voice": {
                "provider": "azure",
                "voiceId": "andrew",
                "speed": 1.25,
                "fillerInjectionEnabled": False
            },
            "firstMessageMode": "assistant-speaks-first",
            "recordingEnabled": True,
            "hipaaEnabled": False,
            "backgroundSound": "office",
            "backchannelingEnabled": False,
            "silenceTimeoutSeconds": 30,
            "maxDurationSeconds": 3600
        },
        {
            "id": "assistant-id-002",
            "name": "Technical Support Bot",
            "status": "inactive",
            "createdAt": "2023-02-15T12:00:00Z",
            "updatedAt": "2023-07-01T15:00:00Z",
            "transcriber": {
                "provider": "azure",
                "model": "neural-en",
                "language": "en",
                "smartFormat": False,
                "keywords": ["error", "bug"],
                "endpointing": 200
            },
            "model": {
                "provider": "azure",
                "model": "gpt-3",
                "temperature": 0.7,
                "maxTokens": 800,
                "emotionRecognitionEnabled": False,
                "numFastTurns": 1
            },
            "voice": {
                "provider": "google",
                "voiceId": "samantha",
                "speed": 1.0,
                "fillerInjectionEnabled": True
            },
            "firstMessageMode": "assistant-waits-for-user",
            "recordingEnabled": False,
            "hipaaEnabled": True,
            "backgroundSound": "off",
            "backchannelingEnabled": True,
            "silenceTimeoutSeconds": 60,
            "maxDurationSeconds": 1800
        }
        # More assistant objects...
    ],
    "totalCount": 2
}