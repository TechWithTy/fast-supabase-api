from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class Flags(BaseModel):
    is_authenticated: bool = Field(..., alias="is-authenticated")
    is_routed: bool = Field(..., alias="is-routed")
    is_big: bool = Field(..., alias="is-big")
    is_system_test: bool = Field(..., alias="is-system-test")
    is_test_mode: bool = Field(..., alias="is-test-mode")

class MessageHeaders(BaseModel):
    message_id: str = Field(..., alias="message-id")
    from_: str = Field(..., alias="from")
    to: str

class Message(BaseModel):
    attachments: List[str]
    headers: MessageHeaders
    size: int

class DeliveryStatus(BaseModel):
    attempt_no: int = Field(..., alias="attempt-no")
    code: int
    message: str
    description: str
    session_seconds: float = Field(..., alias="session-seconds")
    enhanced_code: str = Field(..., alias="enhanced-code")
    mx_host: str = Field(..., alias="mx-host")
    utf8: bool
    i_first_delivery_attempt_seconds: float = Field(..., alias="i-first-delivery-attempt-seconds")

class Envelope(BaseModel):
    sender: str
    targets: str
    transport: str
    sending_ip: str = Field(..., alias="sending-ip")
    i_ip_pool_id: str = Field(..., alias="i-ip-pool-id")
    i_ip_pool_name: str = Field(..., alias="i-ip-pool-name")

class WebhookPayload(BaseModel):
    event: str
    id: str
    timestamp: int
    flags: Flags
    message: Message
    log_level: str = Field(..., alias="log-level")
    recipient: str
    recipient_domain: str = Field(..., alias="recipient-domain")
    tags: List[str]
    recipient_provider: str = Field(..., alias="recipient-provider")
    campaigns: List[str]
    delivery_status: DeliveryStatus = Field(..., alias="delivery-status")
    envelope: Envelope

class LCEmailStats(BaseModel):
    type: str
    location_id: str = Field(..., alias="locationId")
    company_id: str = Field(..., alias="companyId")
    webhook_payload: WebhookPayload = Field(..., alias="webhookPayload")

def process_lc_email_stats(data: Dict) -> LCEmailStats:
    """
    Process the incoming webhook data for LC Email Stats.

    Args:
        data (Dict): The raw webhook payload.

    Returns:
        LCEmailStats: A validated LCEmailStats object.
    """
    return LCEmailStats.parse_obj(data)

# Example usage
example_data = {
    "type": "LCEmailStats",
    "locationId": "ve9EPM428h8vShlRW1KT",
    "companyId": "ve9EPM428h8vShlRW1KT",
    "webhookPayload": {
        "event": "delivered",
        "id": "ve9EPM428h8vShlRW1KT",
        "timestamp": 1714032441,
        "flags": {
            "is-authenticated": True,
            "is-routed": False,
            "is-big": False,
            "is-system-test": False,
            "is-test-mode": False
        },
        "message": {
            "attachments": [],
            "headers": {
                "message-id": "<message-id>",
                "from": "Aaditya Chakravarty <dummy@example.com>",
                "to": "test@example.com"
            },
            "size": 1725
        },
        "log-level": "info",
        "recipient": "test@example.com",
        "recipient-domain": "example.com",
        "tags": ["loc_ve9EPM428h8vShlRW1KT", "com_ve9EPM428h8vShlRW1KT", "et_other"],
        "recipient-provider": "Other",
        "campaigns": [],
        "delivery-status": {
            "attempt-no": 1,
            "code": 250,
            "message": "OK",
            "description": "",
            "session-seconds": 0.087,
            "enhanced-code": "",
            "mx-host": "mail.example.com",
            "utf8": True,
            "i-first-delivery-attempt-seconds": 0.047
        },
        "envelope": {
            "sender": "<sender-id>",
            "targets": "test@example.com",
            "transport": "smtp",
            "sending-ip": "127.0.0.1",
            "i-ip-pool-id": "65cc66e77a4d4f63649d394c",
            "i-ip-pool-name": "<pool-name>"
        }
    }
}

lc_email_stats = process_lc_email_stats(example_data)
print(lc_email_stats)