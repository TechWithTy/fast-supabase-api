// ElevenLabs API Types
export interface ElevenLabsVoice {
  voice_id: string;
  name: string;
  description?: string;
  language: string;
}

export interface GenerateSpeechRequest {
  voice_id: string;
  text: string;
  model_id?: string; // Optional, defaults to 'eleven_multilingual_v2'
}

export interface GenerateSpeechResponse {
  audio_url: string;
  duration: number;
  format: string;
}

export interface CloneVoiceRequest {
  voice_name: string;
  samples: string[]; // Array of audio sample URLs or paths
}

export interface CloneVoiceResponse {
  voice_id: string;
  status: 'success' | 'error';
  message?: string;
}
