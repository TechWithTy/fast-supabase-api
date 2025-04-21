// Types for the Get Opportunity endpoint
export type GetOpportunityResponse = {
  opportunity: {
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
    followers: any[]; // Adjust the type if more information is known about followers
  };
};

// Types for the Create Opportunity endpoint
export type CreateOpportunityRequest = {
  pipelineId: string;
  locationId: string;
  name: string;
  pipelineStageId: string;
  status: string;
  contactId: string;
  monetaryValue?: number;
  assignedTo?: string;
  customFields?: {
    id?: string;
    key?: string;
    field_value: string;
  }[];
};

export type CreateOpportunityResponse = {
  opportunity: {
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
  };
};

// Types for the Update Opportunity endpoint
export type UpdateOpportunityRequest = {
  pipelineId?: string;
  name?: string;
  pipelineStageId?: string;
  status?: string;
  monetaryValue?: number;
  assignedTo?: string;
  customFields?: {
    id?: string;
    key?: string;
    field_value: string;
  }[];
};

export type UpdateOpportunityResponse = GetOpportunityResponse;

// Types for the Delete Opportunity endpoint
export type DeleteOpportunityResponse = {
  succeeded: boolean;
};

// Types for the Upsert Opportunity endpoint
export type UpsertOpportunityRequest = CreateOpportunityRequest;

export type UpsertOpportunityResponse = {
  opportunity: CreateOpportunityResponse['opportunity'];
  new: boolean;
};

// Types for the Update Opportunity Status endpoint
export type UpdateOpportunityStatusRequest = {
  status: string;
};

export type UpdateOpportunityStatusResponse = {
  succeeded: boolean;
};
