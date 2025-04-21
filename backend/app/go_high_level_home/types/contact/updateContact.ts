// Existing custom field type for update
export type UpdateCustomField = {
  id: string; // Unique ID of the custom field
  key: string; // The key or name of the custom field
  field_value: any; // The new value for the custom field
};

// Define the type for DND settings
export type DndSetting = {
  status: string;
  message: string;
  code: string;
};

// Define the main update contact request type
export type UpdateContactRequest = {
  firstName?: string;
  lastName?: string;
  name?: string;
  email?: string;
  phone?: string;
  address1?: string;
  city?: string;
  state?: string;
  postalCode?: string;
  website?: string;
  timezone?: string;
  dnd?: boolean;
  dndSettings?: {
    Call?: DndSetting;
    Email?: DndSetting;
    SMS?: DndSetting;
    WhatsApp?: DndSetting;
    GMB?: DndSetting;
    FB?: DndSetting;
  };
  inboundDndSettings?: {
    all?: {
      status: string;
      message: string;
    };
  };
  tags?: string[];
  customFields?: UpdateCustomField[]; // Array of custom fields for the update
  source?: string;
  country?: string;
  assignedTo?: string;
};

export const updateContactRequest: UpdateContactRequest = {
  firstName: 'rosan',
  lastName: 'Deo',
  name: 'rosan Deo',
  email: 'rosan@deos.com',
  phone: '+1 888-888-8888',
  address1: '3535 1st St N',
  city: 'Dolomite',
  state: 'AL',
  postalCode: '35061',
  website: 'https://www.tesla.com',
  timezone: 'America/Chihuahua',
  dnd: true,
  dndSettings: {
    Call: {
      status: 'active',
      message: 'string',
      code: 'string'
    },
    Email: {
      status: 'active',
      message: 'string',
      code: 'string'
    },
    SMS: {
      status: 'active',
      message: 'string',
      code: 'string'
    },
    WhatsApp: {
      status: 'active',
      message: 'string',
      code: 'string'
    },
    GMB: {
      status: 'active',
      message: 'string',
      code: 'string'
    },
    FB: {
      status: 'active',
      message: 'string',
      code: 'string'
    }
  },
  inboundDndSettings: {
    all: {
      status: 'active',
      message: 'string'
    }
  },
  tags: ['nisi sint commodo amet', 'consequat'],
  customFields: [
    {
      id: 'MgobCB14YMVKuE4Ka8p1',
      key: 'agent_name',
      field_value: 'John Doe'
    },
    {
      id: '6dvNaf7VhkQ9snc5vnjJ',
      key: 'property_id',
      field_value: 'PROP-456'
    },
    {
      id: 'Fb123',
      key: 'facebook_profile',
      field_value: 'https://facebook.com/sampleprofile'
    },
    {
      id: 'Ig123',
      key: 'instagram_profile',
      field_value: 'https://instagram.com/sampleprofile'
    }
  ],
  source: 'public api',
  country: 'US',
  assignedTo: 'y0BeYjuRIlDwsDcOHOJo'
};

export const extendedUpdateContactRequest: UpdateContactRequest = {
  ...updateContactRequest, // Spread the existing fields to preserve them
  customFields: [
    ...(updateContactRequest.customFields ?? []), // Use an empty array if customFields is undefined
    {
      id: '123PropertyAltPhotos',
      key: 'property_alt_photos',
      field_value: [
        'https://example.com/photo1.jpg',
        'https://example.com/photo2.jpg'
      ]
    },
    {
      id: '456AddressedValue',
      key: 'addressed_value',
      field_value: 250000
    },
    {
      id: '789PropertyBeds',
      key: 'property_beds',
      field_value: 4
    },
    {
      id: '1011BrokerName',
      key: 'broker_name',
      field_value: 'Real Estate Brokers Inc.'
    },
    {
      id: '1213BrokerPhone',
      key: 'broker_phone',
      field_value: '+1 555-555-5555'
    },
    {
      id: '1415BrokerWebsite',
      key: 'broker_website',
      field_value: 'https://realestatebroker.com'
    },
    {
      id: '1617PropertyCity',
      key: 'property_city',
      field_value: 'Springfield'
    },
    {
      id: '1819PropertyCounty',
      key: 'property_county',
      field_value: 'Greene'
    },
    {
      id: '2021DaysOnMLS',
      key: 'days_on_mls',
      field_value: 30
    },
    {
      id: '2223EstimatedValue',
      key: 'estimated_value',
      field_value: 275000
    },
    {
      id: '2425FipsCode',
      key: 'fips_code',
      field_value: 12345
    },
    {
      id: '2627FullBaths',
      key: 'full_baths',
      field_value: 2
    },
    {
      id: '2829FullStreetAddress',
      key: 'full_street_address',
      field_value: '123 Elm St, Apt 4B'
    },
    {
      id: '3031HalfBaths',
      key: 'half_baths',
      field_value: 1
    },
    {
      id: '3233HoaFee',
      key: 'hoa_fee',
      field_value: 200
    },
    {
      id: '3435LastSaleDate',
      key: 'last_sale_date',
      field_value: '2023-09-01T00:00:00.000Z'
    },
    {
      id: '3637Latitude',
      key: 'latitude',
      field_value: 37.7749
    },
    {
      id: '3839ListDate',
      key: 'list_date',
      field_value: '2023-09-01T00:00:00.000Z'
    },
    {
      id: '4041ListPrice',
      key: 'list_price',
      field_value: 350000
    },
    {
      id: '4243Longitude',
      key: 'longitude',
      field_value: -122.4194
    },
    {
      id: '4445LotSqft',
      key: 'lot_sqft',
      field_value: 5000
    },
    {
      id: '4647MLS',
      key: 'mls',
      field_value: 'MLS12345'
    },
    {
      id: '4849NearbySchools',
      key: 'nearby_schools',
      field_value: ['Lincoln Elementary', 'Washington High School']
    },
    {
      id: '5051MLSID',
      key: 'mls_id',
      field_value: 'MLS-ID-6789'
    },
    {
      id: '5253Neighborhoods',
      key: 'neighborhoods',
      field_value: ['Downtown', 'Uptown']
    },
    {
      id: '5455ParkingGarage',
      key: 'parking_garage',
      field_value: 'Yes'
    },
    {
      id: '5657PricePerSqft',
      key: 'price_per_sqft',
      field_value: 300
    },
    {
      id: '5859PrimaryPhoto',
      key: 'primary_photo',
      field_value: 'https://example.com/primary-photo.jpg'
    },
    {
      id: '6061PropertyURL',
      key: 'property_url',
      field_value: 'https://example.com/property'
    },
    {
      id: '6263SoldPrice',
      key: 'sold_price',
      field_value: 320000
    },
    {
      id: '6465Sqft',
      key: 'sqft',
      field_value: 1500
    },
    {
      id: '6667Status',
      key: 'status',
      field_value: 'Active'
    },
    {
      id: '6869Stories',
      key: 'stories',
      field_value: 2
    },
    {
      id: '7071PropertyStreet',
      key: 'property_street',
      field_value: '123 Elm St'
    },
    {
      id: '7273PropertyState',
      key: 'property_state',
      field_value: 'CA'
    },
    {
      id: '7475PropertyStyle',
      key: 'property_style',
      field_value: 'Ranch'
    },
    {
      id: '7677MLSDescription',
      key: 'mls_description',
      field_value:
        'A beautiful ranch-style home with a spacious backyard and modern amenities.'
    },
    {
      id: '7879Unit',
      key: 'unit',
      field_value: '4B'
    },
    {
      id: '8081YearBuilt',
      key: 'year_built',
      field_value: 1995
    },
    {
      id: '8283PropertyZipCode',
      key: 'property_zip_code',
      field_value: 94103
    },
    {
      id: '8485FacebookProfile',
      key: 'facebook_profile',
      field_value: 'https://facebook.com/sampleprofile'
    },
    {
      id: '8687InstagramProfile',
      key: 'instagram_profile',
      field_value: 'https://instagram.com/sampleprofile'
    },
    {
      id: '8889CustomDnd',
      key: 'custom_dnd',
      field_value: ['Email', 'Phone'] // Example values for custom DND
    },
    {
      id: '9091CallOutcome',
      key: 'call_outcome',
      field_value: 'Appointment Booked' // Example value from EndedReason options
    }
  ]
};
