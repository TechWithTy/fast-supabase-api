

# Example usage
squad_id = "squad-id-123"  # The ID of the squad to update

example_update_squad_data = {
    "name": "New Squad Name",
    "members": [
        {
            "assistantId": "assistant-id-001",
            "assistant": {
                "transcriber": {
                    "provider": "deepgram",
                    "model": "nova-2",
                    "language": "en"
                },
                "model": {
                    "messages": [{"content": "Welcome to the call.", "role": "assistant"}],
                    "provider": "anyscale",
                    "temperature": 0.7
                },
                "voice": {
                    "provider": "azure",
                    "voiceId": "andrew",
                    "speed": 1.25
                }
            },
            "assistantOverrides": {
                "voice": {
                    "speed": 1.1
                }
            }
        }
    ],
    "membersOverrides": {
        "assistant": {
            "transcriber": {"provider": "deepgram", "model": "nova-2"}
        }
    }
}

# Example usage
example_create_squad_data = {
    "name": "My Squad",
    "members": [
        {
            "assistantId": "assistant-123",
            "assistant": {
                "transcriber": {
                    "provider": "deepgram",
                    "model": "nova-2",
                    "language": "en",
                    "smartFormat": False,
                    "keywords": ["support", "help"],
                    "endpointing": 255
                },
                "model": {
                    "messages": [
                        {"content": "Hello, how can I assist you?", "role": "assistant"}
                    ],
                    "tools": [
                        {
                            "async": False,
                            "messages": [
                                {
                                    "type": "tool-message-start",
                                    "content": "Processing your request, please wait...",
                                    "role": "assistant"
                                }
                            ],
                            "type": "dtmf",
                            "function": {
                                "name": "DTMF Tool",
                                "description": "Tool for DTMF detection",
                                "parameters": {
                                    "type": "object",
                                    "properties": {},
                                    "required": ["param1"]
                                }
                            },
                            "server": {
                                "timeoutSeconds": 20,
                                "url": "https://my-tool-url.com",
                                "secret": "mySecretKey"
                            }
                        }
                    ],
                    "toolIds": ["tool-1"],
                    "provider": "anyscale",
                    "model": "gpt-4",
                    "temperature": 0.7,
                    "maxTokens": 1000,
                    "emotionRecognitionEnabled": True,
                    "numFastTurns": 1
                },
                "voice": {
                    "provider": "azure",
                    "voiceId": "en-US-GuyNeural",
                    "speed": 1.2,
                    "chunkPlan": {
                        "enabled": True,
                        "minCharacters": 30,
                        "punctuationBoundaries": [".", ",", "?", "!", ";"],
                        "formatPlan": {"enabled": True, "numberToDigitsCutoff": 2025}
                    }
                },
                "firstMessageMode": "assistant-speaks-first",
                "recordingEnabled": True,
                "hipaaEnabled": False,
                "clientMessages": ["conversation-update", "function-call", "transcript"],
                "serverMessages": ["conversation-update", "end-of-call-report"],
                "silenceTimeoutSeconds": 30,
                "maxDurationSeconds": 600,
                "backgroundSound": "office",
                "backchannelingEnabled": False,
                "backgroundDenoisingEnabled": True,
                "modelOutputInMessagesEnabled": False,
                "transportConfigurations": [
                    {
                        "provider": "twilio",
                        "timeout": 60,
                        "record": False,
                        "recordingChannels": "mono"
                    }
                ],
                "voicemailDetection": {
                    "provider": "twilio",
                    "voicemailDetectionTypes": ["machine_end_beep", "machine_end_silence"],
                    "enabled": True,
                    "machineDetectionTimeout": 30,
                    "machineDetectionSpeechThreshold": 3000,
                    "machineDetectionSpeechEndThreshold": 2500,
                    "machineDetectionSilenceTimeout": 5000
                },
                "voicemailMessage": "You have reached our voicemail, please leave a message after the beep.",
                "endCallMessage": "Thank you for calling. Goodbye!",
                "endCallPhrases": ["Goodbye", "Take care"],
                "serverUrl": "https://my-server-url.com",
                "serverUrlSecret": "serverSecret",
                "analysisPlan": {
                    "summaryPrompt": "Summarize the call in a few sentences.",
                    "successEvaluationPrompt": "Did the call meet the customer's needs?",
                    "successEvaluationRubric": "NumericScale",
                    "summaryRequestTimeoutSeconds": 10,
                    "structuredDataRequestTimeoutSeconds": 10,
                    "successEvaluationRequestTimeoutSeconds": 10,
                    "structuredDataPrompt": "Provide structured data from the call.",
                    "structuredDataSchema": {
                        "type": "object",
                        "properties": {},
                        "required": ["field1"]
                    }
                },
                "artifactPlan": {
                    "videoRecordingEnabled": True,
                    "recordingS3PathPrefix": "s3://my-bucket/recordings/"
                },
                "messagePlan": {
                    "idleMessages": ["Are you still there?"],
                    "idleMessageMaxSpokenCount": 3,
                    "idleTimeoutSeconds": 20
                },
                "startSpeakingPlan": {
                    "waitSeconds": 1,
                    "smartEndpointingEnabled": True,
                    "transcriptionEndpointingPlan": {
                        "onPunctuationSeconds": 0.1,
                        "onNoPunctuationSeconds": 1.5,
                        "onNumberSeconds": 0.5
                    }
                },
                "stopSpeakingPlan": {"numWords": 50, "voiceSeconds": 1, "backoffSeconds": 1},
                "credentialIds": ["credential-1"]
            }
        }
    ],
    "membersOverrides": {
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2",
            "language": "bg",
            "smartFormat": True,
            "keywords": ["override"],
            "endpointing": 300
        }
    }
}