from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class Attachment(BaseModel):
    url: str

class OutboundMessage(BaseModel):
    type: str = "OutboundMessage"
    location_id: str
    attachments: List[Attachment] = []
    body: Optional[str] = None
    contact_id: str
    content_type: Optional[str] = None
    conversation_id: str
    date_added: datetime
    direction: str
    message_type: str
    status: Optional[str] = None
    message_id: str
    user_id: Optional[str] = None
    source: Optional[str] = None
    conversation_provider_id: Optional[str] = None
    call_duration: Optional[int] = None
    call_status: Optional[str] = None
    email_message_id: Optional[str] = None
    thread_id: Optional[str] = None
    provider: Optional[str] = None
    to: Optional[List[str]] = None
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
    from_email: Optional[str] = Field(None, alias="from")
    subject: Optional[str] = None

    class Config:
        allow_population_by_field_name = True

def handle_outbound_message(data: dict) -> OutboundMessage:
    """
    Process the incoming webhook data for an outbound message.

    This function is called whenever a user sends a message to a contact.
    Supported channels include: Call, Voicemail, SMS, GMB, FB, IG, Email, Live Chat.

    Args:
        data (dict): The webhook payload containing the outbound message data.

    Returns:
        OutboundMessage: A processed OutboundMessage object.
    """
    return OutboundMessage(**data)

# Example usage:
if __name__ == "__main__":
    # Example SMS message
    sms_data = {
        "type": "OutboundMessage",
        "locationId": "l1C08ntBrFjLS0elLIYU",
        "attachments": [],
        "body": "This is a test message",
        "contactId": "cI08i1Bls3iTB9bKgFJh",
        "contentType": "text/plain",
        "conversationId": "fcanlLgpbQgQhderivVs",
        "dateAdded": "2021-04-21T11:31:45.750Z",
        "direction": "outbound",
        "messageType": "SMS",
        "source": "app",
        "status": "delivered",
        "messageId": "someMessageId",
        "conversationProviderId": "cI08i1Bls3iTB9bKgF01"
    }
    sms_message = handle_outbound_message(sms_data)
    print(sms_message)

    # Example Email message
    email_data = {
        "type": "OutboundMessage",
        "locationId": "kF4NJ5gzRyQF2gKFD34G",
        "body": "<div style=\"font-family: verdana, geneva; font-size: 11pt;\">Testing Email Notification</div>",
        "contactId": "3bN9f8LYJFG8F232XMUbfq",
        "conversationId": "yCdNo6pwyTLYKgg6V2gj",
        "dateAdded": "2024-01-12T12:59:04.045Z",
        "direction": "outbound",
        "messageType": "Email",
        "emailMessageId": "sddfDSF3G56GHG",
        "from": "Internal Notify <sample@email.service>",
        "threadId": "sddfDSF3G56GHG",
        "subject": "Order Confirmed",
        "to": ["example@email.com"],
        "source": "app",
        "messageId": "someEmailMessageId",
        "conversationProviderId": "cI08i1Bls3iTB9bKgF01"
    }
    email_message = handle_outbound_message(email_data)
    print(email_message)