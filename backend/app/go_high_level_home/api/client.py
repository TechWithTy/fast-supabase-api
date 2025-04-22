from typing import Any

import httpx

from app.core.config import settings


class GoHighLevelClient:
    """
    Client for interacting with the Go High Level API.
    """

    def __init__(self, api_key: str | None = None, api_base_url: str | None = None):
        self.api_key = api_key or settings.GHL_API_KEY
        self.api_base_url = api_base_url or settings.GHL_API_BASE_URL
        self.api_version = "2021-07-28"

        if not self.api_key:
            raise ValueError("GO_HIGH_LEVEL_API_KEY environment variable or GHL_API_KEY setting is not set")

    def get_headers(self) -> dict[str, str]:
        """
        Get the headers required for API requests.

        Returns:
            dict[str, str]: Dictionary containing Authorization and Version headers
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Version": self.api_version
        }

    async def make_request(self, method: str, endpoint: str, **kwargs) -> dict[str, Any]:
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