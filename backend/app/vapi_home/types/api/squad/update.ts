// types/vapiAi/api/squad/update.ts

export interface UpdateSquadRequest {
  name?: string; // Optional, the name of the squad
  members?: {
    assistantId: string;
    assistant: Record<string, any>; // Assistant details
    assistantOverrides?: Record<string, any>; // Optional overrides for this assistant
  }[];
  membersOverrides?: Partial<{
    assistant: Record<string, any>;
    voice: Record<string, any>;
  }>;
}

// Response type for updating a squad (usually just reflects the updated squad)
export interface UpdateSquadResponse {
  id: string;
  name: string;
  members: {
    assistantId: string;
    assistant: Record<string, any>;
    assistantOverrides?: Record<string, any>;
  }[];
  membersOverrides?: Partial<Record<string, any>>;
  orgId: string;
  createdAt: string; // ISO 8601 date-time string
  updatedAt: string; // ISO 8601 date-time string
}
