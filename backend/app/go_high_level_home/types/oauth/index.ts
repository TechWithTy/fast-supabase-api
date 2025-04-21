export interface OAuthResponse {
  success: boolean;
  statusCode: number;
  message: string;
  results?: any;
}

export interface OAuthAccountDetails {
  accountId: string;
  locationId: string;
}

export interface OAuthStartResponse {
  actionType: string;
  page: string;
  platform: string;
  placement: string;
  accountId: string;
  reconnectAccounts: string[];
}

export interface AttachAccountRequest {
  originId: string;
  name: string;
  avatar: string;
  pageId?: string; // Optional for Instagram
  urn?: string; // Optional for LinkedIn
  companyId: string;
  type?: string; // Optional, varies per platform
}

export interface SetBusinessLocationRequest {
  location: object;
  account: object;
  companyId: string;
}

export interface AttachFacebookPageRequest {
  type: string;
  originId: string;
  name: string;
  avatar: string;
  companyId: string;
}
