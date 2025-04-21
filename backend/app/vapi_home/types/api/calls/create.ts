// Enum for transcriber providers
export type TranscriberProvider = 'deepgram' | 'azure' | 'google' | 'aws';

// Enum for LLM providers
export type ModelProvider =
  | 'anyscale'
  | 'openai'
  | 'azure'
  | 'google'
  | 'custom';

// Enum for background sounds
export type BackgroundSound = 'off' | 'office';

// Enum for first message modes
export type FirstMessageMode =
  | 'assistant-speaks-first'
  | 'assistant-waits-for-user';

// Enum for call statuses
export type CallStatus =
  | 'queued'
  | 'ringing'
  | 'in-progress'
  | 'forwarding'
  | 'ended';

// Enum for call end reasons

// Type for creating a call request
export interface CreateCallRequest {
  name: string; // The name of the call
  assistantId?: string; // Existing assistant ID if you're using an assistant that has already been created
  assistant?: Assistant; // Transient assistant data (used if assistantId is not provided)
  assistantOverrides?: AssistantOverrides; // Overrides for assistant or assistantId settings
  squadId?: string; // Existing squad ID
  squad?: Squad; // Transient squad data (used if squadId is not provided)
  phoneNumberId?: string; // Existing phone number ID
  phoneNumber?: PhoneNumber; // Transient phone number data (used if phoneNumberId is not provided)
  customerId?: string; // Existing customer ID
  customer?: Customer; // Transient customer data (used if customerId is not provided)
}

// Transcriber options
export interface Transcriber {
  provider: TranscriberProvider; // Available transcriber providers
  model: string; // Model used for transcription
  language: string; // Language code (e.g., 'en', 'bg')
  smartFormat: boolean; // Smart formatting options
  keywords: string[]; // Keywords to improve transcription accuracy
  endpointing?: number; // Endpointing threshold
}

// Assistant model tools
export interface ModelTool {
  async: boolean; // Whether the tool runs asynchronously
  messages: ToolMessage[]; // Messages associated with the tool
  type: 'dtmf'; // Type of tool (for example, DTMF tool)
  function: ModelFunction; // Function details of the tool
  server: ServerDetails; // Server details for tool execution
}

// Function details for model tool
export interface ModelFunction {
  name: string; // Name of the function
  description: string; // Function description
  parameters: {
    type: 'object'; // Type of parameters (usually object)
    properties: Record<string, unknown>; // Parameter properties
    required: string[]; // Required parameter names
  };
}

// Server details for tool execution
export interface ServerDetails {
  timeoutSeconds: number; // Timeout for server requests
  url: string; // Server URL
  secret: string; // Server secret for authentication
}

// Assistant model
export interface AssistantModel {
  assistantID?: string;
  messages: ConversationMessage[]; // Messages exchanged by the assistant
  tools: ModelTool[]; // Tools that the assistant can use
  toolIds: string[]; // List of tool IDs
  provider: ModelProvider; // Available LLM providers
  model: string; // Model identifier
  temperature: number; // Temperature for model responses
  knowledgeBase?: KnowledgeBase; // Optional knowledge base for model queries
  maxTokens: number; // Maximum number of tokens for responses
  emotionRecognitionEnabled: boolean; // Whether emotion recognition is enabled
  numFastTurns: number; // Number of fast-turns allowed
}

// Knowledge base configuration
export interface KnowledgeBase {
  provider: 'canonical'; // Knowledge base provider
  topK: number; // Number of top results returned
  fileIds: string[]; // File IDs for the knowledge base
}

// Assistant voice options
export interface Voice {
  fillerInjectionEnabled: boolean; // Whether filler words like 'um' are injected
  provider: 'azure' | 'google' | 'anyscale'; // Voice provider
  voiceId: string; // Voice identifier
  speed: number; // Speed of the speech
  chunkPlan: ChunkPlan; // Plan for chunking voice output
}

// Chunk plan for voice output
export interface ChunkPlan {
  enabled: boolean; // Whether chunking is enabled
  minCharacters: number; // Minimum characters per chunk
  punctuationBoundaries: string[]; // Punctuation boundaries for chunks
  formatPlan: FormatPlan; // Plan for formatting numbers and punctuation
}

// Format plan for speech
export interface FormatPlan {
  enabled: boolean; // Whether formatting is enabled
  numberToDigitsCutoff: number; // Cutoff for converting numbers to digits
}

export enum MessageType {
  UserMessage = 'UserMessage',
  SystemMessage = 'SystemMessage',
  BotMessage = 'BotMessage',
  FunctionCallMessage = 'FunctionCallMessage',
  ToolCallMessage = 'ToolCallMessage',
  ToolCallResultMessage = 'ToolCallResultMessage',
  FunctionResultMessage = 'FunctionResultMessage'
}
// Message structure
export interface Message {
  role: string; // The role in the conversation (user, system, bot, function call, etc.)
  message: string; // The content of the message
  time: number; // The timestamp when the message was sent
  secondsFromStart: number; // The number of seconds from the start of the conversation
}

export interface UserMessage extends Message {
  role: 'user'; // The role of the user
  endTime: number; // The timestamp when the message ended
  duration?: number; // The duration of the message in seconds (optional)
}
export interface SystemMessage extends Message {
  role: 'system'; // The role of the system
}

export interface BotMessage extends Message {
  role: 'bot'; // The role of the bot
  endTime: number; // The timestamp when the message ended
}

export interface FunctionCallMessage extends Message {
  role: 'function-call'; // The role of the function call
  name: string; // The name of the function being called
  args: string; // The arguments for the function call in JSON format
}
export interface NestedToolCallMessage extends Message {
  role: 'tool-call'; // The role of the tool call in the conversation
  toolCalls: object[]; // The list of tool calls made during the conversation
}

export interface ToolCallResultMessage extends Message {
  role: 'tool-call-result'; // The role of the tool call result
  toolCallId: string; // The ID of the tool call
  name: string; // The name of the tool that returned the result
  result: string; // The result of the tool call in JSON format
}
export interface FunctionResultMessage extends Message {
  role: 'function-result'; // The role of the function result
  name: string; // The name of the function that returned the result
  result: string; // The result of the function call in JSON format
}

export type ConversationMessage =
  | UserMessage
  | SystemMessage
  | BotMessage
  | FunctionCallMessage
  | NestedToolCallMessage
  | ToolCallResultMessage
  | FunctionResultMessage;

// Enum for tool message types in the correct order
export enum ToolMessageType {
  ToolMessageStart = 'request-start',
  ToolMessageComplete = 'request-complete',
  ToolMessageFailed = 'request-failed',
  ToolMessageDelayed = 'request-response-delayed'
}

// Interface for tool message conditions
export interface Condition {
  value: string; // Value to compare
  operator: ConditionOperator; // Operator for comparison
  param: string; // Parameter name to check
}

// Enum for condition operators
export enum ConditionOperator {
  Eq = 'eq',
  Neq = 'neq',
  Gt = 'gt',
  Gte = 'gte',
  Lt = 'lt',
  Lte = 'lte'
}

// Enum for message roles
export enum MessageRole {
  Assistant = 'assistant',
  System = 'system'
}

// Interface for tool messages
export interface ToolMessage {
  type: ToolMessageType; // Type of the tool message (start, complete, failed, delayed)
  content: string; // The content of the message
  role?: MessageRole; // Optional, default is 'assistant', can be 'system'
  endCallAfterSpokenEnabled?: boolean; // Whether to end the call after speaking this message, default false
  timingMilliseconds?: number; // For delayed messages, how long to wait before saying the message
  conditions?: readonly Condition[]; // Allow readonly arrays for conditions
}

// Tool message array for usage
export type ToolMessagesArray = ToolMessage[];

// Assistant configuration
export interface Assistant {
  transcriber: Transcriber; // Transcriber options
  model: AssistantModel; // Model options for the assistant
  voice: Voice; // Voice options for the assistant
  firstMessageMode: FirstMessageMode; // Defines who speaks first
  recordingEnabled: boolean; // Whether recording is enabled
  hipaaEnabled: boolean; // Whether HIPAA compliance is enabled
  clientMessages: string[]; // List of client messages
  serverMessages: string[]; // List of server messages
  silenceTimeoutSeconds: number; // Timeout for silence before ending the call
  maxDurationSeconds: number; // Maximum duration of the call in seconds
  backgroundSound: BackgroundSound; // Background sound during the call
  backchannelingEnabled: boolean; // Whether backchanneling ('mm-hmm') is enabled
  backgroundDenoisingEnabled: boolean; // Whether background denoising is enabled
}

// Assistant overrides for call configuration
export interface AssistantOverrides {
  transcriber?: Transcriber; // Override transcriber options
  model?: Partial<AssistantModel>; // Override model options
  voice?: Partial<Voice>; // Override voice options
  clientMessages?: string[]; // Override client messages
  serverMessages?: string[]; // Override server messages
}

// Squad configuration (group of assistants)
export interface Squad {
  name: string; // Name of the squad
  members: AssistantMember[]; // List of squad members (assistants)
}

// Assistant member within a squad
export interface AssistantMember {
  assistantId: string; // Existing assistant ID
  assistant?: Assistant; // Transient assistant data
  assistantOverrides?: AssistantOverrides; // Override assistant configuration
}

// Phone number configuration
export interface PhoneNumber {
  fallbackDestination: FallbackDestination; // Fallback if the primary destination is unreachable
  twilioPhoneNumber: string; // Twilio phone number
  twilioAccountSid: string; // Twilio account SID
  twilioAuthToken: string; // Twilio auth token
  name: string; // Name of the phone number
  assistantId: string; // Associated assistant ID
  squadId: string; // Associated squad ID
  serverUrl: string; // Server URL for call handling
  serverUrlSecret: string; // Server URL secret
}

// Fallback destination in case the call fails
export interface FallbackDestination {
  type: 'number'; // Fallback type
  numberE164CheckEnabled: boolean; // Whether E164 number validation is enabled
  number: string; // Fallback number
  extension: string; // Fallback extension (if any)
  message: string; // Fallback message
  description: string; // Description of fallback
}

// Customer configuration
export interface Customer {
  numberE164CheckEnabled: boolean; // Whether E164 number validation is enabled
  extension?: string; // Extension for the customer
  number: string; // Customer's phone number
  sipUri?: string; // SIP URI (if any)
  name: string; // Customer's name
}
