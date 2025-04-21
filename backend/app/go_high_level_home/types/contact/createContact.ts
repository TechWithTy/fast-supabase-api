// Define the custom field type
export type ContactCustomField = {
  id: string; // Unique ID of the custom field
  value: any; // Value of the custom field
};

// Define DND settings type
export type DndStatus = 'active' | 'inactive';

export type DndSettings = {
  status: DndStatus;
  message: string;
  code: string;
};

export type DndSettingsType = {
  Call: DndSettings;
  Email: DndSettings;
  SMS: DndSettings;
  WhatsApp: DndSettings;
  GMB: DndSettings;
  FB: DndSettings;
};

// Define the type for creating a contact response
export type CreateContactResponse = {
  contact: {
    id: string;
    dateAdded: string; // ISO date string
    dateUpdated: string; // ISO date string
    deleted: boolean;
    tags: string[];
    type: string;
    customFields: ContactCustomField[];
    locationId: string;
    firstName: string;
    firstNameLowerCase: string;
    fullNameLowerCase: string;
    lastName: string;
    lastNameLowerCase: string;
    email: string;
    emailLowerCase: string;
    bounceEmail: boolean;
    unsubscribeEmail: boolean;
    dnd: boolean;
    dndSettings: DndSettingsType;
    phone: string;
    address1?: string;
    city?: string;
    state?: string;
    country?: string;
    postalCode?: string;
    website?: string;
    source?: string;
    companyName?: string;
    dateOfBirth?: string; // ISO date string
    birthMonth?: number;
    birthDay?: number;
    lastSessionActivityAt?: string; // ISO date string
    offers?: string[]; // Assuming offers and products are arrays of strings
    products?: string[];
    businessId: string;
    assignedTo?: string;
  };
};

export const exampleCreateContactResponse: CreateContactResponse = {
  contact: {
    id: 'seD4PfOuKoVMLkEZqohJ',
    dateAdded: '2021-08-31T09:59:41.937Z',
    dateUpdated: '2021-08-31T09:59:41.937Z',
    deleted: false,
    tags: ['nisi sint commodo amet', 'consequat'],
    type: 'read',
    customFields: [
      {
        id: '123PropertyAltPhotos',
        value: [
          'https://example.com/photo1.jpg',
          'https://example.com/photo2.jpg'
        ]
      },
      {
        id: '456AddressedValue',
        value: 250000
      },
      {
        id: '789PropertyBeds',
        value: 4
      },
      {
        id: '1011BrokerName',
        value: 'Real Estate Brokers Inc.'
      },
      {
        id: '1213BrokerPhone',
        value: '+1 555-555-5555'
      },
      {
        id: '1415BrokerWebsite',
        value: 'https://realestatebroker.com'
      },
      {
        id: '1617PropertyCity',
        value: 'Springfield'
      },
      {
        id: '1819PropertyCounty',
        value: 'Greene'
      },
      {
        id: '2021DaysOnMLS',
        value: 30
      },
      {
        id: '2223EstimatedValue',
        value: 275000
      },
      {
        id: '2425FipsCode',
        value: 12345
      },
      {
        id: '2627FullBaths',
        value: 2
      },
      {
        id: '2829FullStreetAddress',
        value: '123 Elm St, Apt 4B'
      },
      {
        id: '3031HalfBaths',
        value: 1
      },
      {
        id: '3233HoaFee',
        value: 200
      },
      {
        id: '3435LastSaleDate',
        value: '2023-09-01T00:00:00.000Z'
      },
      {
        id: '3637Latitude',
        value: 37.7749
      },
      {
        id: '3839ListDate',
        value: '2023-09-01T00:00:00.000Z'
      },
      {
        id: '4041ListPrice',
        value: 350000
      },
      {
        id: '4243Longitude',
        value: -122.4194
      },
      {
        id: '4445LotSqft',
        value: 5000
      },
      {
        id: '4647MLS',
        value: 'MLS12345'
      },
      {
        id: '4849NearbySchools',
        value: ['Lincoln Elementary', 'Washington High School']
      },
      {
        id: '5051MLSID',
        value: 'MLS-ID-6789'
      },
      {
        id: '5253Neighborhoods',
        value: ['Downtown', 'Uptown']
      },
      {
        id: '5455ParkingGarage',
        value: 'Yes'
      },
      {
        id: '5657PricePerSqft',
        value: 300
      },
      {
        id: '5859PrimaryPhoto',
        value: 'https://example.com/primary-photo.jpg'
      },
      {
        id: '6061PropertyURL',
        value: 'https://example.com/property'
      },
      {
        id: '6263SoldPrice',
        value: 320000
      },
      {
        id: '6465Sqft',
        value: 1500
      },
      {
        id: '6667Status',
        value: 'Active'
      },
      {
        id: '6869Stories',
        value: 2
      },
      {
        id: '7071PropertyStreet',
        value: '123 Elm St'
      },
      {
        id: '7273PropertyState',
        value: 'CA'
      },
      {
        id: '7475PropertyStyle',
        value: 'Ranch'
      },
      {
        id: '7677MLSDescription',
        value:
          'A beautiful ranch-style home with a spacious backyard and modern amenities.'
      },
      {
        id: '7879Unit',
        value: '4B'
      },
      {
        id: '8081YearBuilt',
        value: 1995
      },
      {
        id: '8283PropertyZipCode',
        value: 94103
      },
      {
        id: '8485FacebookProfile',
        value: 'https://facebook.com/sampleprofile'
      },
      {
        id: '8687InstagramProfile',
        value: 'https://instagram.com/sampleprofile'
      },
      {
        id: '8889CustomDnd',
        value: ['Email', 'Phone'] // Example values for custom DND
      },
      {
        id: '9091CallOutcome',
        value: 'Appointment Booked' // Example value from EndedReason options
      }
    ],
    locationId: 've9EPM428h8vShlRW1KT',
    firstName: 'rubika',
    firstNameLowerCase: 'rubika',
    fullNameLowerCase: 'rubika deo',
    lastName: 'Deo',
    lastNameLowerCase: 'deo',
    email: 'rubika@deos.com',
    emailLowerCase: 'rubika@deos.com',
    bounceEmail: false,
    unsubscribeEmail: false,
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
    phone: '+18832327657',
    address1: '3535 1st St N',
    city: 'ruDolomitebika',
    state: 'AL',
    country: 'US',
    postalCode: '35061',
    website: 'https://www.tesla.com',
    source: 'public api',
    companyName: 'DGS VolMAX',
    dateOfBirth: '1990-09-25T00:00:00.000Z',
    birthMonth: 8,
    birthDay: 25,
    lastSessionActivityAt: '2021-07-16T11:39:30.564Z',
    offers: [],
    products: [],
    businessId: '641c094001436dbc2081e642',
    assignedTo: 'y0BeYjuRIlDwsDcOHOJo'
  }
};
