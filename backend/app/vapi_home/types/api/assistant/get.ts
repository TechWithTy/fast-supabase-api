// Add specific types for the 'get assistant' response
export interface AssistantResponse extends CreateAssistantRequest {
  id: string; // The unique ID of the assistant
  orgId: string; // The organization ID that owns the assistant
  createdAt: string; // ISO timestamp of when the assistant was created
  updatedAt: string; // ISO timestamp of when the assistant was last updated
}
