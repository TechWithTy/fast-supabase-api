// Types for Get List of Files
export interface GetFilesQueryParams {
  limit?: string;
  offset?: string;
  query?: string;
  type?: string;
  altId: string; // Required
  altType: 'agency' | 'location'; // Required
  sortBy: string; // Required
  sortOrder: 'asc' | 'desc'; // Required
}

export interface FileObject {
  altId: string;
  altType: string;
  name: string;
  parentId?: string;
  url: string;
  path: string;
}

export interface GetFilesResponse {
  files: FileObject[];
}

// Types for Upload File
export interface UploadFileRequest {
  file?: Blob; // When using multipart/form-data
  hosted?: boolean;
  fileUrl?: string;
  name: string;
}

export interface UploadFileResponse {
  fileId: string;
}

// Types for Delete File or Folder
export interface DeleteFileOrFolderQueryParams {
  altId: string; // Required
  altType: 'agency' | 'location'; // Required
}

export interface DeleteFileResponse {
  success: boolean;
}
