import requests
import json

def create_calendar(token, api_version, calendar_data):
    """
    Create a calendar in Go High Level
    
    Args:
        token (str): Access token for authentication
        api_version (str): API version to use (e.g., '2021-04-15')
        calendar_data (dict): Calendar configuration data
        
    Returns:
        dict: Response from the API containing the created calendar
    """
    url = "https://services.leadconnectorhq.com/calendars/"
    
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Version": api_version
    }
    
    response = requests.post(url, headers=headers, json=calendar_data)
    response.raise_for_status()
    
    return response.json()