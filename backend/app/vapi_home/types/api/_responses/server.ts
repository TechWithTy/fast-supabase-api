// Enum for the message type
export enum MessageType {
  ASSISTANT_REQUEST = 'assistant-request',
  CONVERSATION_UPDATE = 'conversation-update',
  END_OF_CALL_REPORT = 'end-of-call-report',
  MODEL_OUTPUT = 'model-output',
  PHONE_CALL_CONTROL = 'phone-call-control',
  SPEECH_UPDATE = 'speech-update',
  STATUS_UPDATE = 'status-update',
  TOOL_CALLS = 'tool-calls'
}

// Enum for call ended reason
export enum EndedReason {
  ASSISTANT_ERROR = 'assistant-error',
  ASSISTANT_NOT_FOUND = 'assistant-not-found',
  CUSTOMER_BUSY = 'customer-busy',
  CUSTOMER_ENDED_CALL = 'customer-ended-call'
  // Additional reasons as per the provided list
}

// Common Call Object
export interface Call {
  id: string; // Unique call ID
  status: 'queued' | 'ringing' | 'in-progress' | 'ended'; // Status of the call
  endedReason?: EndedReason; // Reason why the call ended (optional if status is 'ended')
  timestamp: string; // Timestamp of the call (ISO 8601 format)
  // Any other fields relevant to the call object
}

// PhoneNumber Object
export interface PhoneNumber {
  id: string; // Phone number ID
  e164: string; // E.164 formatted number
  // Additional phone number properties
}

// Assistant Object
export interface Assistant {
  id: string; // Assistant ID
  name: string; // Assistant name
  // Additional properties of the assistant
}

// Customer Object
export interface Customer {
  id: string; // Customer ID
  name: string; // Customer name
  phone: string; // Customer phone number
  // Additional customer details
}

// Artifact Object for live call artifacts
export interface Artifact {
  // Example: live transcriptions, recordings, etc.
  transcriptions: string[];
  recordings: string[];
}

// Server Message Interface
export interface ServerMessage {
  type: MessageType; // The type of the message (required)
  assistant: Assistant; // Active assistant object
  phoneNumber: PhoneNumber; // Phone number object associated with the call
  customer: Customer; // Customer object associated with the call
  call: Call; // Main call object
  artifact: Artifact; // Artifacts generated during the call (optional)
  timestamp: string; // Timestamp when the message was sent (ISO 8601 format)
}

export const exampleServerResponses = {
  type: 'assistant-request',
  assistant: {
    id: 'assistant-id-123',
    name: 'Sample Assistant'
  },
  phoneNumber: {
    id: 'phone-number-id-123',
    e164: '+1234567890'
  },
  customer: {
    id: 'customer-id-123',
    name: 'John Doe',
    phone: '+1234567890'
  },
  call: {
    id: 'call-id-123',
    status: 'in-progress',
    timestamp: '2023-11-07T05:31:56Z'
  },
  artifact: {
    transcriptions: ['Hello, how may I assist you?'],
    recordings: ['https://example.com/recording.mp3']
  },
  timestamp: '2023-11-07T05:32:00Z'
};
