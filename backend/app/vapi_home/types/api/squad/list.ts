// types/vapiAi/api/squad/list.ts

// Query parameters for listing squads
export interface ListSquadsQueryParams {
  limit?: number; // Optional limit for the number of squads to return
  createdAtGt?: string; // Optional: squads created after this date
  createdAtLt?: string; // Optional: squads created before this date
  createdAtGe?: string; // Optional: squads created on or after this date
  createdAtLe?: string; // Optional: squads created on or before this date
  updatedAtGt?: string; // Optional: squads updated after this date
  updatedAtLt?: string; // Optional: squads updated before this date
  updatedAtGe?: string; // Optional: squads updated on or after this date
  updatedAtLe?: string; // Optional: squads updated on or before this date
}

// Response type for squad members (reusing SquadMember from another file if it exists)
export interface SquadMember {
  assistantId: string;
  assistant: Record<string, any>; // Details for each assistant
  assistantOverrides?: Record<string, any>; // Optional overrides
}

// Response type for listing squads
export interface ListSquadsResponse {
  squads: {
    id: string;
    name: string;
    members: SquadMember[];
    createdAt: string; // ISO 8601 date-time string of creation
    updatedAt: string; // ISO 8601 date-time string of last update
    membersOverrides?: Partial<SquadMember>; // Optional member overrides
  }[];
}
