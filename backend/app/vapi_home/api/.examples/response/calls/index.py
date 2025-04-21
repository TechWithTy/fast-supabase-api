import datetime

example_create_call_response = {
    "id": "call-id-001",  # Unique identifier for the call
    "name": "Test Call",
    "assistantId": "assistant-123",
    "squadId": None,
    "phoneNumberId": "phone-number-123",
    "customerId": "customer-123",
    "status": "queued",  # Initial status of the call
    "endedReason": None,  # Not ended yet
    "type": "outboundPhoneCall",
    "phoneCallProvider": "twilio",
    "phoneCallTransport": "pstn",
    "createdAt": "2024-09-08T12:00:00Z",
    "updatedAt": "2024-09-08T12:01:00Z",
    "startedAt": None,  # Call hasn't started yet
    "endedAt": None,  # Call hasn't ended yet
    "cost": 0.0,  # Cost will be calculated after the call
    "messages": [
        {
            "content": "Hello!",
            "role": "assistant",  # Initial assistant message
        }
    ],
    "recordingUrl": None,  # Recording will be available after the call
    "stereoRecordingUrl": None,
    "transcript": None,  # Transcript will be generated after the call
    "artifact": {
        "videoRecordingEnabled": True,
        "recordingS3PathPrefix": "s3://recordings/call-id-001",
    },
    "analysis": {"summary": None, "structuredData": {}, "successEvaluation": None},
    "assistant": {
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2",
            "language": "bg",
            "smartFormat": False,
            "keywords": ["test"],
            "endpointing": 255,
        },
        "model": {
            "messages": [{"content": "Hello!", "role": "assistant"}],
            "tools": [
                {
                    "async": False,
                    "messages": [
                        {
                            "type": "request-start",
                            "content": "Tool started",
                            "role": "assistant",
                            "conditions": [
                                {"value": "start", "operator": "eq", "param": "trigger"}
                            ],
                        }
                    ],
                    "type": "dtmf",
                    "function": {
                        "name": "DTMF Tool",
                        "description": "Tool for DTMF detection",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": ["param1"],
                        },
                    },
                    "server": {
                        "timeoutSeconds": 20,
                        "url": "https://tool.server.url",
                        "secret": "secretKey",
                    },
                }
            ],
            "toolIds": ["tool-1"],
            "provider": "anyscale",
            "model": "model-1",
            "temperature": 1,
            "maxTokens": 525,
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
                "punctuationBoundaries": [".", ",", "!", "?"],
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
    },
}


example_get_call_response = {
    "id": "call-id-123",
    "orgId": "org-id-456",
    "type": "inboundPhoneCall",
    "phoneCallProvider": "twilio",
    "phoneCallTransport": "sip",
    "status": "ended",
    "endedReason": "assistant-error",
    "monitor": {
        "listenUrl": "https://example.com/listen",
        "controlUrl": "https://example.com/control",
    },
    "messages": [
        {
            "role": "user",
            "message": "Hello, how can I help?",
            "time": datetime.datetime.now().isoformat(),
            "secondsFromStart": 5,
            "endTime": datetime.datetime.now() + datetime.timedelta(seconds=1),
            "duration": 1,
        }
    ],
    "endedAt": datetime.datetime.now() + datetime.timedelta(seconds=10),
    "destination": {
        "type": "number",
        "numberE164CheckEnabled": True,
        "number": "+1234567890",
        "extension": "123",
        "message": "Transfer to support",
        "description": "Call transferred to support team",
    },
    "createdAt": "2023-09-07T12:00:00Z",
    "updatedAt": "2023-09-07T12:05:00Z",
    "startedAt": "2023-09-07T12:01:00Z",
    "endedAt": "2023-09-07T12:04:30Z",
    "cost": 5.0,
    "costBreakdown": {
        "transport": 1.5,
        "stt": 1.0,
        "llm": 0.5,
        "tts": 0.8,
        "vapi": 1.2,
        "total": 5.0,
        "llmPromptTokens": 100,
        "llmCompletionTokens": 80,
        "ttsCharacters": 500,
    },
    "transcript": "Transcript of the call goes here...",
    "recordingUrl": "https://example.com/recording.mp3",
    "stereoRecordingUrl": "https://example.com/stereo-recording.mp3",
    "artifact": {
        "videoRecordingEnabled": True,
        "recordingS3PathPrefix": "s3://recordings/call-id-123",
    },
    "analysis": {
        "summary": "The call ended abruptly due to an error.",
        "structuredData": {},
        "successEvaluation": "unsuccessful",
    },
    "assistantId": "assistant-id-789",
    "assistant": {
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2",
            "language": "en",
            "smartFormat": False,
            "keywords": ["support", "account"],
            "endpointing": 255,
        },
        "model": {
            "messages": [
                {
                    "role": "user",
                    "message": "Hello, how can I help?",
                    "time": datetime.datetime.now(),
                    "secondsFromStart": 5,
                    "endTime": datetime.datetime.now() + datetime.timedelta(seconds=1),
                    "duration": 1,
                }
            ],
            "tools": [],
            "toolIds": [],
            "provider": "anyscale",
            "model": "gpt-4",
            "temperature": 0.8,
            "knowledgeBase": {
                "provider": "canonical",
                "topK": 5,
                "fileIds": ["file-id-001"],
            },
            "maxTokens": 500,
            "emotionRecognitionEnabled": True,
            "numFastTurns": 2,
        },
        "voice": {
            "fillerInjectionEnabled": False,
            "provider": "azure",
            "voiceId": "andrew",
            "speed": 1.25,
            "chunkPlan": {
                "enabled": True,
                "minCharacters": 30,
                "punctuationBoundaries": [".", "?", "!"],
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
        "backgroundDenoisingEnabled": True,
    },
}


example_list_calls_response = {
    "calls": [
        {
            "id": "call-id-001",
            "orgId": "org-id-001",
            "type": "inboundPhoneCall",
            "monitor": {
                "listenUrl": "https://example.com/listen",
                "controlUrl": "https://example.com/control",
            },
            "phoneCallProvider": "twilio",
            "phoneCallTransport": "sip",
            "status": "ended",
            "endedReason": "assistant-error",
            "messages": [
                {
                    "role": "user",
                    "message": "Hello, how can I help?",
                    "time": datetime.datetime.now(),
                    "secondsFromStart": 5,
                    "endTime": datetime.datetime.now() + datetime.timedelta(seconds=1),
                    "duration": 1,
                }
            ],
            "createdAt": "2023-09-07T12:00:00Z",
            "updatedAt": "2023-09-07T12:05:00Z",
            "startedAt": "2023-09-07T12:01:00Z",
            "endedAt": "2023-09-07T12:04:30Z",
            "cost": 5.0,
            "costBreakdown": {
                "transport": 1.5,
                "stt": 1.0,
                "llm": 0.5,
                "tts": 0.8,
                "vapi": 1.2,
                "total": 5.0,
                "llmPromptTokens": 100,
                "llmCompletionTokens": 80,
                "ttsCharacters": 500,
            },
            "transcript": "Transcript of the call goes here...",
            "recordingUrl": "https://example.com/recording.mp3",
            "stereoRecordingUrl": "https://example.com/stereo-recording.mp3",
            "artifact": {
                "videoRecordingEnabled": True,
                "recordingS3PathPrefix": "s3://recordings/call-id-001",
            },
            "analysis": {
                "summary": "The call ended due to an error.",
                "structuredData": {},
                "successEvaluation": "unsuccessful",
            },
            "assistantId": "assistant-id-001",
        }
        # More calls...
    ],
    "totalCount": 20,  # Optional total count of calls
}

example_update_call_response = {
    "id": "call-id-123",
    "orgId": "org-id-456",
    "type": "outboundPhoneCall",
    "messages": [
        {"content": "Hello, how can I help you?", "role": "assistant"},
        {"content": "I need help with my account.", "role": "user"},
    ],
    "status": "ended",
    "endedReason": "assistant-ended-call",
    "createdAt": "2023-09-07T12:00:00Z",
    "updatedAt": "2023-09-07T12:05:00Z",
    "startedAt": "2023-09-07T12:01:00Z",
    "endedAt": "2023-09-07T12:04:30Z",
    "cost": 5.0,
    "transcript": "Transcript of the call goes here...",
    "recordingUrl": "https://example.com/recording.mp3",
    "assistantId": "assistant-id-001",
}
