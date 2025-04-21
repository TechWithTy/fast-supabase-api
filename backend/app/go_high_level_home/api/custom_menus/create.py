from typing import Dict, Any, List
import httpx

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def create_custom_menu(
    headers: Dict[str, str],
    title: str,
    url: str,
    icon_name: str,
    icon_font_family: str,
    show_on_company: bool = True,
    show_on_location: bool = True,
    show_to_all_locations: bool = True,
    open_mode: str = "iframe",
    locations: List[str] = None,
    user_role: str = "all",
    allow_camera: bool = False,
    allow_microphone: bool = False
) -> Dict[str, Any]:
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")

    request_headers = {
        "Accept": "application/json",
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Version": headers.get("Version", API_VERSION)
    }

    data = {
        "title": title,
        "url": url,
        "icon": {
            "name": icon_name,
            "fontFamily": icon_font_family
        },
        "showOnCompany": show_on_company,
        "showOnLocation": show_on_location,
        "showToAllLocations": show_to_all_locations,
        "openMode": open_mode,
        "locations": locations or [],
        "userRole": user_role,
        "allowCamera": allow_camera,
        "allowMicrophone": allow_microphone
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_BASE_URL}/custom-menus/", headers=request_headers, json=data)
        response.raise_for_status()
        return response.json()