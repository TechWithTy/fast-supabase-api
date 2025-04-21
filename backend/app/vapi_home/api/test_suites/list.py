import os
import requests
from typing import Dict, Any, List, Optional

def list_test_suites(
    limit: int = 100,
    created_at_gt: Optional[str] = None,
    created_at_lt: Optional[str] = None,
    updated_at_gt: Optional[str] = None,
    updated_at_lt: Optional[str] = None
) -> Dict[str, Any]:
    api_key = os.getenv('VAPI_PRIVATE_KEY')
    url = "https://api.vapi.ai/test-suite"
    
    params = {'limit': limit}
    if created_at_gt:
        params['createdAtGt'] = created_at_gt
    if created_at_lt:
        params['createdAtLt'] = created_at_lt
    if updated_at_gt:
        params['updatedAtGt'] = updated_at_gt
    if updated_at_lt:
        params['updatedAtLt'] = updated_at_lt
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error listing test suites: {e}")
        raise