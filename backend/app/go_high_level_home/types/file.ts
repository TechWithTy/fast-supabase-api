export type GHLFile = {
  altId: string; // Maps to locationId
  altType: 'location'; // Denotes the type as 'location', fixed value
  name: string; // File name
  parentId?: string; // Optional parent folder ID
  url: string; // File URL
  path: string; // File path
};

export const exampleFile: GHLFile = {
  altId: 'locationId',
  altType: 'location',
  name: 'file name',
  parentId: 'parent folder id',
  url: 'file url',
  path: 'file path'
};
