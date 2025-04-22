# Re-export SupabaseService from _service.py for compatibility with tests
from ._service import (
    SupabaseAPIError,
    SupabaseAuthError,
    SupabaseError,
    SupabaseService,
)

__all__ = ['SupabaseService', 'SupabaseError', 'SupabaseAuthError', 'SupabaseAPIError']
