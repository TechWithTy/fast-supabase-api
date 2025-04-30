// Reusing the assistant types from CreateCallRequest

import { CampaignBase } from '@/types/_dashboard/campaign';
import { Assistant, CallStatus, ConversationMessage } from './create';
import { CallType } from '@prisma/client';
import { EndedReason } from './_enums';

// Add the other reasons as specified...

// Cost breakdown of the call
export interface CostBreakdown {
  transport: number;
  stt: number;
  llm: number;
  tts: number;
  vapi: number;
  total: number;
  llmPromptTokens: number;
  llmCompletionTokens: number;
  ttsCharacters: number;
}

// Artifact Plan and Analysis
export interface ArtifactPlan {
  videoRecordingEnabled: boolean;
  recordingS3PathPrefix: string;
}

export interface AnalysisPlan {
  summary: string;
  structuredData: Record<string, unknown>;
  successEvaluation: string;
}

// Call response type
export interface GetCallResponse {
  id: string; // Unique identifier for the call
  orgId: string; // Unique identifier for the org
  type: CallType; // Type of the call
  phoneCallProvider: 'twilio' | 'vonage' | 'vapi'; // Provider of the call
  phoneCallTransport: 'sip' | 'pstn'; // Transport of the call
  status: CallStatus; // Status of the call
  endedReason?: EndedReason; // Why the call ended (optional)
  messages: ConversationMessage[]; // Messages spoken during the call
  destination?: Destination; // Transfer destination
  monitor: Monitor;

  createdAt: string; // ISO date-time of call creation
  updatedAt: string; // ISO date-time of last update
  startedAt?: string; // ISO date-time of when the call started
  endedAt?: string; // ISO date-time of when the call ended
  cost: number; // Cost of the call
  costBreakdown: CostBreakdown; // Cost breakdown
  transcript: string; // Transcript of the call
  recordingUrl?: string; // Recording URL
  stereoRecordingUrl?: string; // Stereo recording URL
  artifact?: ArtifactPlan; // Artifact details
  analysis?: AnalysisPlan; // Analysis details
  assistantId?: string; // Assistant ID
  assistant?: Assistant; // Assistant data (reusing existing type)
}

export interface ghlCallResponseo extends GetCallResponse {
  contactId: string; // Unique identifier for the contact associated with the call
  campaignId: string; // Unique identifier for the campaign associated with the call
}

// Destination object
export interface Destination {
  type: 'number'; // Type of the destination
  numberE164CheckEnabled: boolean; // E164 validation
  number: string; // Phone number
  extension: string; // Extension (optional)
  message: string; // Message (optional)
  description: string; // Description (optional)
}

export type Monitor = {
  listenUrl: string;
  controlUrl: string;
};

export interface CallCampaignAnalytics extends CampaignBase {
  id: string; // Campaign ID
  callType: CallType; // Type of call (inbound, outbound, web call)
  callStatus: CallStatus; // Status of the call
  endedReason?: EndedReason; // Reason for call termination
  cost: number; // Total cost of the call
  costBreakdown: CostBreakdown; // Detailed cost breakdown
  messages: ConversationMessage[]; // Array of messages in the call
  recordingUrl?: string; // URL for call recording
  stereoRecordingUrl?: string; // URL for stereo recording (optional)
  transcript: string; // Transcript of the call
  assistantId?: string; // Optional assistant ID for the call
  assistant?: Assistant; // Optional assistant details
  artifact?: ArtifactPlan; // Optional artifact plan for the call
  analysis?: AnalysisPlan; // Optional analysis plan for the call
}
