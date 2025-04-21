import { EndedReason } from '@/types/vapiAi/api/calls/_enums';

// Define a generic custom field type for receiving custom fields in the response
export type ContactCustomField = {
  id: string; // Unique ID of the custom field
  value: any; // The value of the custom field (can be string, number, etc.)
};

// Define a type for custom fields when updating
export type UpdateCustomField = {
  id: string; // Unique ID of the custom field
  key: string; // The key or name of the custom field
  field_value: any; // The new value for the custom field
};

// Define a generic custom field type for specific custom fields in ExtendedContact
export type CustomField<T> = {
  optionName: T; // Value of the field (this can be used for display purposes)
  uniqueKey: string; // Unique key associated with the custom field (same as in GHL)
  id?: string; // Optional ID for updating existing fields
};

// Define custom field types for each specific field with their respective unique keys
export type PropertyIDField = CustomField<string> & {
  uniqueKey: 'property_id';
};
export type AgentNameField = CustomField<string> & { uniqueKey: 'agent_name' };
export type AgentMainPhoneField = CustomField<string> & {
  uniqueKey: 'agent_main_phone';
};
export type PropertyAltPhotosField = CustomField<string[]> & {
  uniqueKey: 'property_alt_photos';
};
export type AddressedValueField = CustomField<number> & {
  uniqueKey: 'addressed_value';
};
export type PropertyBedsField = CustomField<number> & {
  uniqueKey: 'property_beds';
};
export type BrokerNameField = CustomField<string> & {
  uniqueKey: 'broker_name';
};
export type BrokerPhoneField = CustomField<string> & {
  uniqueKey: 'broker_phone';
};
export type BrokerWebsiteField = CustomField<string> & {
  uniqueKey: 'broker_website';
};
export type PropertyCityField = CustomField<string> & {
  uniqueKey: 'property_city';
};
export type PropertyCountyField = CustomField<string> & {
  uniqueKey: 'property_county';
};
export type DaysOnMLSField = CustomField<number> & { uniqueKey: 'days_on_mls' };
export type EstimatedValueField = CustomField<number> & {
  uniqueKey: 'estimated_value';
};
export type FipsCodeField = CustomField<number> & { uniqueKey: 'fips_code' };
export type FullBathsField = CustomField<number> & { uniqueKey: 'full_baths' };
export type FullStreetAddressField = CustomField<string> & {
  uniqueKey: 'full_street_address';
};
export type HalfBathsField = CustomField<number> & { uniqueKey: 'half_baths' };
export type HoaFeeField = CustomField<number> & { uniqueKey: 'hoa_fee' };
export type LastSaleDateField = CustomField<string> & {
  uniqueKey: 'last_sale_date';
}; // Store as string (ISO format)
export type LatitudeField = CustomField<number> & { uniqueKey: 'latitude' };
export type ListDateField = CustomField<string> & { uniqueKey: 'list_date' }; // Store as string (ISO format)
export type ListPriceField = CustomField<number> & { uniqueKey: 'list_price' };
export type LongitudeField = CustomField<number> & { uniqueKey: 'longitude' };
export type LotSqftField = CustomField<number> & { uniqueKey: 'lot_sqft' };
export type MLSField = CustomField<string> & { uniqueKey: 'mls' };
export type NearbySchoolsField = CustomField<string[]> & {
  uniqueKey: 'nearby_schools';
}; // Array for multiple entries
export type MLSIDField = CustomField<string> & { uniqueKey: 'mls_id' };
export type NeighborhoodsField = CustomField<string[]> & {
  uniqueKey: 'neighborhoods';
}; // Array for multiple entries
export type ParkingGarageField = CustomField<'Yes' | 'No'> & {
  uniqueKey: 'parking_garage';
}; // Example values
export type PricePerSqftField = CustomField<number> & {
  uniqueKey: 'price_per_sqft';
};
export type PrimaryPhotoField = CustomField<string> & {
  uniqueKey: 'primary_photo';
}; // URL for the photo
export type PropertyURLField = CustomField<string> & {
  uniqueKey: 'property_url';
};
export type SoldPriceField = CustomField<number> & { uniqueKey: 'sold_price' };
export type SqftField = CustomField<number> & { uniqueKey: 'sqft' };
export type StatusField = CustomField<string> & { uniqueKey: 'status' };
export type StoriesField = CustomField<number> & { uniqueKey: 'stories' };
export type PropertyStreetField = CustomField<string> & {
  uniqueKey: 'property_street';
};
export type PropertyStateField = CustomField<string> & {
  uniqueKey: 'property_state';
};
export type PropertyStyleField = CustomField<string> & {
  uniqueKey: 'property_style';
};
export type MLSDescriptionField = CustomField<string> & {
  uniqueKey: 'mls_description';
}; // Large text
export type UnitField = CustomField<string> & { uniqueKey: 'unit' };
export type YearBuiltField = CustomField<number> & { uniqueKey: 'year_built' };
export type PropertyZipCodeField = CustomField<number> & {
  uniqueKey: 'property_zip_code';
};

// Define custom field types for social profiles
export type FacebookProfileField = CustomField<string> & {
  uniqueKey: 'facebook_profile';
};
export type InstagramProfileField = CustomField<string> & {
  uniqueKey: 'instagram_profile';
};

// Define custom options types
export type CustomDndOption = {
  optionName: 'Email' | 'Phone' | 'Social' | 'Text';
  uniqueKey: 'custom_dnd';
};

export type CallOutcomeOption = {
  optionName: EndedReason;
  uniqueKey: 'call_outcome';
};

// Define the structure for custom options in contacts
export type CustomOptions = {
  facebook_profile?: FacebookProfileField;
  instagram_profile?: InstagramProfileField;
  custom_dnd?: CustomDndOption;
  call_outcome?: CallOutcomeOption;
};
