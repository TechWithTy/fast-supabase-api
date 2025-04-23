import json
import logging
from typing import Any

import httpx
from fastapi import HTTPException

from app.core.config import settings

logger = logging.getLogger("apps.supabase_home")


class SupabaseError(Exception):
    """Base exception for Supabase-related errors"""
    pass

class SupabaseAuthError(SupabaseError):
    """Exception raised for authentication errors"""
    pass

class SupabaseAPIError(SupabaseError):
    """Exception raised for API errors"""
    def __init__(self, message: str, status_code: int = None, details: dict = None):
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

class SupabaseService:
    """
    Service class for interacting with Supabase API.

    This class provides methods for interacting with various Supabase services:
    - Auth (user management)
    - Database (PostgreSQL)
    - Storage
    - Edge Functions
    - Realtime

    It handles authentication, request formatting, and response parsing.
    """

    def __init__(self):
        from app.supabase_home import get_supabase_client
        self.base_url = settings.SUPABASE_URL
        self.anon_key = settings.SUPABASE_ANON_KEY
        self.service_role_key = settings.SUPABASE_SERVICE_ROLE_KEY
        self.raw = get_supabase_client()


        self._configure_service()

        if not self.base_url:
            logger.error("SUPABASE_URL is not set in settings")
            raise ValueError("SUPABASE_URL is not set in settings")

        if not self.anon_key:
            logger.error("SUPABASE_ANON_KEY is not set in settings")
            raise ValueError("SUPABASE_ANON_KEY is not set in settings")

        if not self.service_role_key:
            logger.warning(
                "SUPABASE_SERVICE_ROLE_KEY is not set in settings. Admin operations will not work."
            )

    def _get_headers(
        self, auth_token: str | None = None, is_admin: bool = False
    ) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "apikey": self.service_role_key if is_admin else self.anon_key,
        }

        if is_admin:
            if not self.service_role_key:
                raise SupabaseAuthError(
                    "Service role key is required for admin operations"
                )
            headers["Authorization"] = f"Bearer {self.service_role_key}"
        elif auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        return headers

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        auth_token: str | None = None,
        is_admin: bool = False,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int = 30,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{endpoint}"

        request_headers = self._get_headers(auth_token, is_admin)
        if headers:
            request_headers.update(headers)

        logger.info(f"Making {method} request to {url}")
        logger.info(f"Headers: {request_headers}")
        if "Authorization" in request_headers:
            auth_header = request_headers["Authorization"]
            logger.info(f"Authorization header: {auth_header[:15]}...")
        else:
            logger.info("No Authorization header found")

        logger.info(f"Request data: {data}")
        logger.info(f"Request params: {params}")

        if (
            data is None
            and "Content-Type" in request_headers
            and request_headers["Content-Type"] == "application/json"
        ):
            data = {}
            logger.info("Initialized empty JSON data")

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    json=data,
                    params=params,
                )

            logger.info(f"Request to {url}: {method} - Status: {response.status_code}")
            logger.info(f"Response headers: {response.headers}")

            try:
                if response.content:
                    logger.info(f"Response content: {response.content[:200]}...")
                    if response.status_code >= 400:
                        logger.error(f"Error response: {response.content}")
            except Exception as e:
                logger.error(f"Error logging response content: {str(e)}")

            if response.status_code == 401 or response.status_code == 403:
                error_detail = self._parse_error_response(response)
                logger.error(f"Authentication error: {error_detail}")
                raise HTTPException(status_code=response.status_code, detail=str(error_detail))

            response.raise_for_status()

            if response.content:
                return response.json()
            return {}

        except httpx.HTTPStatusError as e:
            error_detail = self._parse_error_response(e.response)
            logger.error(f"Supabase API error: {str(e)} - Details: {error_detail}")
            raise HTTPException(status_code=e.response.status_code, detail=str(error_detail))

        except httpx.RequestError as e:
            logger.error(f"Supabase request exception: {str(e)}")
            raise HTTPException(status_code=500, detail="Request error")

        except Exception as e:
            logger.exception(f"Unexpected error during Supabase request: {str(e)}")
            raise HTTPException(status_code=500, detail="Unexpected error during Supabase request")

    def _parse_error_response(self, response) -> dict:
        try:
            return response.json()
        except Exception:
            return {"status": getattr(response, "status_code", None), "message": getattr(response, "text", str(response))}
