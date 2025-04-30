// Call types
export type CallType = 'inboundPhoneCall' | 'outboundPhoneCall' | 'webCall';

// Available call statuses
export type CallStatus =
  | 'queued'
  | 'ringing'
  | 'in-progress'
  | 'forwarding'
  | 'ended';

// Call end reasons
export type EndedReason =
  | 'assistant-error'
  | 'assistant-not-found'
  | 'db-error'
  | 'no-server-available'
  | 'license-check-failed'
  | 'pipeline-error-openai-llm-failed'
  | 'pipeline-error-azure-openai-llm-failed'
  | 'pipeline-error-groq-llm-failed'
  | 'pipeline-error-anthropic-llm-failed'
  | 'pipeline-error-vapi-llm-failed'
  | 'pipeline-error-vapi-401-unauthorized'
  | 'pipeline-error-vapi-403-model-access-denied'
  | 'pipeline-error-vapi-429-exceeded-quota'
  | 'pipeline-error-vapi-500-server-error'
  | 'pipeline-error-openai-voice-failed'
  | 'pipeline-error-cartesia-voice-failed'
  | 'pipeline-error-deepgram-transcriber-failed'
  | 'pipeline-error-deepgram-voice-failed'
  | 'pipeline-error-gladia-transcriber-failed'
  | 'pipeline-error-eleven-labs-voice-failed'
  | 'pipeline-error-playht-voice-failed'
  | 'pipeline-error-lmnt-voice-failed'
  | 'pipeline-error-azure-voice-failed'
  | 'pipeline-error-rime-ai-voice-failed'
  | 'pipeline-error-neets-voice-failed'
  | 'pipeline-no-available-model'
  | 'worker-shutdown'
  | 'unknown-error'
  | 'vonage-disconnected'
  | 'vonage-failed-to-connect-call'
  | 'phone-call-provider-bypass-enabled-but-no-call-received'
  | 'vapifault-phone-call-worker-setup-socket-error'
  | 'vapifault-phone-call-worker-worker-setup-socket-timeout'
  | 'vapifault-phone-call-worker-could-not-find-call'
  | 'vapifault-transport-never-connected'
  | 'vapifault-web-call-worker-setup-failed'
  | 'vapifault-transport-connected-but-call-not-active'
  | 'assistant-not-invalid'
  | 'assistant-not-provided'
  | 'call-start-error-neither-assistant-nor-server-set'
  | 'assistant-request-failed'
  | 'assistant-request-returned-error'
  | 'assistant-request-returned-unspeakable-error'
  | 'assistant-request-returned-invalid-assistant'
  | 'assistant-request-returned-no-assistant'
  | 'assistant-request-returned-forwarding-phone-number'
  | 'assistant-ended-call'
  | 'assistant-said-end-call-phrase'
  | 'assistant-forwarded-call'
  | 'assistant-join-timed-out'
  | 'customer-busy'
  | 'customer-ended-call'
  | 'customer-did-not-answer'
  | 'customer-did-not-give-microphone-permission'
  | 'assistant-said-message-with-end-call-enabled'
  | 'exceeded-max-duration'
  | 'manually-canceled'
  | 'phone-call-provider-closed-websocket'
  | 'pipeline-error-openai-401-unauthorized'
  | 'pipeline-error-openai-403-model-access-denied'
  | 'pipeline-error-openai-429-exceeded-quota'
  | 'pipeline-error-openai-500-server-error'
  | 'pipeline-error-azure-openai-401-unauthorized'
  | 'pipeline-error-azure-openai-403-model-access-denied'
  | 'pipeline-error-azure-openai-429-exceeded-quota'
  | 'pipeline-error-azure-openai-500-server-error'
  | 'pipeline-error-groq-401-unauthorized'
  | 'pipeline-error-groq-403-model-access-denied'
  | 'pipeline-error-groq-429-exceeded-quota'
  | 'pipeline-error-groq-500-server-error'
  | 'pipeline-error-anthropic-401-unauthorized'
  | 'pipeline-error-anthropic-403-model-access-denied'
  | 'pipeline-error-anthropic-429-exceeded-quota'
  | 'pipeline-error-anthropic-500-server-error'
  | 'pipeline-error-together-ai-401-unauthorized'
  | 'pipeline-error-together-ai-403-model-access-denied'
  | 'pipeline-error-together-ai-429-exceeded-quota'
  | 'pipeline-error-together-ai-500-server-error'
  | 'pipeline-error-together-ai-llm-failed'
  | 'pipeline-error-anyscale-401-unauthorized'
  | 'pipeline-error-anyscale-403-model-access-denied'
  | 'pipeline-error-anyscale-429-exceeded-quota'
  | 'pipeline-error-anyscale-500-server-error'
  | 'pipeline-error-anyscale-llm-failed'
  | 'pipeline-error-openrouter-401-unauthorized'
  | 'pipeline-error-openrouter-403-model-access-denied'
  | 'pipeline-error-openrouter-429-exceeded-quota'
  | 'pipeline-error-openrouter-500-server-error'
  | 'pipeline-error-openrouter-llm-failed'
  | 'pipeline-error-perplexity-ai-401-unauthorized'
  | 'pipeline-error-perplexity-ai-403-model-access-denied'
  | 'pipeline-error-perplexity-ai-429-exceeded-quota'
  | 'pipeline-error-perplexity-ai-500-server-error'
  | 'pipeline-error-perplexity-ai-llm-failed'
  | 'pipeline-error-deepinfra-401-unauthorized'
  | 'pipeline-error-deepinfra-403-model-access-denied'
  | 'pipeline-error-deepinfra-429-exceeded-quota'
  | 'pipeline-error-deepinfra-500-server-error'
  | 'pipeline-error-deepinfra-llm-failed'
  | 'pipeline-error-runpod-401-unauthorized'
  | 'pipeline-error-runpod-403-model-access-denied'
  | 'pipeline-error-runpod-429-exceeded-quota'
  | 'pipeline-error-runpod-500-server-error'
  | 'pipeline-error-runpod-llm-failed'
  | 'pipeline-error-custom-llm-401-unauthorized'
  | 'pipeline-error-custom-llm-403-model-access-denied'
  | 'pipeline-error-custom-llm-429-exceeded-quota'
  | 'pipeline-error-custom-llm-500-server-error'
  | 'pipeline-error-custom-llm-llm-failed'
  | 'pipeline-error-cartesia-socket-hang-up'
  | 'pipeline-error-cartesia-requested-payment'
  | 'pipeline-error-cartesia-500-server-error'
  | 'pipeline-error-cartesia-522-server-error'
  | 'pipeline-error-eleven-labs-voice-not-found'
  | 'pipeline-error-eleven-labs-quota-exceeded'
  | 'pipeline-error-eleven-labs-unauthorized-access'
  | 'pipeline-error-eleven-labs-unauthorized-to-access-model'
  | 'pipeline-error-eleven-labs-professional-voices-only-for-creator-plus'
  | 'pipeline-error-eleven-labs-blocked-free-plan-and-requested-upgrade'
  | 'pipeline-error-eleven-labs-blocked-concurrent-requests-and-requested-upgrade'
  | 'pipeline-error-eleven-labs-blocked-using-instant-voice-clone-and-requested-upgrade'
  | 'pipeline-error-eleven-labs-system-busy-and-requested-upgrade'
  | 'pipeline-error-eleven-labs-voice-not-fine-tuned'
  | 'pipeline-error-eleven-labs-invalid-api-key'
  | 'pipeline-error-eleven-labs-invalid-voice-samples'
  | 'pipeline-error-eleven-labs-voice-disabled-by-owner'
  | 'pipeline-error-eleven-labs-blocked-account-in-probation'
  | 'pipeline-error-eleven-labs-blocked-content-against-their-policy'
  | 'pipeline-error-eleven-labs-missing-samples-for-voice-clone'
  | 'pipeline-error-eleven-labs-voice-not-fine-tuned-and-cannot-be-used'
  | 'pipeline-error-eleven-labs-voice-not-allowed-for-free-users'
  | 'pipeline-error-eleven-labs-500-server-error'
  | 'pipeline-error-eleven-labs-max-character-limit-exceeded'
  | 'pipeline-error-playht-request-timed-out'
  | 'pipeline-error-playht-invalid-voice'
  | 'pipeline-error-playht-unexpected-error'
  | 'pipeline-error-playht-out-of-credits'
  | 'pipeline-error-playht-voice-must-be-a-valid-voice-manifest-uri'
  | 'pipeline-error-playht-401-unauthorized'
  | 'pipeline-error-playht-403-forbidden-out-of-characters'
  | 'pipeline-error-playht-403-forbidden-api-access-not-available'
  | 'pipeline-error-playht-429-exceeded-quota'
  | 'pipeline-error-playht-502-gateway-error'
  | 'pipeline-error-playht-504-gateway-error'
  | 'pipeline-error-deepgram-403-model-access-denied'
  | 'pipeline-error-deepgram-404-not-found'
  | 'pipeline-error-deepgram-400-no-such-model-language-tier-combination'
  | 'pipeline-error-deepgram-500-returning-invalid-json'
  | 'sip-gateway-failed-to-connect-call'
  | 'silence-timed-out'
  | 'twilio-failed-to-connect-call'
  | 'twilio-reported-customer-misdialed'
  | 'voicemail'
  | 'vonage-rejected';

// In the file where EndedReason is declared (e.g., '@/types/_dashboard/campaign')

// Create an array of EndedReason values
export const endedReasonValues: EndedReason[] = [
  'assistant-error',
  'assistant-not-found',
  'db-error',
  'no-server-available',
  'license-check-failed',
  'pipeline-error-openai-llm-failed',
  'pipeline-error-azure-openai-llm-failed',
  'pipeline-error-groq-llm-failed',
  'pipeline-error-anthropic-llm-failed',
  'pipeline-error-vapi-llm-failed',
  'pipeline-error-vapi-401-unauthorized',
  'pipeline-error-vapi-403-model-access-denied',
  'pipeline-error-vapi-429-exceeded-quota',
  'pipeline-error-vapi-500-server-error',
  'pipeline-error-openai-voice-failed',
  'pipeline-error-cartesia-voice-failed',
  'pipeline-error-deepgram-transcriber-failed',
  'pipeline-error-deepgram-voice-failed',
  'pipeline-error-gladia-transcriber-failed',
  'pipeline-error-eleven-labs-voice-failed',
  'pipeline-error-playht-voice-failed',
  'pipeline-error-lmnt-voice-failed',
  'pipeline-error-azure-voice-failed',
  'pipeline-error-rime-ai-voice-failed',
  'pipeline-error-neets-voice-failed',
  'pipeline-no-available-model',
  'worker-shutdown',
  'unknown-error',
  'vonage-disconnected',
  'vonage-failed-to-connect-call',
  'phone-call-provider-bypass-enabled-but-no-call-received',
  'vapifault-phone-call-worker-setup-socket-error',
  'vapifault-phone-call-worker-worker-setup-socket-timeout',
  'vapifault-phone-call-worker-could-not-find-call',
  'vapifault-transport-never-connected',
  'vapifault-web-call-worker-setup-failed',
  'vapifault-transport-connected-but-call-not-active',
  'assistant-not-invalid',
  'assistant-not-provided',
  'call-start-error-neither-assistant-nor-server-set',
  'assistant-request-failed',
  'assistant-request-returned-error',
  'assistant-request-returned-unspeakable-error',
  'assistant-request-returned-invalid-assistant',
  'assistant-request-returned-no-assistant',
  'assistant-request-returned-forwarding-phone-number',
  'assistant-ended-call',
  'assistant-said-end-call-phrase',
  'assistant-forwarded-call',
  'assistant-join-timed-out',
  'customer-busy',
  'customer-ended-call',
  'customer-did-not-answer',
  'customer-did-not-give-microphone-permission',
  'assistant-said-message-with-end-call-enabled',
  'exceeded-max-duration',
  'manually-canceled',
  'phone-call-provider-closed-websocket',
  'pipeline-error-openai-401-unauthorized',
  'pipeline-error-openai-403-model-access-denied',
  'pipeline-error-openai-429-exceeded-quota',
  'pipeline-error-openai-500-server-error',
  'pipeline-error-azure-openai-401-unauthorized',
  'pipeline-error-azure-openai-403-model-access-denied',
  'pipeline-error-azure-openai-429-exceeded-quota',
  'pipeline-error-azure-openai-500-server-error',
  'pipeline-error-groq-401-unauthorized',
  'pipeline-error-groq-403-model-access-denied',
  'pipeline-error-groq-429-exceeded-quota',
  'pipeline-error-groq-500-server-error',
  'pipeline-error-anthropic-401-unauthorized',
  'pipeline-error-anthropic-403-model-access-denied',
  'pipeline-error-anthropic-429-exceeded-quota',
  'pipeline-error-anthropic-500-server-error',
  'pipeline-error-together-ai-401-unauthorized',
  'pipeline-error-together-ai-403-model-access-denied',
  'pipeline-error-together-ai-429-exceeded-quota',
  'pipeline-error-together-ai-500-server-error',
  'pipeline-error-together-ai-llm-failed',
  'pipeline-error-anyscale-401-unauthorized',
  'pipeline-error-anyscale-403-model-access-denied',
  'pipeline-error-anyscale-429-exceeded-quota',
  'pipeline-error-anyscale-500-server-error',
  'pipeline-error-anyscale-llm-failed',
  'pipeline-error-openrouter-401-unauthorized',
  'pipeline-error-openrouter-403-model-access-denied',
  'pipeline-error-openrouter-429-exceeded-quota',
  'pipeline-error-openrouter-500-server-error',
  'pipeline-error-openrouter-llm-failed',
  'pipeline-error-perplexity-ai-401-unauthorized',
  'pipeline-error-perplexity-ai-403-model-access-denied',
  'pipeline-error-perplexity-ai-429-exceeded-quota',
  'pipeline-error-perplexity-ai-500-server-error',
  'pipeline-error-perplexity-ai-llm-failed',
  'pipeline-error-deepinfra-401-unauthorized',
  'pipeline-error-deepinfra-403-model-access-denied',
  'pipeline-error-deepinfra-429-exceeded-quota',
  'pipeline-error-deepinfra-500-server-error',
  'pipeline-error-deepinfra-llm-failed',
  'pipeline-error-runpod-401-unauthorized',
  'pipeline-error-runpod-403-model-access-denied',
  'pipeline-error-runpod-429-exceeded-quota',
  'pipeline-error-runpod-500-server-error',
  'pipeline-error-runpod-llm-failed',
  'pipeline-error-custom-llm-401-unauthorized',
  'pipeline-error-custom-llm-403-model-access-denied',
  'pipeline-error-custom-llm-429-exceeded-quota',
  'pipeline-error-custom-llm-500-server-error',
  'pipeline-error-custom-llm-llm-failed',
  'pipeline-error-cartesia-socket-hang-up',
  'pipeline-error-cartesia-requested-payment',
  'pipeline-error-cartesia-500-server-error',
  'pipeline-error-cartesia-522-server-error',
  'pipeline-error-eleven-labs-voice-not-found',
  'pipeline-error-eleven-labs-quota-exceeded',
  'pipeline-error-eleven-labs-unauthorized-access',
  'pipeline-error-eleven-labs-unauthorized-to-access-model',
  'pipeline-error-eleven-labs-professional-voices-only-for-creator-plus',
  'pipeline-error-eleven-labs-blocked-free-plan-and-requested-upgrade',
  'pipeline-error-eleven-labs-blocked-concurrent-requests-and-requested-upgrade',
  'pipeline-error-eleven-labs-blocked-using-instant-voice-clone-and-requested-upgrade',
  'pipeline-error-eleven-labs-system-busy-and-requested-upgrade',
  'pipeline-error-eleven-labs-voice-not-fine-tuned',
  'pipeline-error-eleven-labs-invalid-api-key',
  'pipeline-error-eleven-labs-invalid-voice-samples',
  'pipeline-error-eleven-labs-voice-disabled-by-owner',
  'pipeline-error-eleven-labs-blocked-account-in-probation',
  'pipeline-error-eleven-labs-blocked-content-against-their-policy',
  'pipeline-error-eleven-labs-missing-samples-for-voice-clone',
  'pipeline-error-eleven-labs-voice-not-fine-tuned-and-cannot-be-used',
  'pipeline-error-eleven-labs-voice-not-allowed-for-free-users',
  'pipeline-error-eleven-labs-500-server-error',
  'pipeline-error-eleven-labs-max-character-limit-exceeded',
  'pipeline-error-playht-request-timed-out',
  'pipeline-error-playht-invalid-voice',
  'pipeline-error-playht-unexpected-error',
  'pipeline-error-playht-out-of-credits',
  'pipeline-error-playht-voice-must-be-a-valid-voice-manifest-uri',
  'pipeline-error-playht-401-unauthorized',
  'pipeline-error-playht-403-forbidden-out-of-characters',
  'pipeline-error-playht-403-forbidden-api-access-not-available',
  'pipeline-error-playht-429-exceeded-quota',
  'pipeline-error-playht-502-gateway-error',
  'pipeline-error-playht-504-gateway-error',
  'pipeline-error-deepgram-403-model-access-denied',
  'pipeline-error-deepgram-404-not-found',
  'pipeline-error-deepgram-400-no-such-model-language-tier-combination',
  'pipeline-error-deepgram-500-returning-invalid-json',
  'sip-gateway-failed-to-connect-call',
  'silence-timed-out',
  'twilio-failed-to-connect-call',
  'twilio-reported-customer-misdialed',
  'voicemail',
  'vonage-rejected'
] as const;
