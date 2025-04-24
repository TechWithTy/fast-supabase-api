"""
OSINT endpoint using theHarvester submodule (tools/theHarvester)

This endpoint allows you to perform reconnaissance using theHarvester from your FastAPI backend.
It executes theHarvester as a subprocess and returns its output.

Requirements:
- Python 3.11+
- theHarvester installed as a submodule in backend/app/osint/tools/theHarvester
- Optionally configure api-keys.yaml for advanced modules

Security: This endpoint is for demonstration and should be protected in production.
"""
import subprocess
import sys
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/osint/theharvester", tags=["theHarvester OSINT"])

class TheHarvesterRequest(BaseModel):
    domain: str = Query(..., description="Domain to search for (e.g. example.com)")
    sources: list[str] = Query(["google"], description="Comma-separated list of sources (e.g. google,bing,baidu)")
    limit: int = Query(100, description="Number of results to fetch")

@router.post("/search", response_model=dict[str, Any])
async def theharvester_search(req: TheHarvesterRequest):
    """
    Run theHarvester as a subprocess and return its output.
    """
    # Path to theHarvester.py in the submodule
    harvester_path = "../../osint/tools/theHarvester/theHarvester.py"
    sources_arg = ",".join(req.sources)
    cmd = [
        sys.executable, harvester_path,
        "-d", req.domain,
        "-b", sources_arg,
        "-l", str(req.limit),
        "-f", "output.html"
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "exit_code": proc.returncode,
            "output_file": "output.html"
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"theHarvester failed: {e.stderr}")
