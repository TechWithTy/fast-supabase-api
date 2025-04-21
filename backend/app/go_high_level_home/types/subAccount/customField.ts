// Types for Custom Field
export interface CustomField {
  id: string;
  name: string;
  fieldKey: string;
  placeholder: string;
  dataType: string;
  position: number;
  picklistOptions?: string[];
  picklistImageOptions?: string[];
  isAllowedCustomOption?: boolean;
  isMultiFileAllowed?: boolean;
  maxFileLimit?: number;
  locationId: string;
  model: string;
}

// Types for Create/Update Custom Field Request
export interface CustomFieldRequest {
  name: string;
  dataType: string;
  placeholder?: string;
  acceptedFormat?: string[];
  isMultipleFile?: boolean;
  maxNumberOfFiles?: number;
  textBoxListOptions?: {
    label: string;
    prefillValue?: string;
    position?: number;
  }[];
  position?: number;
  model?: string;
}

// Response Types
export interface CustomFieldResponse {
  customField: CustomField;
}

export interface GetCustomFieldsResponse {
  customFields: CustomField[];
}

export interface UploadFileResponse {
  uploadedFiles: { [key: string]: string };
  meta: {
    fieldname: string;
    originalname: string;
    encoding: string;
    mimetype: string;
    size: number;
    url: string;
  }[];
}
