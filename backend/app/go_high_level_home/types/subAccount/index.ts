// Common Types
export interface SubAccount {
  id: string;
  companyId: string;
  name: string;
  domain?: string;
  address?: string;
  city?: string;
  state?: string;
  logoUrl?: string;
  country?: string;
  postalCode?: string;
  website?: string;
  timezone?: string;
  firstName?: string;
  lastName?: string;
  email?: string;
  phone?: string;
  business?: object;
  social?: object;
  settings?: object;
  reseller?: object;
}

export interface CreateOrUpdateSubAccountRequest {
  name: string;
  phone?: string;
  companyId: string;
  address?: string;
  city?: string;
  state?: string;
  country?: string;
  postalCode?: string;
  website?: string;
  timezone?: string;
  prospectInfo?: {
    firstName: string;
    lastName: string;
    email: string;
  };
  settings?: {
    allowDuplicateContact?: boolean;
    allowDuplicateOpportunity?: boolean;
    allowFacebookNameMerge?: boolean;
    disableContactTimezone?: boolean;
  };
  social?: {
    facebookUrl?: string;
    googlePlus?: string;
    linkedIn?: string;
    foursquare?: string;
    twitter?: string;
    yelp?: string;
    instagram?: string;
    youtube?: string;
    pinterest?: string;
    blogRss?: string;
    googlePlacesId?: string;
  };
  twilio?: {
    sid: string;
    authToken: string;
  };
  mailgun?: {
    apiKey: string;
    domain: string;
  };
  snapshotId?: string;
}

export interface DeleteSubAccountResponse {
  success: boolean;
  message: string;
}
