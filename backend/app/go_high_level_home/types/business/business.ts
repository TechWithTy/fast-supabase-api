export type Business = {
  id: string; // Business ID
  name: string; // Business Name
  phone?: string; // Optional phone number
  email?: string; // Optional email
  website?: string; // Optional website URL
  address?: string; // Optional address
  city?: string; // Optional city
  description?: string; // Optional business description
  state?: string; // Optional state
  postalCode?: string; // Optional postal code
  country?: string; // Optional country
  updatedBy?: object; // Optional object representing who updated the business
  locationId: string; // Required location ID
  createdBy?: object; // Optional object representing who created the business
  createdAt: string; // ISO date-time for when the business was created
  updatedAt: string; // ISO date-time for the last update of the business
};

export type GetBusinessResponse = {
  business: Business; // The business object returned in the response
};

export const exampleGetBusinessResponse: GetBusinessResponse = {
  business: {
    id: '63771dcac1116f0e21de8e12',
    name: 'Microsoft',
    phone: 'string',
    email: 'abc@microsoft.com',
    website: 'microsoft.com',
    address: 'string',
    city: 'string',
    description: 'string',
    state: 'string',
    postalCode: 'string',
    country: 'united states',
    updatedBy: {},
    locationId: 'string',
    createdBy: {},
    createdAt: '2019-08-24T14:15:22Z',
    updatedAt: '2019-08-24T14:15:22Z'
  }
};
