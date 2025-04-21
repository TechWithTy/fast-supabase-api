from typing import Dict, Any
import os
import httpx
import logging

class GoHighLevelClient:
    """
    Client for interacting with the Go High Level API.
    """

    def __init__(self):
        self.api_base_url = "https://services.leadconnectorhq.com"
        self.api_version = "2021-07-28"
        self.api_key = os.getenv('GO_HIGH_LEVEL_API_KEY')

        if not self.api_key:
            raise ValueError("GO_HIGH_LEVEL_API_KEY environment variable is not set")

    def get_headers(self) -> Dict[str, str]:
        """
        Get the headers required for API requests.

        Returns:
            Dict[str, str]: Dictionary containing Authorization and Version headers
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Version": self.api_version
        }

    async def make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an HTTP request to the Go High Level API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint to call
            **kwargs: Additional arguments to pass to httpx.request

        Returns:
            Dict[str, Any]: JSON response from the API
        """
        url = f"{self.api_base_url}/{endpoint}"
        headers = self.get_headers()

        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()