// Types for Tag Responses
export interface Tag {
  id: string;
  name: string;
  locationId: string;
}

export interface GetTagsResponse {
  tags: Tag[];
}

export interface GetTagResponse {
  tag: Tag;
}

export interface CreateOrUpdateTagRequest {
  name: string;
}
