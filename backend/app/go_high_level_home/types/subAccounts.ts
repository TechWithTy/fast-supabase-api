export type Business = {
  name: string; // Business name
  address: string; // Business address
  city: string; // Business city
  state: string; // Business state
  country: string; // Business country
  postalCode: string; // Business postal code
  website: string; // Business website
  timezone: string; // Business timezone
  logoUrl: string; // URL to the business logo image
};

export type Social = {
  facebookUrl?: string; // Facebook URL
  googlePlus?: string; // Google+ URL
  linkedIn?: string; // LinkedIn URL
  foursquare?: string; // Foursquare URL
  twitter?: string; // Twitter URL
  yelp?: string; // Yelp URL
  instagram?: string; // Instagram URL
  youtube?: string; // YouTube URL
  pinterest?: string; // Pinterest URL
  blogRss?: string; // Blog RSS feed URL
  googlePlacesId?: string; // Google Places ID
};

export type Settings = {
  allowDuplicateContact: boolean; // Whether duplicate contacts are allowed
  allowDuplicateOpportunity: boolean; // Whether duplicate opportunities are allowed
  allowFacebookNameMerge: boolean; // Whether to merge Facebook names
  disableContactTimezone: boolean; // Whether to disable contact timezone
};

export type Location = {
  id: string; // Location ID
  companyId: string; // Company ID
  name: string; // Location name
  domain: string; // Domain of the location
  address: string; // Location address
  city: string; // Location city
  state: string; // Location state
  logoUrl: string; // URL of the logo image
  country: string; // Country code (e.g., "IN" for India)
  postalCode: string; // Postal code of the location
  website: string; // Website URL
  timezone: string; // Timezone of the location
  firstName: string; // First name of the contact person
  lastName: string; // Last name of the contact person
  email: string; // Email of the contact person
  phone: string; // Phone number of the contact person
  business: Business; // Business details
  social: Social; // Social media links
  settings: Settings; // Location settings
  reseller: object; // Reseller information (if any)
};

export type GetSubAccountResponse = {
  location: Location; // Location object returned in the response
};

export type GetSubAccountPathParams = {
  locationId: string; // Required Location ID for querying the sub-account
};

export type GetSubAccountHeaders = {
  Authorization: string; // Bearer token for authorization
  Version: string; // API version (e.g., '2021-07-28')
};

export const exampleGetSubAccountResponse: GetSubAccountResponse = {
  location: {
    id: 've9EPM428h8vShlRW1KT',
    companyId: '5DP4iH6HLkQsiKESj6rh',
    name: 'dentist',
    domain: 'test.msgsndr.com',
    address: 'ganthi nagar, gyanbabu chauk motihati',
    city: 'motihari',
    state: 'Loca',
    logoUrl:
      'https://dummyimage.com/o/locationPhotos%2Fve9EPM428h8vShlRW1KT.jpeg',
    country: 'IN',
    postalCode: '567654',
    website: 'https://gohighlevel.com/',
    timezone: 'America/Chicago',
    firstName: 'Dr. Rane',
    lastName: 'deo',
    email: 'rane@due.com',
    phone: '+919039160788',
    business: {
      name: 'dentist',
      address: 'MIG 14, Delhi',
      city: 'delhi',
      state: 'delhi',
      country: 'IN',
      postalCode: '567654',
      website: 'https://gohighlevel.com/',
      timezone: 'America/Chicago',
      logoUrl:
        'https://dummyimage.com/o/locationPhotos%2Fve9EPM428h8vShlRW1KT.jpeg'
    },
    social: {
      facebookUrl: 'https://www.facebook.com/',
      googlePlus: 'https://www.googleplus.com/',
      linkedIn: 'https://www.linkedIn.com/',
      foursquare: 'https://www.foursquare.com/',
      twitter: 'https://www.foutwitterrsquare.com/',
      yelp: 'https://www.yelp.com/',
      instagram: 'https://www.instagram.com/',
      youtube: 'https://www.youtube.com/',
      pinterest: 'https://www.pinterest.com/',
      blogRss: 'https://www.blogRss.com/',
      googlePlacesId: 'ChIJJGPdVbQTrjsRGUkefteUeFk'
    },
    settings: {
      allowDuplicateContact: false,
      allowDuplicateOpportunity: false,
      allowFacebookNameMerge: false,
      disableContactTimezone: false
    },
    reseller: {}
  }
};
