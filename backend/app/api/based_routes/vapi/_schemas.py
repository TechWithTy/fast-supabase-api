from pydantic import BaseModel
from typing import Optional, Any, List

class AssistantOverrides(BaseModel):
    transcriber: Optional[dict[str, Any]] = None
    model: Optional[dict[str, Any]] = None
    voice: Optional[dict[str, Any]] = None
    clientMessages: Optional[list[str]] = None
    serverMessages: Optional[list[str]] = None

class Assistant(BaseModel):
    transcriber: dict[str, Any]
    model: dict[str, Any]
    voice: dict[str, Any]
    firstMessageMode: str
    recordingEnabled: bool
    hipaaEnabled: bool
    clientMessages: list[str]
    serverMessages: list[str]
    silenceTimeoutSeconds: int
    maxDurationSeconds: int
    backgroundSound: str
    backchannelingEnabled: bool
    backgroundDenoisingEnabled: bool

class CreateCallRequest(BaseModel):
    name: str
    assistantId: Optional[str] = None
    assistant: Optional[Assistant] = None
    assistantOverrides: Optional[AssistantOverrides] = None
    squadId: Optional[str] = None
    squad: Optional[dict[str, Any]] = None
    phoneNumberId: Optional[str] = None
    phoneNumber: Optional[dict[str, Any]] = None
    customerId: Optional[str] = None
    customer: Optional[dict[str, Any]] = None

class UpdateCallRequest(BaseModel):
    name: Optional[str] = None
    assistantId: Optional[str] = None
    assistant: Optional[Assistant] = None
    assistantOverrides: Optional[AssistantOverrides] = None
    squadId: Optional[str] = None
    squad: Optional[dict[str, Any]] = None
    phoneNumberId: Optional[str] = None
    phoneNumber: Optional[dict[str, Any]] = None
    customerId: Optional[str] = None
    customer: Optional[dict[str, Any]] = None
    # Add other updatable fields as needed
