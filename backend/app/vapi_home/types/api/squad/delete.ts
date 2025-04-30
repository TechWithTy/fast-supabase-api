// types/vapiAi/api/squad/delete.ts

export interface DeleteSquadResponse {
  id: string; // Unique identifier of the squad
  name: string; // Name of the squad
  members: {
    assistantId: string;
    assistant: Record<string, any>;
  }[];
  membersOverrides?: Record<string, any>; // Optional overrides for all members
  orgId: string; // Organization ID the squad belongs to
  createdAt: string; // When the squad was created (ISO 8601 date-time)
  updatedAt: string; // When the squad was last updated (ISO 8601 date-time)
}
