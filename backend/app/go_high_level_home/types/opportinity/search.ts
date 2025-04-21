// Types for Search Opportunities
export type SearchOpportunitiesQueryParams = {
  assigned_to?: string;
  campaignId?: string;
  contact_id?: string;
  country?: string;
  date?: string;
  endDate?: string;
  getCalendarEvents?: boolean;
  getNotes?: boolean;
  getTasks?: boolean;
  id?: string;
  limit?: number;
  order?: string;
  page?: number;
  pipeline_id?: string;
  pipeline_stage_id?: string;
  q?: string;
  startAfter?: string;
  startAfterId?: string;
  status?: string;
  location_id: string; // Required
};

export type SearchOpportunitiesResponse = {
  opportunities: {
    id: string;
    name: string;
    monetaryValue: number;
    pipelineId: string;
    pipelineStageId: string;
    assignedTo: string;
    status: string;
    source: string;
    lastStatusChangeAt: string;
    lastStageChangeAt: string;
    lastActionDate: string;
    indexVersion: string;
    createdAt: string;
    updatedAt: string;
    contactId: string;
    locationId: string;
    contact: {
      id: string;
      name: string;
      companyName: string;
      email: string;
      phone: string;
      tags: string[];
    };
    notes: string[];
    tasks: string[];
    calendarEvents: string[];
    customFields: {
      id: string;
      fieldValue: string;
    }[];
    followers: any[];
  }[];
  meta: {
    total: number;
    nextPageUrl: string;
    startAfterId: string;
    startAfter: number;
    currentPage: number;
    nextPage: number;
    prevPage: number;
  };
  aggregations: object;
};

// Types for Get Pipelines
export type GetPipelinesResponse = {
  pipelines: {
    id: string;
    name: string;
    stages: any[][];
    showInFunnel: boolean;
    showInPieChart: boolean;
    locationId: string;
  }[];
};

// Types for Add Followers
export type AddFollowersRequest = {
  followers: string[];
};

export type AddFollowersResponse = {
  followers: string[];
  followersAdded: string[];
};

// Types for Remove Followers
export type RemoveFollowersRequest = {
  followers: string[];
};

export type RemoveFollowersResponse = {
  followers: string[];
  followersRemoved: string[];
};
