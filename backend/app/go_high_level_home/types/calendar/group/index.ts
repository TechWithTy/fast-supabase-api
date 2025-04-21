// Common Types
export interface CalendarGroup {
  locationId: string;
  name: string;
  description: string;
  slug: string;
  isActive?: boolean;
  id?: string;
}

// Request and Response Types
export interface GetGroupsQueryParams {
  locationId: string; // Required
}

export interface CreateGroupRequest extends CalendarGroup {}

export interface UpdateGroupRequest {
  name: string;
  description: string;
  slug: string;
}

export interface ValidateGroupSlugRequest {
  locationId: string;
  slug: string;
}

export interface DisableGroupRequest {
  isActive: boolean;
}

// Response Types
export interface GetGroupsResponse {
  groups: CalendarGroup[];
}

export interface CreateOrUpdateGroupResponse {
  group: CalendarGroup;
}

export interface ValidateGroupSlugResponse {
  available: boolean;
}

export interface DeleteGroupResponse {
  success: boolean;
}
