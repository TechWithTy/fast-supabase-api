// Type for Transcriber options
interface Transcriber {
  provider: 'deepgram' | 'google' | 'aws'; // Example options, expand if needed
  model: string;
  language: string; // ISO language code, e.g., 'en' for English
  smartFormat: boolean;
  keywords: string[];
  endpointing: number;
}

// Type for conditions in the model messages
interface Condition {
  value: string;
  operator: 'eq' | 'neq' | 'gt' | 'lt'; // Example comparison operators
  param: string;
}

// Type for model messages
interface Message {
  content: string;
  role: 'user' | 'assistant' | 'tool' | 'function' | 'system';
  type?: string;
  conditions?: Condition[];
}

// Type for tool function parameters
interface ToolFunctionParameters {
  type: 'object';
  properties: Record<string, any>;
  required: string[];
}

// Type for a Tool
interface Tool {
  async: boolean;
  messages: Message[];
  type: string;
  function: {
    name: string;
    description: string;
    parameters: ToolFunctionParameters;
  };
  server: {
    timeoutSeconds: number;
    url: string;
    secret: string;
  };
}

// Type for the Model configuration
interface Model {
  messages: Message[];
  tools: Tool[];
  toolIds: string[];
  provider: string;
  model: string;
  temperature: number;
  knowledgeBase: {
    provider: string;
    topK: number;
    fileIds: string[];
  };
  maxTokens: number;
  emotionRecognitionEnabled: boolean;
  numFastTurns: number;
}

// Type for the Voice configuration
interface AssistantVoice {
  fillerInjectionEnabled: boolean;
  provider: 'azure' | 'aws' | 'google' | '11labs'; // Example voice providers
  voiceId: string;
  speed: number;
  chunkPlan: {
    enabled: boolean;
    minCharacters: number;
    punctuationBoundaries: string[];
    formatPlan: {
      enabled: boolean;
      numberToDigitsCutoff: number;
    };
  };
}

// Type for the main CreateAssistantRequest
interface CreateAssistantRequest {
  transcriber: Transcriber;
  model: Model;
  voice: AssistantVoice;
  firstMessageMode:
    | 'assistant-speaks-first'
    | 'assistant-speaks-first-with-model-generated-message'
    | 'assistant-waits-for-user';
  recordingEnabled: boolean;
  hipaaEnabled: boolean;
  clientMessages: string[];
  serverMessages: string[];
  silenceTimeoutSeconds: number;
  maxDurationSeconds: number;
  backgroundSound: 'off' | 'office';
  backchannelingEnabled: boolean;
  backgroundDenoisingEnabled: boolean;
  modelOutputInMessagesEnabled: boolean;
  transportConfigurations: {
    provider: 'twilio' | 'vonage'; // Example transport providers
    timeout: number;
    record: boolean;
    recordingChannels: 'mono' | 'stereo';
  }[];
  name: string;
  firstMessage: string;
  voicemailDetection: {
    provider: 'twilio';
    voicemailDetectionTypes: string[];
    enabled: boolean;
    machineDetectionTimeout: number;
    machineDetectionSpeechThreshold: number;
    machineDetectionSpeechEndThreshold: number;
    machineDetectionSilenceTimeout: number;
  };
  voicemailMessage: string;
  endCallMessage: string;
  endCallPhrases: string[];
  metadata: Record<string, any>;
  serverUrl: string;
  serverUrlSecret: string;
  analysisPlan: {
    summaryPrompt: string;
    summaryRequestTimeoutSeconds: number;
    structuredDataRequestTimeoutSeconds: number;
    successEvaluationPrompt: string;
    successEvaluationRubric: string;
    successEvaluationRequestTimeoutSeconds: number;
    structuredDataPrompt: string;
    structuredDataSchema: {
      type: string;
      items: Record<string, any>;
      properties: Record<string, any>;
      description: string;
      required: string[];
    };
  };
  artifactPlan: {
    videoRecordingEnabled: boolean;
    recordingS3PathPrefix: string;
  };
  messagePlan: {
    idleMessages: string[];
    idleMessageMaxSpokenCount: number;
    idleTimeoutSeconds: number;
  };
  startSpeakingPlan: {
    waitSeconds: number;
    smartEndpointingEnabled: boolean;
    transcriptionEndpointingPlan: {
      onPunctuationSeconds: number;
      onNoPunctuationSeconds: number;
      onNumberSeconds: number;
    };
  };
  stopSpeakingPlan: {
    numWords: number;
    voiceSeconds: number;
    backoffSeconds: number;
  };
  credentialIds: string[];
}
