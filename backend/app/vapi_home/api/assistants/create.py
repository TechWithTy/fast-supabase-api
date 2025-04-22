from ..client import get_client
from typing import Any


def create_assistant(payload: dict[str, Any]) -> dict[str, Any] | None:
    """
    Create a Vapi assistant using the Vapi SDK client.

    Args:
        payload (dict): The assistant configuration as per Vapi docs.

    Returns:
        dict or None: The created assistant response or None if error.
    """
    try:
        client = get_client()
        # Defensive: check client has 'assistants' and 'create'
        if not hasattr(client, 'assistants') or not hasattr(client.assistants, 'create'):
            raise AttributeError("Vapi client does not support assistants.create(). Check SDK version.")
        return client.assistants.create(**payload)
    except Exception as e:
        print(f"Error creating assistant: {e}")
        return None


example_payload = {
    "transcriber": {
        "provider": "deepgram",
        "model": "nova-2",
        "language": "en",
        "smartFormat": False,
        "keywords": ["example", "test"],
        "endpointing": 255,
    },
    "model": {
        "messages": [
            {"content": "Hello, how may I assist you today?", "role": "assistant"}
        ],
        "tools": [
            {
                "async": False,
                "messages": [
                    {
                        "type": "request-start",
                        "content": "Starting tool...",
                        "role": "assistant",
                        "conditions": [
                            {"value": "start", "operator": "eq", "param": "status"}
                        ],
                    }
                ],
                "type": "dtmf",
                "function": {
                    "name": "ProcessPayment",
                    "description": "This function processes payments.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": ["amount"],
                    },
                },
                "server": {
                    "timeoutSeconds": 20,
                    "url": "https://example.com/process-payment",
                    "secret": "my-secret",
                },
            }
        ],
        "toolIds": ["tool-123"],
        "provider": "anyscale",
        "model": "gpt-3",
        "temperature": 1,
        "knowledgeBase": {
            "provider": "canonical",
            "topK": 5,
            "fileIds": ["file-123"],
        },
        "maxTokens": 500,
        "emotionRecognitionEnabled": True,
        "numFastTurns": 1,
    },
    "voice": {
        "fillerInjectionEnabled": False,
        "provider": "azure",
        "voiceId": "andrew",
        "speed": 1.25,
        "chunkPlan": {
            "enabled": True,
            "minCharacters": 30,
            "punctuationBoundaries": [".", "!", "?"],
            "formatPlan": {"enabled": True, "numberToDigitsCutoff": 2025},
        },
    },
    "firstMessageMode": "assistant-speaks-first",
    "recordingEnabled": True,
    "hipaaEnabled": False,
    "clientMessages": ["conversation-update", "function-call"],
    "serverMessages": ["conversation-update", "end-of-call-report"],
    "silenceTimeoutSeconds": 30,
    "maxDurationSeconds": 600,
    "backgroundSound": "office",
    "backchannelingEnabled": False,
    "backgroundDenoisingEnabled": False,
    "modelOutputInMessagesEnabled": False,
    "transportConfigurations": [
        {
            "provider": "twilio",
            "timeout": 60,
            "record": False,
            "recordingChannels": "mono",
        }
    ],
    "name": "Test Assistant",
    "firstMessage": "Hello! How can I assist you today?",
    "voicemailDetection": {
        "provider": "twilio",
        "voicemailDetectionTypes": ["machine_end_beep"],
        "enabled": True,
        "machineDetectionTimeout": 31,
        "machineDetectionSpeechThreshold": 3500,
        "machineDetectionSpeechEndThreshold": 2750,
        "machineDetectionSilenceTimeout": 6000,
    },
    "voicemailMessage": "Please leave a message after the beep.",
    "endCallMessage": "Thank you for calling, goodbye!",
    "endCallPhrases": ["goodbye", "bye"],
    "metadata": {},
    "serverUrl": "https://example.com/server-url",
    "serverUrlSecret": "my-server-secret",
    "analysisPlan": {
        "summaryPrompt": "Summarize the conversation.",
        "summaryRequestTimeoutSeconds": 10,
        "structuredDataRequestTimeoutSeconds": 10,
        "successEvaluationPrompt": "Was this successful?",
        "successEvaluationRubric": "NumericScale",
        "successEvaluationRequestTimeoutSeconds": 10,
        "structuredDataPrompt": "Provide structured data.",
        "structuredDataSchema": {
            "type": "string",
            "items": {},
            "properties": {},
            "description": "Schema description",
            "required": ["requiredField"],
        },
    },
    "artifactPlan": {
        "videoRecordingEnabled": True,
        "recordingS3PathPrefix": "s3://my-recordings/",
    },
    "messagePlan": {
        "idleMessages": ["Please hold."],
        "idleMessageMaxSpokenCount": 5,
        "idleTimeoutSeconds": 20,
    },
    "startSpeakingPlan": {
        "waitSeconds": 0.4,
        "smartEndpointingEnabled": False,
        "transcriptionEndpointingPlan": {
            "onPunctuationSeconds": 0.1,
            "onNoPunctuationSeconds": 1.5,
            "onNumberSeconds": 0.5,
        },
    },
    "stopSpeakingPlan": {"numWords": 0, "voiceSeconds": 0.2, "backoffSeconds": 1},
    "credentialIds": ["credential-123"],
}

# Example usage:
# response = create_assistant(example_payload)
# print(response)
