// Permissions structure
export type UserPermissions = {
  campaignsEnabled?: boolean;
  campaignsReadOnly?: boolean;
  contactsEnabled?: boolean;
  workflowsEnabled?: boolean;
  workflowsReadOnly?: boolean;
  triggersEnabled?: boolean;
  funnelsEnabled?: boolean;
  websitesEnabled?: boolean;
  opportunitiesEnabled?: boolean;
  dashboardStatsEnabled?: boolean;
  bulkRequestsEnabled?: boolean;
  appointmentsEnabled?: boolean;
  reviewsEnabled?: boolean;
  onlineListingsEnabled?: boolean;
  phoneCallEnabled?: boolean;
  conversationsEnabled?: boolean;
  assignedDataOnly?: boolean;
  adwordsReportingEnabled?: boolean;
  membershipEnabled?: boolean;
  facebookAdsReportingEnabled?: boolean;
  attributionsReportingEnabled?: boolean;
  settingsEnabled?: boolean;
  tagsEnabled?: boolean;
  leadValueEnabled?: boolean;
  marketingEnabled?: boolean;
  agentReportingEnabled?: boolean;
  botService?: boolean;
  socialPlanner?: boolean;
  bloggingEnabled?: boolean;
  invoiceEnabled?: boolean;
  affiliateManagerEnabled?: boolean;
  contentAiEnabled?: boolean;
  refundsEnabled?: boolean;
  recordPaymentEnabled?: boolean;
  cancelSubscriptionEnabled?: boolean;
  paymentsEnabled?: boolean;
  communitiesEnabled?: boolean;
  exportPaymentsEnabled?: boolean;
};

// Request body for creating a user
export type CreateUserRequest = {
  companyId: string;
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  phone?: string;
  type: string;
  role: string;
  locationIds: string[];
  permissions: UserPermissions;
  scopes?: string[];
  scopesAssignedToOnly?: string[];
  profilePhoto?: string;
};

export type ghlUser = {
  id: string;
  name: string;
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  extension?: string;
  permissions: UserPermissions;
  roles: {
    type: string;
    role: string;
    locationIds: string[];
  };
  deleted: boolean;
};
// Request body for updating a user
export type UpdateUserRequest = CreateUserRequest & {
  emailChangeOTP?: string;
};

// Response types
export type GetUserResponse = {
  users: ghlUser[];
};

export type CreateUserResponse = ghlUser;

export type UpdateUserResponse = ghlUser;

export type DeleteUserResponse = {
  succeeded: boolean;
  message: string;
};
