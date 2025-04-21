export type FunnelStep = {
  id: string; // Step ID
  name: string; // Name of the step
  originId: string; // Origin ID of the step
  pages: string[]; // Array of page IDs
  products: string[]; // Array of product IDs (if any)
  sequence: number; // Sequence order of the step
  type: string; // Type of the funnel step (e.g., "optin_funnel_page")
  url: string; // URL of the funnel step
};

export type Funnel = {
  _id: string; // Funnel ID
  dateAdded: string; // Date the funnel was added (ISO string)
  dateUpdated: string; // Date the funnel was last updated (ISO string)
  deleted: boolean; // Boolean indicating if the funnel is deleted
  domainId?: string; // Domain ID (optional)
  locationId: string; // Location ID
  name: string; // Name of the funnel
  orderFormVersion: number; // Version of the order form
  originId: string; // Origin ID of the funnel
  steps: FunnelStep[]; // Array of steps associated with the funnel
  type: string; // Type of the funnel (e.g., "funnel")
  updatedAt: string; // Last update date (ISO string)
  faviconUrl?: string; // Optional URL of the favicon
  globalSectionVersion: number; // Global section version number
  globalSectionsPath: string; // Path to the global sections
  globalSectionsUrl: string; // URL to the global sections
  isStoreActive: boolean; // Boolean indicating if the store is active
  trackingCodeBody?: string; // Optional tracking code for the body
  trackingCodeHead?: string; // Optional tracking code for the head
  url: string; // URL of the funnel
};

export type GetFunnelsResponse = {
  funnels: Funnel; // The funnel object returned
  count: number; // Total number of funnels returned
  traceId: string; // Trace ID for tracking the request
};

export type FunnelPage = {
  _id: string; // Funnel page ID
  locationId: string; // Location ID
  funnelId: string; // ID of the funnel the page belongs to
  name: string; // Name of the funnel page
  stepId: string; // Step ID associated with this page
  deleted: boolean; // Whether the page is marked as deleted
  updatedAt: string; // Last updated timestamp (ISO string)
};

export type GetFunnelPagesResponse = {
  pages: FunnelPage[]; // Array of funnel pages returned
  count: number; // Total number of pages returned
  traceId: string; // Trace ID for tracking the request
};

export type GetFunnelCountResponse = {
  count: number; // The total count of funnel pages
};

export const exampleGetFunnelsResponse: GetFunnelsResponse = {
  funnels: {
    _id: 'SkIDfu0S4m3NYQyvWHC6',
    dateAdded: '2024-04-29T15:00:05.681Z',
    dateUpdated: '2024-04-29T15:00:28.465Z',
    deleted: false,
    domainId: '',
    locationId: 'ojQjykmwNIU88vfsfzvH',
    name: 'Chaitanya Copy',
    orderFormVersion: 2,
    originId: 'hAmyh7jrJH5FfEEKAJ9z',
    steps: [
      {
        id: 'f5d178c0-8bbb-4cd4-927c-691c68a62c59',
        name: 'Step 1',
        originId: '80b2f227-5bc8-4ca5-980d-817745ea4e8b',
        pages: ['2IhBmBcQRx9JXV1JZsRt'],
        products: [],
        sequence: 1,
        type: 'optin_funnel_page',
        url: '/newtestifypath'
      }
    ],
    type: 'funnel',
    updatedAt: '2024-04-29T15:00:34.233Z',
    faviconUrl: '',
    globalSectionVersion: 1,
    globalSectionsPath: 'funnel/SkIDfu0S4m3NYQyvWHC6/global-sections-1',
    globalSectionsUrl:
      'https://firebasestorage.googleapis.com/v0/b/highlevel-staging.appspot.com/o/funnel%2FSkIDfu0S4m3NYQyvWHC6%2Fglobal-sections-1?alt=media&token=9cc5c211-093b-4751-aeba-19282ac92955',
    isStoreActive: false,
    trackingCodeBody: '',
    trackingCodeHead: '',
    url: '/chaitanya'
  },
  count: 24,
  traceId: '03774d31-a57e-4b4f-95c7-315ce61969f1'
};

export const exampleGetFunnelPagesResponse: GetFunnelPagesResponse = {
  pages: [
    {
      _id: '0yJbP3q7t7pLmeTWRAE2',
      locationId: 'ojQjykmwNIU88vfsfzvH',
      funnelId: 'iucJ6TdFZiddhq9f6znh',
      name: 'Home',
      stepId: '343bf634-3aa6-4ade-b963-2d3cd0bf2ede',
      deleted: false,
      updatedAt: '2024-04-18T12:25:23.029Z'
    }
  ],
  count: 1,
  traceId: '123e4567-e89b-12d3-a456-426614174000'
};

export const exampleGetFunnelCountResponse: GetFunnelCountResponse = {
  count: 20
};
