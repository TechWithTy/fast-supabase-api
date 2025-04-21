import {
  PropertyIDField,
  AgentNameField,
  AgentMainPhoneField,
  PropertyAltPhotosField,
  AddressedValueField,
  PropertyBedsField,
  BrokerNameField,
  BrokerPhoneField,
  BrokerWebsiteField,
  PropertyCityField,
  PropertyCountyField,
  DaysOnMLSField,
  EstimatedValueField,
  FipsCodeField,
  FullBathsField,
  FullStreetAddressField,
  HalfBathsField,
  HoaFeeField,
  LastSaleDateField,
  LatitudeField,
  ListDateField,
  ListPriceField,
  LongitudeField,
  LotSqftField,
  MLSField,
  NearbySchoolsField,
  MLSIDField,
  NeighborhoodsField,
  ParkingGarageField,
  PricePerSqftField,
  PrimaryPhotoField,
  PropertyURLField,
  SoldPriceField,
  SqftField,
  StatusField,
  StoriesField,
  PropertyStreetField,
  PropertyStateField,
  PropertyStyleField,
  MLSDescriptionField,
  UnitField,
  YearBuiltField,
  PropertyZipCodeField,
  CustomOptions
} from './_enums';

export type DndSettings = {
  status: string; // DND status (e.g., "active")
  message: string; // DND message
  code: string; // DND code
};

export type ContactDndSettings = {
  Call: DndSettings;
  Email: DndSettings;
  SMS: DndSettings;
  WhatsApp: DndSettings;
  GMB: DndSettings;
  FB: DndSettings;
};

export type CustomField = {
  id: string; // Custom field ID
  value: string; // Custom field value
};

export type AttributionSource = {
  url: string; // Attribution source URL
  campaign: string; // Campaign name
  utmSource: string; // UTM Source
  utmMedium: string; // UTM Medium
  utmContent: string; // UTM Content
  referrer: string; // Referrer URL
  campaignId: string; // Campaign ID
  fbclid: string; // Facebook click ID
  gclid: string; // Google click ID
  msclikid: string; // Microsoft click ID
  dclid: string; // Display click ID
  fbc: string; // Facebook cookie
  fbp: string; // Facebook Pixel
  fbEventId: string; // Facebook event ID
  userAgent: string; // User agent
  ip: string; // IP address
  medium: string; // Medium
  mediumId: string; // Medium ID
};

export type Contact = {
  id: string; // Contact ID
  name: string; // Full name of the contact
  locationId: string; // Location ID
  firstName: string; // First name
  lastName: string; // Last name
  email: string; // Email address
  emailLowerCase: string; // Lowercase email address
  timezone: string; // Timezone
  companyName?: string; // Company name (optional)
  phone?: string; // Phone number (optional)
  dnd: boolean; // Do Not Disturb status
  dndSettings: ContactDndSettings; // DND settings object
  type: string; // Contact type (e.g., "read")
  source: string; // Source of the contact (e.g., "public api")
  assignedTo: string; // Assigned to user or location ID
  address1?: string; // Address line 1 (optional)
  city?: string; // City (optional)
  state?: string; // State (optional)
  country?: string; // Country code (optional)
  postalCode?: string; // Postal code (optional)
  website?: string; // Website URL (optional)
  tags: string[]; // Tags array
  dateOfBirth?: string; // Date of birth (ISO string)
  dateAdded: string; // Date added (ISO string)
  dateUpdated: string; // Date updated (ISO string)
  attachments?: string; // Attachments (optional)
  ssn?: string; // Social Security Number (optional)
  keyword?: string; // Keyword associated with the contact (optional)
  firstNameLowerCase: string; // Lowercase first name
  fullNameLowerCase: string; // Lowercase full name
  lastNameLowerCase: string; // Lowercase last name
  lastActivity?: string; // Last activity timestamp (ISO string, optional)
  customFields: CustomField[]; // Custom fields
  businessId: string; // Business ID
  attributionSource?: AttributionSource; // Attribution source (optional)
  lastAttributionSource?: AttributionSource; // Last attribution source (optional)
};

// Extend the Contact type to include the new custom fields and social profiles
export type ExtendedContact = Contact & {
  property_id?: PropertyIDField;
  agent_name?: AgentNameField;
  agent_main_phone?: AgentMainPhoneField;
  property_alt_photos?: PropertyAltPhotosField;
  addressed_value?: AddressedValueField;
  property_beds?: PropertyBedsField;
  broker_name?: BrokerNameField;
  broker_phone?: BrokerPhoneField;
  broker_website?: BrokerWebsiteField;
  property_city?: PropertyCityField;
  property_county?: PropertyCountyField;
  days_on_mls?: DaysOnMLSField;
  estimated_value?: EstimatedValueField;
  fips_code?: FipsCodeField;
  full_baths?: FullBathsField;
  full_street_address?: FullStreetAddressField;
  half_baths?: HalfBathsField;
  hoa_fee?: HoaFeeField;
  last_sale_date?: LastSaleDateField;
  latitude?: LatitudeField;
  list_date?: ListDateField;
  list_price?: ListPriceField;
  longitude?: LongitudeField;
  lot_sqft?: LotSqftField;
  mls?: MLSField;
  nearby_schools?: NearbySchoolsField;
  mls_id?: MLSIDField;
  neighborhoods?: NeighborhoodsField;
  parking_garage?: ParkingGarageField;
  price_per_sqft?: PricePerSqftField;
  primary_photo?: PrimaryPhotoField;
  property_url?: PropertyURLField;
  sold_price?: SoldPriceField;
  sqft?: SqftField;
  status?: StatusField;
  stories?: StoriesField;
  property_street?: PropertyStreetField;
  property_state?: PropertyStateField;
  property_style?: PropertyStyleField;
  mls_description?: MLSDescriptionField;
  unit?: UnitField;
  year_built?: YearBuiltField;
  property_zip_code?: PropertyZipCodeField;
  customOptions?: CustomOptions;
};
export type GetContactResponse = {
  contact: Contact | ExtendedContact; // Contact object returned in the response
};

export type GetContactPathParams = {
  contactId: string; // Required Contact ID
};

export type GetContactHeaders = {
  Authorization: string; // Bearer token for authorization
  Version: string; // API version (e.g., '2021-07-28')
};

export const exampleGetContactResponse: GetContactResponse = {
  contact: {
    id: 'seD4PfOuKoVMLkEZqohJ',
    name: 'rubika deo',
    locationId: 've9EPM428h8vShlRW1KT',
    firstName: 'rubika',
    lastName: 'Deo',
    email: 'rubika@deos.com',
    emailLowerCase: 'rubika@deos.com',
    timezone: '',
    companyName: 'DGS VolMAX',
    phone: '+18832327657',
    dnd: true,
    dndSettings: {
      Call: { status: 'active', message: 'string', code: 'string' },
      Email: { status: 'active', message: 'string', code: 'string' },
      SMS: { status: 'active', message: 'string', code: 'string' },
      WhatsApp: { status: 'active', message: 'string', code: 'string' },
      GMB: { status: 'active', message: 'string', code: 'string' },
      FB: { status: 'active', message: 'string', code: 'string' }
    },
    type: 'read',
    source: 'public api',
    assignedTo: 've9EPM428h8vShlRW1KT',
    address1: '3535 1st St N',
    city: 'ruDolomitebika',
    state: 'AL',
    country: 'US',
    postalCode: '35061',
    website: 'https://www.tesla.com',
    tags: ['nisi sint commodo amet', 'consequat'],
    dateOfBirth: '1990-09-25T00:00:00.000Z',
    dateAdded: '2021-07-02T05:18:26.704Z',
    dateUpdated: '2021-07-02T05:18:26.704Z',
    attachments: 'string',
    ssn: 'string',
    keyword: 'test',
    firstNameLowerCase: 'rubika',
    fullNameLowerCase: 'rubika deo',
    lastNameLowerCase: 'deo',
    lastActivity: '2021-07-16T11:39:30.564Z',
    customFields: [{ id: 'MgobCB14YMVKuE4Ka8p1', value: 'name' }],
    businessId: '641c094001436dbc2081e642',
    attributionSource: {
      url: 'Trigger Link',
      campaign: 'string',
      utmSource: 'string',
      utmMedium: 'string',
      utmContent: 'string',
      referrer: 'https: //www.google.com',
      campaignId: 'string',
      fbclid: 'string',
      gclid:
        'CjOKCQjwnNyUBhCZARISAI9AYIFtNnIcWcYGIOQINz_ZoFI5SSLRRugSoPZoiEu27IZBY£1-MAIWmEaAo2VEALW_WCB',
      msclikid: 'string',
      dclid: 'string',
      fbc: 'string',
      fbp: 'fb. 1.1674748390986.1171287961',
      fbEventId: 'Mozilla/5.0',
      userAgent: 'Mozilla/5.0',
      ip: '58.111.106.198',
      medium: 'survey',
      mediumId: 'FglfHAn30PRwsZVyQlKp'
    },
    lastAttributionSource: {
      url: 'Trigger Link',
      campaign: 'string',
      utmSource: 'string',
      utmMedium: 'string',
      utmContent: 'string',
      referrer: 'https: //www.google.com',
      campaignId: 'string',
      fbclid: 'string',
      gclid:
        'CjOKCQjwnNyUBhCZARISAI9AYIFtNnIcWcYGIOQINz_ZoFI5SSLRRugSoPZoiEu27IZBY£1-MAIWmEaAo2VEALW_WCB',
      msclikid: 'string',
      dclid: 'string',
      fbc: 'string',
      fbp: 'fb. 1.1674748390986.1171287961',
      fbEventId: 'Mozilla/5.0',
      userAgent: 'Mozilla/5.0',
      ip: '58.111.106.198',
      medium: 'survey',
      mediumId: 'FglfHAn30PRwsZVyQlKp'
    }
  }
};

export const exampleExtendedContact: ExtendedContact = {
  ...exampleGetContactResponse.contact, // Spread the original contact object

  // Custom Fields
  property_id: { optionName: 'PROP-12345', uniqueKey: 'property_id' },
  agent_name: { optionName: 'John Doe', uniqueKey: 'agent_name' },
  agent_main_phone: {
    optionName: '+1234567890',
    uniqueKey: 'agent_main_phone'
  },
  property_alt_photos: {
    optionName: [
      'https://example.com/photo1.jpg',
      'https://example.com/photo2.jpg'
    ],
    uniqueKey: 'property_alt_photos'
  },
  addressed_value: { optionName: 500000, uniqueKey: 'addressed_value' },
  property_beds: { optionName: 4, uniqueKey: 'property_beds' },
  broker_name: { optionName: 'Best Real Estate', uniqueKey: 'broker_name' },
  broker_phone: { optionName: '+1987654321', uniqueKey: 'broker_phone' },
  broker_website: {
    optionName: 'https://brokerwebsite.com',
    uniqueKey: 'broker_website'
  },
  property_city: { optionName: 'Sample City', uniqueKey: 'property_city' },
  property_county: {
    optionName: 'Sample County',
    uniqueKey: 'property_county'
  },
  days_on_mls: { optionName: 30, uniqueKey: 'days_on_mls' },
  estimated_value: { optionName: 550000, uniqueKey: 'estimated_value' },
  fips_code: { optionName: 12345, uniqueKey: 'fips_code' },
  full_baths: { optionName: 2, uniqueKey: 'full_baths' },
  full_street_address: {
    optionName: '1234 Elm St',
    uniqueKey: 'full_street_address'
  },
  half_baths: { optionName: 1, uniqueKey: 'half_baths' },
  hoa_fee: { optionName: 150, uniqueKey: 'hoa_fee' },
  last_sale_date: {
    optionName: '2023-08-01T00:00:00.000Z',
    uniqueKey: 'last_sale_date'
  },
  latitude: { optionName: 40.7128, uniqueKey: 'latitude' },
  list_date: { optionName: '2023-07-01T00:00:00.000Z', uniqueKey: 'list_date' },
  list_price: { optionName: 600000, uniqueKey: 'list_price' },
  longitude: { optionName: -74.006, uniqueKey: 'longitude' },
  lot_sqft: { optionName: 10000, uniqueKey: 'lot_sqft' },
  mls: { optionName: 'MLS123456', uniqueKey: 'mls' },
  nearby_schools: {
    optionName: ['School A', 'School B'],
    uniqueKey: 'nearby_schools'
  },
  mls_id: { optionName: '123-MLS-ID', uniqueKey: 'mls_id' },
  neighborhoods: {
    optionName: ['Downtown', 'Uptown'],
    uniqueKey: 'neighborhoods'
  },
  parking_garage: { optionName: 'Yes', uniqueKey: 'parking_garage' },
  price_per_sqft: { optionName: 200, uniqueKey: 'price_per_sqft' },
  primary_photo: {
    optionName: 'https://example.com/primary_photo.jpg',
    uniqueKey: 'primary_photo'
  },
  property_url: {
    optionName: 'https://propertywebsite.com',
    uniqueKey: 'property_url'
  },
  sold_price: { optionName: 590000, uniqueKey: 'sold_price' },
  sqft: { optionName: 3000, uniqueKey: 'sqft' },
  status: { optionName: 'For Sale', uniqueKey: 'status' },
  stories: { optionName: 2, uniqueKey: 'stories' },
  property_street: { optionName: '1234 Elm St', uniqueKey: 'property_street' },
  property_state: { optionName: 'NY', uniqueKey: 'property_state' },
  property_style: { optionName: 'Colonial', uniqueKey: 'property_style' },
  mls_description: {
    optionName: 'A beautiful colonial-style home...',
    uniqueKey: 'mls_description'
  },
  unit: { optionName: 'Unit 1', uniqueKey: 'unit' },
  year_built: { optionName: 1990, uniqueKey: 'year_built' },
  property_zip_code: { optionName: 12345, uniqueKey: 'property_zip_code' },

  // Custom Options (nested)
  customOptions: {
    facebook_profile: {
      optionName: 'https://facebook.com/sampleprofile',
      uniqueKey: 'facebook_profile'
    },
    instagram_profile: {
      optionName: 'https://instagram.com/sampleprofile',
      uniqueKey: 'instagram_profile'
    },
    custom_dnd: { optionName: 'Email', uniqueKey: 'custom_dnd' },
    call_outcome: { optionName: 'voicemail', uniqueKey: 'call_outcome' }
  }
};
