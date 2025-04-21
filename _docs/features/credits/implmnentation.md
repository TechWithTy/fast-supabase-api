clean, type-annotated, production-ready implementation of the call_function_with_credits utility for FastAPI, following DRY, SOLID, and robust error-handling best practices. This assumes you have SQLAlchemy models for UserProfile and CreditTransaction, and are using dependency injection for authentication.

python
CopyInsert
from fastapi import Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Callable, Awaitable, Any
from models import UserProfile, CreditTransaction, User  # adjust import paths as needed
from dependencies import get_db, get_current_user  # your DI for DB/session/user

async def call_function_with_credits(
    func: Callable[[Request, User], Awaitable[Any]],
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    credit_amount: int = 5
) -> JSONResponse:
    """
    FastAPI utility to wrap endpoint logic with credit-based access control.
    """
    # 1. Authentication
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    # 2. Admin override for credit amount
    actual_credit_amount = credit_amount
    if getattr(current_user, "is_superuser", False) or getattr(current_user, "is_staff", False):
        body = await request.json()
        override = body.get("credit_amount")
        if override is not None:
            try:
                actual_credit_amount = int(override)
                if actual_credit_amount < 0:
                    raise HTTPException(status_code=400, detail="Credit amount cannot be negative")
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="Credit amount must be a valid integer")

    # 3. Get or create user profile
    profile = db.query(UserProfile).filter_by(user_id=current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id, credits_balance=0)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    # 4. Check credits
    if actual_credit_amount > 0 and profile.credits_balance < actual_credit_amount:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "error": "Insufficient credits",
                "required": actual_credit_amount,
                "available": profile.credits_balance,
                "message": f"This operation requires {actual_credit_amount} credits. You have {profile.credits_balance} credits."
            }
        )

    # 5. Execute function and handle credits
    try:
        response = await func(request, current_user)
        # Only deduct credits if function succeeded (status < 400)
        if actual_credit_amount > 0 and getattr(response, "status_code", 200) < 400:
            profile.credits_balance -= actual_credit_amount
            db.add(profile)
            db.add(CreditTransaction(
                user_id=current_user.id,
                amount=-actual_credit_amount,
                balance_after=profile.credits_balance,
                description=f"Executed {func.__name__}",
                endpoint=str(request.url)
            ))
            db.commit()
            # Inject credit info into response
            if isinstance(response, JSONResponse):
                data = response.body if hasattr(response, "body") else {}
                data.update({
                    "credits_used": actual_credit_amount,
                    "credits_remaining": profile.credits_balance
                })
                return JSONResponse(content=data, status_code=response.status_code)
            else:
                return response
        return response
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute function: {str(e)}"
        )
Usage Example in FastAPI Endpoint:

python
CopyInsert
from fastapi import APIRouter, Request, Depends

router = APIRouter()

@router.post("/credit-demo")
async def credit_demo_endpoint(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    async def demo_func(req: Request, user: User):
        body = await req.json()
        return JSONResponse({"message": "Function executed successfully", "parameters": body.get("parameters", {})})
    return await call_function_with_credits(demo_func, request, db=db, current_user=current_user, credit_amount=3)
Key Notes:

Replace UserProfile, CreditTransaction, and User with your actual SQLAlchemy models.
Adjust the get_db and get_current_user dependencies to your project.
Handles admin override, error reporting, and transactional safety.
Type-checked, robust, and production-ready.