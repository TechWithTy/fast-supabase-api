"""
credits.py
Middleware utility for credit-based access control in FastAPI endpoints.
Implements call_function_with_credits as described in project docs.
"""

from datetime import datetime
from typing import Any, Awaitable, Callable

from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models import CreditTransaction, User, UserProfile
from app.core.config import settings
from app.supabase_home.client import supabase
from app.supabase_home.functions.database import SupabaseDatabaseService

async def call_function_with_credits(
    func: Callable[[Request, User], Awaitable[Any]],
    request: Request,
    db: Session | SupabaseDatabaseService = Depends(get_db),
    current_user: User = Depends(get_current_user),
    credit_amount: int = 5
) -> JSONResponse:
    """
    FastAPI utility to wrap endpoint logic with credit-based access control.
    Handles authentication, admin override, atomic deduction, and audit logging.
    Supports both Postgres (SQLAlchemy) and Supabase backends.
    """
    # 1. Authentication
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    # 2. Admin override for credit amount
    actual_credit_amount = credit_amount
    if getattr(current_user, "is_superuser", False) or getattr(current_user, "is_staff", False):
        try:
            body = await request.json()
            override = body.get("credit_amount")
            if override is not None:
                try:
                    actual_credit_amount = int(override)
                    if actual_credit_amount < 0:
                        raise HTTPException(status_code=400, detail="Credit amount cannot be negative")
                except (ValueError, TypeError):
                    raise HTTPException(status_code=400, detail="Credit amount must be a valid integer")
        except Exception:
            pass  # If body is not JSON or missing, ignore

    backend = settings.db_backend  # 'postgres' or 'supabase'
    if backend == "supabase":
        db_service = supabase.get_database_service()
        # 3. Get or create user profile
        profiles = db_service.fetch_data(
            table="user_profile",
            filters={"user_id": str(current_user.id)},
            limit=1,
        )
        if profiles:
            profile = profiles[0]
        else:
            profile = db_service.insert_data(
                table="user_profile",
                data={"user_id": str(current_user.id), "credits_balance": 0},
            )[0]
        # 4. Check credits
        if actual_credit_amount > 0 and profile["credits_balance"] < actual_credit_amount:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail={
                    "error": "Insufficient credits",
                    "required": actual_credit_amount,
                    "available": profile["credits_balance"],
                },
            )
        # 5. Deduct credits and create transaction
        try:
            db_service.update_data(
                table="user_profile",
                data={"credits_balance": profile["credits_balance"] - actual_credit_amount},
                filters={"id": profile["id"]},
            )
            db_service.insert_data(
                table="credit_transaction",
                data={
                    "user_profile_id": profile["id"],
                    "amount": -actual_credit_amount,
                    "transaction_type": "deduct",
                    "description": f"Used {actual_credit_amount} credits for endpoint {request.url.path}",
                },
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to deduct credits (supabase): {str(e)}")
        # 6. Call the wrapped endpoint logic
        try:
            response = await func(request, current_user)
            return response
        except Exception as e:
            raise  # Optionally, implement refund logic here
    else:
        # --- Postgres/SQLAlchemy logic (unchanged) ---
        profile = db.query(UserProfile).filter_by(user_id=current_user.id).first()
        if not profile:
            profile = UserProfile(user_id=current_user.id, credits_balance=0)
            db.add(profile)
            db.commit()
            db.refresh(profile)
        if actual_credit_amount > 0 and profile.credits_balance < actual_credit_amount:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail={
                    "error": "Insufficient credits",
                    "required": actual_credit_amount,
                    "available": profile.credits_balance,
                },
            )
        try:
            profile.credits_balance -= actual_credit_amount
            profile.updated_at = datetime.utcnow()
            db.add(profile)
            db.add(CreditTransaction(
                user_profile_id=profile.id,
                amount=-actual_credit_amount,
                transaction_type="deduct",
                description=f"Used {actual_credit_amount} credits for endpoint {request.url.path}",
                created_at=datetime.utcnow(),
            ))
            db.commit()
            db.refresh(profile)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to deduct credits: {str(e)}")
        try:
            response = await func(request, current_user)
            return response
        except Exception as e:
            db.rollback()
            raise
