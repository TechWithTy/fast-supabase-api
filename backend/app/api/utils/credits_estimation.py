"""
credits_estimation.py
Utility functions to estimate credits for OSINT endpoints before resource-intensive operations.
"""
from typing import Any

def estimate_mls_credits(req: Any) -> int:
    # Always estimate 1 credit for MLS, since result size cannot be known in advance
    return 1

def estimate_phone_credits(req: Any) -> int:
    # Use the number of phone numbers submitted
    try:
        return max(len(getattr(req, 'phone_numbers', [])), 1)
    except Exception:
        return 1

def estimate_theharvester_credits(req: Any) -> int:
    # Use the number of modules as a proxy, or 1
    try:
        modules = getattr(req, 'modules', None)
        if modules:
            return max(len(modules), 1)
        return 1
    except Exception:
        return 1

def estimate_zehef_credits(req: Any) -> int:
    # Always 1 for a single email lookup
    return 1
