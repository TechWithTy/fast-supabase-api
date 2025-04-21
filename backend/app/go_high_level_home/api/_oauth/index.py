import os
import requests
from typing import Dict, Any

BASE_URL = "https://api.gohighlevel.com/v1"

class LocationTokenRequest:
    def __init__(self, company_id: str, location_id: str):
        self.company_id = company_id
        self.location_id = location_id

class InstalledLocationsParams:
    def __init__(self, limit: int = None, skip: int = None):
        self.limit = limit
        self.skip = skip

def get_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def get_access_token(client_credentials: Dict[str, str]) -> Dict[str, Any]:
    """
    Get access token using client credentials.
    """
    url = f"{BASE_URL}/oauth/token"
    response = requests.post(url, json=client_credentials)
    if not response.ok:
        raise Exception(f"Error fetching access token: {response.text}")
    return response.json()

def get_location_access_token(token: str, data: LocationTokenRequest) -> Dict[str, Any]:
    """
    Get location access token using an agency token.
    
    Args:
        token: The agency access token.
        data: The request body containing company and location IDs.
    
    Returns:
        A dictionary containing the location access token response.
    """
    url = f"{BASE_URL}/oauth/locationToken"
    payload = {
        "companyId": data.company_id,
        "locationId": data.location_id
    }
    response = requests.post(url, json=payload, headers=get_headers(token))
    if not response.ok:
        raise Exception(f"Error fetching location access token: {response.text}")
    return response.json()

def get_installed_locations(token: str, params: InstalledLocationsParams) -> Dict[str, Any]:
    """
    Get locations where the app is installed.
    
    Args:
        token: The access token.
        params: The query parameters for filtering installed locations.
    
    Returns:
        A dictionary containing the installed locations response.
    """
    # Convert params to a dictionary, filtering out None values
    url_params = {}
    if params.limit is not None:
        url_params["limit"] = str(params.limit)
    if params.skip is not None:
        url_params["skip"] = str(params.skip)
    
    url = f"{BASE_URL}/oauth/installedLocations"
    response = requests.get(url, params=url_params, headers=get_headers(token))
    if not response.ok:
        raise Exception(f"Error fetching installed locations: {response.text}")
    return response.json()

# Example usage
client_credentials = {
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "grant_type": "client_credentials"
}

# Get Access Token
try:
    token_response = get_access_token(client_credentials)
    print(f"Access Token: {token_response}")
    token = token_response.get("access_token")
except Exception as e:
    print(f"Error fetching access token: {e}")
    token = None

if token:
    # Get Location Access Token
    location_token_data = LocationTokenRequest(
        company_id="your-company-id",
        location_id="your-location-id"
    )
    
    try:
        location_token_response = get_location_access_token(token, location_token_data)
        print(f"Location Access Token: {location_token_response}")
    except Exception as e:
        print(f"Error fetching location access token: {e}")
    
    # Define installed_locations_params
    installed_locations_params = InstalledLocationsParams(limit=10)
    
    # Fetch Installed Locations
    async def fetch_installed_locations():
        try:
            response = get_installed_locations(token, installed_locations_params)
            print(f"Installed Locations: {response}")
        except Exception as e:
            print(f"Error fetching installed locations: {e}")
    
    # Since this is Python, we need to use asyncio to run the async function
    import asyncio
    asyncio.run(fetch_installed_locations())
