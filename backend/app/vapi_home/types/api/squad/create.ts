import { KnowledgeBase, ToolMessage } from '../calls/create';

export interface CreateSquadRequest {
  name: string;
  members: SquadMember[];
  membersOverrides?: AssistantOverrides;
}

export interface SquadMember {
  assistantId: string;
  assistant: AssistantDetails;
  assistantOverrides?: AssistantOverrides;
}

export interface AssistantDetails {
  transcriber: TranscriberSettings;
  model: AssistantModel;
  voice: VoiceSettings;
  firstMessageMode: 'assistant-speaks-first' | 'user-speaks-first';
  recordingEnabled: boolean;
  hipaaEnabled: boolean;
  clientMessages: string[];
  serverMessages: string[];
  silenceTimeoutSeconds: number;
  maxDurationSeconds: number;
  backgroundSound: 'office' | 'white-noise';
  backchannelingEnabled: boolean;
  backgroundDenoisingEnabled: boolean;
  modelOutputInMessagesEnabled: boolean;
  transportConfigurations: TransportConfiguration[];
  voicemailDetection: VoicemailDetection;
  voicemailMessage: string;
  endCallMessage: string;
  endCallPhrases: string[];
  metadata?: Record<string, any>;
  serverUrl: string;
  serverUrlSecret: string;
  analysisPlan?: AnalysisPlan;
  artifactPlan?: ArtifactPlan;
  messagePlan?: MessagePlan;
  startSpeakingPlan?: SpeakingPlan;
  stopSpeakingPlan?: StopSpeakingPlan;
  credentialIds: string[];
}

export interface AssistantOverrides {
  transcriber?: TranscriberSettings;
  model?: AssistantModel;
  voice?: VoiceSettings;
}

export interface TranscriberSettings {
  provider: 'deepgram' | 'google' | 'ibm';
  model: string;
  language: string;
  smartFormat: boolean;
  keywords: string[];
  endpointing: number;
}

export interface AssistantModel {
  messages: Message[];
  tools: Tool[];
  toolIds: string[];
  provider: 'anyscale' | 'openai';
  model: string;
  temperature: number;
  knowledgeBase?: KnowledgeBase;
  maxTokens: number;
  emotionRecognitionEnabled: boolean;
  numFastTurns: number;
}

export interface Message {
  content: string;
  type?: string;
  role: 'assistant' | 'user';
}

export interface Tool {
  async: boolean;
  messages: ToolMessage[];
  type: 'dtmf';
  function: ToolFunction;
  server: ToolServer;
}

export interface ToolFunction {
  name: string;
  description: string;
  parameters: ToolParameters;
}

export interface ToolParameters {
  type: 'object';
  properties: Record<string, any>;
  required: string[];
}

export interface ToolServer {
  timeoutSeconds: number;
  url: string;
  secret: string;
}

export interface VoiceSettings {
  provider: 'azure' | 'google' | 'amazon';
  voiceId: string;
  speed: number;
  chunkPlan: ChunkPlan;
}

export interface ChunkPlan {
  enabled: boolean;
  minCharacters: number;
  punctuationBoundaries: string[];
  formatPlan: FormatPlan;
}

export interface FormatPlan {
  enabled: boolean;
  numberToDigitsCutoff: number;
}

export interface VoicemailDetection {
  provider: 'twilio';
  voicemailDetectionTypes: string[];
  enabled: boolean;
  machineDetectionTimeout: number;
  machineDetectionSpeechThreshold: number;
  machineDetectionSpeechEndThreshold: number; // Add this property
  machineDetectionSilenceTimeout: number;
}

// Now include it in your object

export interface TransportConfiguration {
  provider: 'twilio' | 'vonage';
  timeout: number;
  record: boolean;
  recordingChannels: 'mono' | 'stereo';
}

export interface AnalysisPlan {
  summaryPrompt: string;
  summaryRequestTimeoutSeconds: number;
  structuredDataRequestTimeoutSeconds: number;
  successEvaluationPrompt: string;
  successEvaluationRubric: 'NumericScale' | 'PassFail';
  successEvaluationRequestTimeoutSeconds: number;
  structuredDataPrompt: string; // Missing property
  structuredDataSchema: Schema;
}

export interface Schema {
  type: string;
  properties: Record<string, any>;
  required: string[];
}

export interface ArtifactPlan {
  videoRecordingEnabled: boolean;
  recordingS3PathPrefix: string;
}

export interface MessagePlan {
  idleMessages: string[];
  idleMessageMaxSpokenCount: number;
  idleTimeoutSeconds: number;
}

export interface SpeakingPlan {
  waitSeconds: number;
  smartEndpointingEnabled: boolean;
  transcriptionEndpointingPlan: TranscriptionEndpointingPlan;
}

export interface TranscriptionEndpointingPlan {
  onPunctuationSeconds: number;
  onNoPunctuationSeconds: number;
  onNumberSeconds: number;
}

export interface StopSpeakingPlan {
  numWords: number;
  voiceSeconds: number;
  backoffSeconds: number;
}
