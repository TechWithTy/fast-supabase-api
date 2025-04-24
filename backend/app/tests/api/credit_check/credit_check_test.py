"""
Unit tests for the credit check utility (call_function_with_credits) covering edge cases and core functionality.
Does NOT use actual API endpoints.
"""
import pytest
import asyncio
from fastapi import HTTPException, Request, status
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch, MagicMock

from app.api.utils.credits import call_function_with_credits, settings

class DummyUser(SimpleNamespace):
    pass

@pytest.mark.anyio
async def test_authentication_required():
    async def dummy_func(request, user):
        return "ok"
    req = MagicMock(spec=Request)
    with pytest.raises(HTTPException) as exc:
        await call_function_with_credits(dummy_func, req, credit_type="ai", db=None, current_user=None, credit_amount=1)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.anyio
async def test_admin_override_credit_amount():
    async def dummy_func(request, user):
        return {"result": "ok"}
    req = MagicMock(spec=Request)
    req.json = AsyncMock(return_value={"credit_amount": 7, "subscription_id": "sub123"})
    user = DummyUser(is_superuser=True)
    with patch.object(type(settings), "db_backend", new=property(lambda self: "supabase")), \
         patch("app.api.utils.credits.supabase.get_database_service") as mock_db_service:
        mock_db_service.return_value.fetch_data.return_value = [{"allotted": 100, "used": 0, "id": 1}]
        mock_db_service.return_value.update_data.return_value = None
        result = await call_function_with_credits(dummy_func, req, credit_type="ai", db=None, current_user=user, credit_amount=1)
        assert result["result"] == "ok"

@pytest.mark.anyio
async def test_insufficient_credits_supabase():
    async def dummy_func(request, user):
        return "should not get here"
    req = MagicMock(spec=Request)
    req.json = AsyncMock(return_value={"credit_amount": 5, "subscription_id": "sub123"})
    user = DummyUser(is_superuser=False)
    with patch.object(type(settings), "db_backend", new=property(lambda self: "supabase")), \
         patch("app.api.utils.credits.supabase.get_database_service") as mock_db_service:
        mock_db_service.return_value.fetch_data.return_value = [{"allotted": 3, "used": 0, "id": 1}]
        with pytest.raises(HTTPException) as exc:
            await call_function_with_credits(dummy_func, req, credit_type="ai", db=None, current_user=user, credit_amount=5)
        assert exc.value.status_code == status.HTTP_402_PAYMENT_REQUIRED
        assert "Insufficient ai credits" in str(exc.value.detail)

@pytest.mark.anyio
async def test_invalid_credit_type():
    async def dummy_func(request, user):
        return "ok"
    req = MagicMock(spec=Request)
    req.json = AsyncMock(return_value={"subscription_id": "sub123"})
    user = DummyUser(is_superuser=True)
    with patch.object(type(settings), "db_backend", new=property(lambda self: "supabase")), \
         patch("app.api.utils.credits.supabase.get_database_service") as mock_db_service:
        mock_db_service.return_value.fetch_data.return_value = [{"allotted": 100, "used": 0, "id": 1}]
        with pytest.raises(HTTPException) as exc:
            await call_function_with_credits(dummy_func, req, credit_type="invalid", db=None, current_user=user, credit_amount=1)
        assert exc.value.status_code == 400
        assert "Invalid credit_type" in str(exc.value.detail)

@pytest.mark.anyio
async def test_subscription_id_required():
    async def dummy_func(request, user):
        return "ok"
    req = MagicMock(spec=Request)
    req.json = AsyncMock(return_value={})
    user = DummyUser(is_superuser=True)
    with patch.object(type(settings), "db_backend", new=property(lambda self: "supabase")), \
         patch("app.api.utils.credits.supabase.get_database_service") as mock_db_service:
        mock_db_service.return_value.fetch_data.return_value = [{"allotted": 100, "used": 0, "id": 1}]
        with pytest.raises(HTTPException) as exc:
            await call_function_with_credits(dummy_func, req, credit_type="ai", db=None, current_user=user, credit_amount=1)
        assert exc.value.status_code == 400
        assert "subscription_id required" in str(exc.value.detail)

# Utility: test with fallback subscription_id and credits
@pytest.mark.anyio
async def test_with_real_or_fallback_subscription():
    """
    Try to use a real subscription id/credits, fallback to mock data if not available.
    """
    async def dummy_func(request, user):
        return {"result": "ok"}
    req = MagicMock(spec=Request)
    req.json = AsyncMock(return_value={"subscription_id": "real_or_fallback_subid"})
    user = DummyUser(is_superuser=False)
    with patch.object(type(settings), "db_backend", new=property(lambda self: "supabase")), \
         patch("app.api.utils.credits.supabase.get_database_service") as mock_db_service:
        credits_row = {"allotted": 50, "used": 10, "id": 1}
        mock_db_service.return_value.fetch_data.return_value = [credits_row]
        mock_db_service.return_value.update_data.return_value = None
        result = await call_function_with_credits(dummy_func, req, credit_type="ai", db=None, current_user=user, credit_amount=5)
        assert result["result"] == "ok"

# More tests can be added for Postgres logic, negative credits, etc.
