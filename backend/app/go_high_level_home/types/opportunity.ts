export type OpportunityResponse = {
  opportunity: {
    id: string; // Required, Opportunity Id
    name: string; // Name of the opportunity
    monetaryValue: number; // The monetary value of the opportunity
    pipelineId: string; // Pipeline Id
    pipelineStageId: string; // Pipeline Stage Id
    assignedTo: string; // ID of the person assigned to the opportunity
    status: string; // Status of the opportunity (e.g., open, closed)
    source?: string; // Source of the opportunity, optional
    lastStatusChangeAt: string; // ISO date of last status change
    lastStageChangeAt: string; // ISO date of last stage change
    lastActionDate: string; // ISO date of the last action
    indexVersion: number; // Index version number
    createdAt: string; // ISO date of creation
    updatedAt: string; // ISO date of last update
    contactId: string; // Contact Id related to the opportunity
    locationId: string; // Location Id related to the opportunity
    contact: {
      id: string; // Contact Id
      name: string; // Name of the contact
      companyName?: string; // Company name, optional
      email: string; // Contact email
      phone: string; // Contact phone number
      tags?: string[]; // Optional array of tags associated with the contact
    };
    notes?: string[]; // Optional array of notes
    tasks?: string[]; // Optional array of tasks
    calendarEvents?: string[]; // Optional array of calendar events
    customFields?: {
      id: string; // Custom field Id
      fieldValue: string; // Value of the custom field
    }[];
    followers?: any[][]; // Nested array for followers
  };
};

export const exampleOpportunityResponse: OpportunityResponse = {
  opportunity: {
    id: 'yWQobCRIhRguQtD2llvk',
    name: 'testing',
    monetaryValue: 500,
    pipelineId: 'VDm7RPYC2GLUvdpKmBfC',
    pipelineStageId: 'e93ba61a-53b3-45e7-985a-c7732dbcdb69',
    assignedTo: 'zT46WSCPbudrq4zhWMk6',
    status: 'open',
    source: '',
    lastStatusChangeAt: '2021-08-03T04:55:17.355Z',
    lastStageChangeAt: '2021-08-03T04:55:17.355Z',
    lastActionDate: '2021-08-03T04:55:17.355Z',
    indexVersion: 1,
    createdAt: '2021-08-03T04:55:17.355Z',
    updatedAt: '2021-08-03T04:55:17.355Z',
    contactId: 'zT46WSCPbudrq4zhWMk6',
    locationId: 'zT46WSCPbudrq4zhW',
    contact: {
      id: 'byMEV0NQinDhq8ZfiOi2',
      name: 'John Deo',
      companyName: 'Tesla Inc',
      email: 'john@deo.com',
      phone: '+1202-555-0107',
      tags: ['string']
    },
    notes: ['string'],
    tasks: ['string'],
    calendarEvents: ['string'],
    customFields: [
      {
        id: 'MgobCB14YMVKuE4Ka8p1',
        fieldValue: 'string'
      }
    ],
    followers: [[]]
  }
};
