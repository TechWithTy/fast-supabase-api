from typing import Dict, Any, Optional, List
import httpx
import logging

API_BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"

async def update_opportunity(
    headers: Dict[str, str],
    opportunity_id: str,
    pipeline_id: Optional[str] = None,
    name: Optional[str] = None,
    pipeline_stage_id: Optional[str] = None,
    status: Optional[str] = None,
    monetary_value: Optional[float] = None,
    assigned_to: Optional[str] = None,
    custom_fields: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/opportunities/{opportunity_id}"
    
    if not headers.get("Authorization") or not headers["Authorization"].startswith("Bearer "):
        raise ValueError("Missing or invalid Authorization header. Must be in format: 'Bearer {token}'")
    
    request_headers = {
        "Authorization": headers["Authorization"],
        "Version": headers.get("Version", API_VERSION),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {}
    if pipeline_id:
        payload["pipelineId"] = pipeline_id
    if name:
        payload["name"] = name
    if pipeline_stage_id:
        payload["pipelineStageId"] = pipeline_stage_id
    if status:
        payload["status"] = status
    if monetary_value is not None:
        payload["monetaryValue"] = monetary_value
    if assigned_to:
        payload["assignedTo"] = assigned_to
    if custom_fields:
        payload["customFields"] = custom_fields
    
    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=request_headers, json=payload)
    
    response.raise_for_status()
    return response.json()