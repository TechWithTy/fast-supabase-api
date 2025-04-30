export interface ClientMessage {
  type: ClientMessageType; // Enum of message types (conversation-update, hang, metadata, etc.)
}

// Enum for Client Message Types
export enum ClientMessageType {
  ConversationUpdate = 'conversation-update',
  Hang = 'hang',
  Metadata = 'metadata',
  ModelOutput = 'model-output',
  SpeechUpdate = 'speech-update',
  Transcript = 'transcript'
}

export interface ConversationUpdateMessage extends ClientMessage {
  type: ClientMessageType.ConversationUpdate;
  messagesOpenAIFormatted: OpenAIFormattedMessage[];
}

export interface OpenAIFormattedMessage {
  content: string;
  role: 'assistant' | 'user' | 'system';
}

export interface HangMessage extends ClientMessage {
  type: ClientMessageType.Hang;
}

export interface MetadataMessage extends ClientMessage {
  type: ClientMessageType.Metadata;
  metadata: any; // You can replace `any` with specific metadata type if available
}

export interface ModelOutputMessage extends ClientMessage {
  type: ClientMessageType.ModelOutput;
  output: ModelOutput;
}

export interface ModelOutput {
  tokens?: string[];
  toolCall?: ToolCall;
}

export interface ToolCall {
  toolId: string;
  parameters: any; // Tool-specific parameters
}

export interface SpeechUpdateMessage extends ClientMessage {
  type: ClientMessageType.SpeechUpdate;
  status: SpeechStatus;
  role: SpeechRole;
}

export enum SpeechStatus {
  Started = 'started',
  Stopped = 'stopped'
}

export enum SpeechRole {
  Assistant = 'assistant',
  User = 'user'
}

export interface TranscriptMessage extends ClientMessage {
  type: ClientMessageType.Transcript;
  role: TranscriptRole;
  transcriptType: TranscriptType;
  transcript: string;
}

export enum TranscriptRole {
  Assistant = 'assistant',
  User = 'user'
}

export enum TranscriptType {
  Partial = 'partial',
  Final = 'final'
}

// Example of a conversation update message
export const exampleConversationUpdate: ConversationUpdateMessage = {
  type: ClientMessageType.ConversationUpdate,
  messagesOpenAIFormatted: [
    {
      content: 'Hello, how can I assist you?',
      role: 'assistant'
    },
    {
      content: 'I need help with my account.',
      role: 'user'
    }
  ]
};

// Example of a transcript message
export const exampleTranscriptMessage: TranscriptMessage = {
  type: ClientMessageType.Transcript,
  role: TranscriptRole.User,
  transcriptType: TranscriptType.Final,
  transcript: 'I need help with my account.'
};
