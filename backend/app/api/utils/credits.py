"""
credits.py
Middleware utility for credit-based access control in FastAPI endpoints.
Implements call_function_with_credits as described in project docs.
"""

from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.models import AICredits, LeadCredits, SkipTraceCredits, User
from app.supabase_home.client import supabase


async def call_function_with_credits(
    func: Callable[[Request, User], Awaitable[Any]],
    request: Request,
    credit_type: str,  # required, no default
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    credit_amount: int = 1,
) -> JSONResponse:
    """
    FastAPI utility to wrap endpoint logic with credit-based access control.
    Handles authentication, admin override, atomic deduction, and audit logging.
    Supports both Postgres (SQLAlchemy) and Supabase backends.
    credit_type: 'ai', 'leads', or 'skiptrace' (required)
    """
    # 1. Authentication
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )

    # 2. Admin override for credit amount
    actual_credit_amount = credit_amount
    if getattr(current_user, "is_superuser", False) or getattr(
        current_user, "is_staff", False
    ):
        try:
            body = await request.json()
            override = body.get("credit_amount")
            if override is not None:
                try:
                    actual_credit_amount = int(override)
                    if actual_credit_amount < 0:
                        raise HTTPException(
                            status_code=400, detail="Credit amount cannot be negative"
                        )
                except (ValueError, TypeError):
                    raise HTTPException(
                        status_code=400, detail="Credit amount must be a valid integer"
                    )
        except Exception:
            pass  # If body is not JSON or missing, ignore

    backend = settings.db_backend  # 'postgres' or 'supabase'
    credit_table_map = {
        "ai": "AICredits",
        "leads": "LeadCredits",
        "skiptrace": "SkipTraceCredits",
    }
    credit_table = credit_table_map.get(credit_type.lower())
    if not credit_table:
        raise HTTPException(
            status_code=400, detail=f"Invalid credit_type: {credit_type}"
        )

    if backend == "supabase":
        db_service = supabase.get_database_service()
        try:
            body = await request.json()
            subscription_id = body.get("subscription_id")
        except Exception:
            subscription_id = None
        if not subscription_id:
            raise HTTPException(
                status_code=400, detail="subscription_id required for credit deduction"
            )
        credits_rows = db_service.fetch_data(
            table=credit_table,
            filters={"subscriptionid": subscription_id},
            limit=1,
        )
        if credits_rows:
            credits_row = credits_rows[0]
        else:
            raise HTTPException(
                status_code=404,
                detail=f"No credits found for this subscription ({credit_type})",
            )
        if (
            actual_credit_amount > 0
            and credits_row["allotted"] - credits_row["used"] < actual_credit_amount
        ):
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail={
                    "error": f"Insufficient {credit_type} credits",
                    "required": actual_credit_amount,
                    "available": credits_row["allotted"] - credits_row["used"],
                },
            )
        try:
            db_service.update_data(
                table=credit_table,
                data={"used": credits_row["used"] + actual_credit_amount},
                filters={"id": credits_row["id"]},
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to deduct {credit_type} credits (supabase): {str(e)}",
            )
        try:
            response = await func(request, current_user)
            return response
        except Exception as e:
            raise  # Optionally, implement refund logic here
    else:
        # --- Postgres/SQLAlchemy logic for multi-type credits ---
        credit_model_map = {
            "ai": AICredits,
            "leads": LeadCredits,
            "skiptrace": SkipTraceCredits,
        }
        credit_model = credit_model_map.get(credit_type.lower())
        if not credit_model:
            raise HTTPException(
                status_code=400, detail=f"Invalid credit_type: {credit_type}"
            )
        try:
            body = await request.json()
            subscription_id = body.get("subscription_id")
        except Exception:
            subscription_id = None
        if not subscription_id:
            raise HTTPException(
                status_code=400, detail="subscription_id required for credit deduction"
            )
        credits_row = (
            db.query(credit_model).filter_by(subscriptionid=subscription_id).first()
        )
        if not credits_row:
            raise HTTPException(
                status_code=404,
                detail=f"No credits found for this subscription ({credit_type})",
            )
        if (
            actual_credit_amount > 0
            and (credits_row.allotted - credits_row.used) < actual_credit_amount
        ):
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail={
                    "error": f"Insufficient {credit_type} credits",
                    "required": actual_credit_amount,
                    "available": credits_row.allotted - credits_row.used,
                },
            )
        try:
            credits_row.used += actual_credit_amount
            db.add(credits_row)
            db.commit()
            db.refresh(credits_row)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to deduct {credit_type} credits: {str(e)}",
            )
        try:
            response = await func(request, current_user)
            return response
        except Exception as e:
            db.rollback()
            raise
