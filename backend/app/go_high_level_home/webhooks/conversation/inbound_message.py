from typing import List, Optional
from datetime import datetime
from enum import Enum

class MessageType(Enum):
    CALL = "CALL"
    VOICEMAIL = "VOICEMAIL"
    SMS = "SMS"
    GMB = "GMB"
    FB = "FB"
    IG = "IG"
    EMAIL = "Email"
    LIVE_CHAT = "LIVE_CHAT"

class Direction(Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

class Status(Enum):
    DELIVERED = "delivered"
    COMPLETED = "completed"
    VOICEMAIL = "voicemail"

class InboundMessage:
    """
    Represents an inbound message from a contact to the user.
    Called whenever a contact sends a message to the user.
    """

    def __init__(
        self,
        type: str,
        location_id: str,
        attachments: List[str],
        body: str,
        contact_id: str,
        content_type: str,
        conversation_id: str,
        date_added: datetime,
        direction: Direction,
        message_type: MessageType,
        status: Status,
        message_id: str,
        user_id: Optional[str] = None,
        conversation_provider_id: Optional[str] = None,
        call_duration: Optional[int] = None,
        call_status: Optional[str] = None,
        email_message_id: Optional[str] = None,
        thread_id: Optional[str] = None,
        provider: Optional[str] = None,
        to: Optional[List[str]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        from_email: Optional[str] = None,
        subject: Optional[str] = None
    ):
        self.type = type
        self.location_id = location_id
        self.attachments = attachments
        self.body = body
        self.contact_id = contact_id
        self.content_type = content_type
        self.conversation_id = conversation_id
        self.date_added = date_added
        self.direction = direction
        self.message_type = message_type
        self.status = status
        self.message_id = message_id
        self.user_id = user_id
        self.conversation_provider_id = conversation_provider_id
        self.call_duration = call_duration
        self.call_status = call_status
        self.email_message_id = email_message_id
        self.thread_id = thread_id
        self.provider = provider
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.from_email = from_email
        self.subject = subject

    @classmethod
    def from_dict(cls, data: dict) -> 'InboundMessage':
        return cls(
            type=data['type'],
            location_id=data['locationId'],
            attachments=data.get('attachments', []),
            body=data.get('body', ''),
            contact_id=data['contactId'],
            content_type=data.get('contentType', ''),
            conversation_id=data['conversationId'],
            date_added=datetime.fromisoformat(data['dateAdded'].rstrip('Z')),
            direction=Direction(data['direction']),
            message_type=MessageType(data['messageType']),
            status=Status(data['status']),
            message_id=data['messageId'],
            user_id=data.get('userId'),
            conversation_provider_id=data.get('conversationProviderId'),
            call_duration=data.get('callDuration'),
            call_status=data.get('callStatus'),
            email_message_id=data.get('emailMessageId'),
            thread_id=data.get('threadId'),
            provider=data.get('provider'),
            to=data.get('to'),
            cc=data.get('cc'),
            bcc=data.get('bcc'),
            from_email=data.get('from'),
            subject=data.get('subject')
        )

# Example usage:
sms_example = {
    "type": "InboundMessage",
    "locationId": "l1C08ntBrFjLS0elLIYU",
    "attachments": [],
    "body": "This is a test message",
    "contactId": "cI08i1Bls3iTB9bKgFJh",
    "contentType": "text/plain",
    "conversationId": "fcanlLgpbQgQhderivVs",
    "dateAdded": "2021-04-21T11:31:45.750Z",
    "direction": "inbound",
    "messageType": "SMS",
    "status": "delivered",
    "messageId": "someMessageId",
    "conversationProviderId": "cI08i1Bls3iTB9bKgF01"
}

sms_message = InboundMessage.from_dict(sms_example)

# For listening to inbound messages, use the following webhook URL:
# https://services.leadconnectorhq.com/conversations/providers/twilio/inbound_message

# Old messaging webhook URL (for reference):
# https://services.leadconnectorhq.com/appengine/twilio/incoming_message