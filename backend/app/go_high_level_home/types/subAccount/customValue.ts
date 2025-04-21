// Types for Custom Value
export interface CustomValue {
  id: string;
  name: string;
  fieldKey: string;
  value: string;
  locationId: string;
}

// Types for Create/Update Custom Value Request
export interface CustomValueRequest {
  name: string;
  value: string;
}

// Response Types
export interface CustomValueResponse {
  customValue: CustomValue;
}

export interface GetCustomValuesResponse {
  customValues: CustomValue[];
}
