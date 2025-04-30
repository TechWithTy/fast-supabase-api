// Enum for messageResponse.destination.type
export enum DestinationType {
  NUMBER = 'number',
  ASSISTANT = 'assistant',
  SIP = 'sip',
  STEP = 'step'
}

// Enum for transferMode in messageResponse.destination
export enum TransferMode {
  ROLLING_HISTORY = 'rolling-history',
  SWAP_SYSTEM_MESSAGE = 'swap-system-message-in-history'
}

// Enum for voicemail detection types
export enum VoicemailDetectionType {
  MACHINE_END_BEEP = 'machine_end_beep',
  MACHINE_END_SILENCE = 'machine_end_silence'
}

// Interface for the Destination object
export interface Destination {
  type: DestinationType;
  numberE164CheckEnabled?: boolean; // Only for 'number' type
  number?: string; // Only for 'number' type
  extension?: string; // Only for 'number' type
  message?: string;
  description?: string;
  assistantName?: string; // Only for 'assistant' type
  transferMode?: TransferMode; // Only for 'assistant' type
  sipUri?: string; // Only for 'sip' type
  stepName?: string; // Only for 'step' type
}

// Interface for Voicemail Detection object
export interface VoicemailDetection {
  provider: string; // e.g., "twilio"
  voicemailDetectionTypes: VoicemailDetectionType[];
  enabled: boolean;
  machineDetectionTimeout: number;
  machineDetectionSpeechThreshold: number;
  machineDetectionSpeechEndThreshold: number;
  machineDetectionSilenceTimeout: number;
}

// Interface for Transcriber configuration
export interface Transcriber {
  provider: string; // e.g., "deepgram"
  model: string; // e.g., "nova-2"
  language: string;
  smartFormat: boolean;
  keywords: string[];
  endpointing: number;
}

// Interface for Model Tools
export interface Tool {
  async: boolean;
  messages: {
    type: 'request-start' | 'request-complete' | 'request-failed';
    content: string;
    conditions?: {
      value: string;
      operator: 'eq' | 'ne' | 'gt' | 'lt';
      param: string;
    }[];
  }[];
  type: 'dtmf' | 'function'; // e.g., 'dtmf'
  function: {
    name: string;
    description: string;
    parameters: {
      type: 'object';
      properties: Record<string, any>;
      required: string[];
    };
  };
  server: {
    timeoutSeconds: number;
    url: string;
    secret: string;
  };
}

// Interface for the Assistant
export interface Assistant {
  transcriber: Transcriber;
  model: {
    messages: {
      content: string;
      role: 'assistant' | 'user' | 'system';
    }[];
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
  };
  voice: {
    provider: string;
    voiceId: string;
    speed: number;
    fillerInjectionEnabled: boolean;
    chunkPlan: {
      enabled: boolean;
      minCharacters: number;
      punctuationBoundaries: string[];
      formatPlan: {
        enabled: boolean;
        numberToDigitsCutoff: number;
      };
    };
  };
  recordingEnabled: boolean;
  clientMessages: string[];
  serverMessages: string[];
  silenceTimeoutSeconds: number;
  maxDurationSeconds: number;
  backgroundSound: string;
  backchannelingEnabled: boolean;
  backgroundDenoisingEnabled: boolean;
  modelOutputInMessagesEnabled: boolean;
  voicemailDetection: VoicemailDetection;
  transportConfigurations: {
    provider: string;
    timeout: number;
    record: boolean;
    recordingChannels: string;
  }[];
}

// Interface for Server Message Response
export interface ServerMessageResponsetype {
  destination?: Destination; // Call destination (optional)
  assistantId?: string; // Assistant ID if used (optional)
  assistant?: Assistant; // Assistant configuration (optional)
  assistantOverrides?: Assistant; // Overrides for the assistant
  squadId?: string; // Squad ID if applicable (optional)
  squad?: {
    name: string;
    members: {
      assistantId: string;
      assistant: Assistant;
      assistantOverrides?: Assistant;
    }[];
  };
  error?: string; // Error message (optional)
}
// Example of exporting an object
export const exampleServerMessageResponse = {
  messageResponse: {
    destination: {
      type: 'number',
      numberE164CheckEnabled: true,
      number: '+14155551234',
      extension: '123',
      message: 'Transferring your call now',
      description: 'Primary contact number for user'
    },
    assistantId: 'assistant-123',
    assistant: {
      transcriber: {
        provider: 'deepgram',
        model: 'nova-2',
        language: 'en',
        smartFormat: false,
        keywords: ['support', 'account'],
        endpointing: 255
      },
      model: {
        messages: [
          {
            content: 'How can I assist you today?',
            role: 'assistant'
          }
        ],
        tools: [
          {
            async: false,
            messages: [
              {
                type: 'request-start',
                content: 'Initiating tool now',
                conditions: [
                  {
                    value: 'start',
                    operator: 'eq',
                    param: 'status'
                  }
                ]
              }
            ],
            type: 'dtmf',
            function: {
              name: 'DTMF Function',
              description: 'Handles DTMF inputs',
              parameters: {
                type: 'object',
                properties: {},
                required: ['dtmfInput']
              }
            },
            server: {
              timeoutSeconds: 20,
              url: 'https://api.example.com/dtmf',
              secret: 'dtmf-secret'
            }
          }
        ],
        toolIds: ['tool-123'],
        provider: 'anyscale',
        model: 'gpt-4',
        temperature: 1.0,
        knowledgeBase: {
          provider: 'canonical',
          topK: 5,
          fileIds: ['file-001', 'file-002']
        },
        maxTokens: 512,
        emotionRecognitionEnabled: true,
        numFastTurns: 1
      },
      voice: {
        provider: 'azure',
        voiceId: 'andrew',
        speed: 1.25,
        fillerInjectionEnabled: false,
        chunkPlan: {
          enabled: true,
          minCharacters: 30,
          punctuationBoundaries: ['.', '!', '?'],
          formatPlan: {
            enabled: true,
            numberToDigitsCutoff: 2025
          }
        }
      },
      recordingEnabled: true,
      clientMessages: ['conversation-update', 'function-call', 'hang'],
      serverMessages: [
        'conversation-update',
        'end-of-call-report',
        'tool-calls'
      ],
      silenceTimeoutSeconds: 30,
      maxDurationSeconds: 600,
      backgroundSound: 'office',
      voicemailDetection: {
        provider: 'twilio',
        voicemailDetectionTypes: ['machine_end_beep', 'machine_end_silence'],
        enabled: true,
        machineDetectionTimeout: 30,
        machineDetectionSpeechThreshold: 3000,
        machineDetectionSpeechEndThreshold: 2000,
        machineDetectionSilenceTimeout: 5000
      }
    },
    error: null
  }
};
