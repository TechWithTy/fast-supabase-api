import os
import requests
from typing import Dict, Any

# Base URL for your customer service (replace with actual URL)
CUSTOMER_SERVICE_BASE_URL = 'https://api.yourdomain.com'

def get_customer_voice_data(customer_id: str) -> Dict[str, Any]:
    """
    Fetch the customer's voice data from the customer service.
    
    Args:
        customer_id: The unique ID of the customer
        
    Returns:
        Dictionary containing the customer's voice data
        
    Raises:
        Exception: If fetching voice data fails
    """
    url = f"{CUSTOMER_SERVICE_BASE_URL}/customers/{customer_id}/voice-data"
    
    headers = {
        "Authorization": f"Bearer {os.getenv('AUTH_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            voice_data = response.json()
            print(f"Successfully fetched voice data for customer {customer_id}")
            return voice_data
        else:
            print(f"Failed to fetch voice data for customer {customer_id}: {response.reason}")
            raise Exception(f"Failed to fetch customer voice data: {response.reason}")
    except Exception as error:
        print(f"Error fetching customer voice data for customer {customer_id}: {error}")
        raise Exception("Could not fetch customer voice data.")
