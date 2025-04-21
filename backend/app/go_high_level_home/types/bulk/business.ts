// Request body for adding/removing contacts from business
export type BulkBusinessRequest = {
  locationId: string;
  ids: string[];
  businessId: string | null;
};

// Response type for adding/removing contacts from business
export type BulkBusinessResponse = {
  success: boolean;
  ids: string[];
};
