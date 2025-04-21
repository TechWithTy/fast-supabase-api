import { SquadMember } from './create';

export interface GetSquadResponse {
  id: string; // Unique squad identifier
  name: string; // Name of the squad
  members: SquadMember[]; // Array of squad members
  createdAt: string; // ISO 8601 date-time when the squad was created
  updatedAt: string; // ISO 8601 date-time when the squad was last updated
  membersOverrides?: Partial<SquadMember>; // Optional overrides for all members
}
