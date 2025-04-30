"""
FastAPI router for Stripe-related endpoints. These routes match the logic and robustness of the previous Django APIViews.

- Uses SQLAlchemy models for StripeCustomer, StripeSubscription, StripePlan
- Uses shared Stripe utility functions
- Handles errors, validation, and dynamic URLs
"""

import logging
import os
from datetime import datetime
from typing import Any

from backend.app.stripe_home.api.config import get_stripe_client
from backend.app.stripe_home.api.credit import (
    allocate_subscription_credits,
    handle_subscription_change,
    map_plan_to_subscription_tier,
)
from backend.app.stripe_home.api.models import (
    StripeCustomer,
    StripePlan,
    StripeSubscription,
)
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.caching.utils.redis_cache import get_or_set_cache

# --- DB Session Dependency (adjust as needed for your project) ---
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stripe", tags=["stripe"])


# --- User Dependency Placeholder ---
def get_current_user():
    # Replace with your authentication logic
    return {
        "id": 1,
        "username": "demo",
        "email": "demo@example.com",
        "stripe_customer_id": "cus_test",
    }


# --- Checkout Session Endpoint ---
@router.post("/subscription/checkout/{plan_id}")
async def subscription_checkout(
    plan_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user),
    success_url: str | None = Body(default=None),
    cancel_url: str | None = Body(default=None),
    customer_id: str | None = Body(default=None),
):
    """Create Stripe Checkout Session for a subscription plan."""
    plan = (
        db.query(StripePlan)
        .filter(StripePlan.id == plan_id, StripePlan.active)
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    stripe = get_stripe_client()
    # Get or create customer
    if customer_id:
        customer = (
            db.query(StripeCustomer)
            .filter(StripeCustomer.customer_id == customer_id)
            .first()
        )
        if not customer:
            raise HTTPException(status_code=404, detail="Customer ID not found")
        customer_id_val = customer.customer_id
    else:
        customer = (
            db.query(StripeCustomer)
            .filter(StripeCustomer.user_id == user["id"])
            .first()
        )
        if not customer:
            # Create Stripe customer and DB record
            stripe_customer = stripe.Customer.create(
                email=user["email"],
                name=user.get("username"),
                metadata={"user_id": str(user["id"])},
            )
            customer = StripeCustomer(
                user_id=user["id"],
                customer_id=stripe_customer.id,
                livemode=not os.environ.get("STRIPE_SECRET_KEY", "").startswith(
                    "sk_test_"
                ),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)
        customer_id_val = customer.customer_id
    # Set URLs
    base_url = os.environ.get("BASE_URL", "https://example.com")
    default_success_url = (
        f"{base_url}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}"
    )
    default_cancel_url = f"{base_url}/subscription/cancel"
    # Create checkout session
    try:
        session = stripe.checkout.Session.create(
            customer=customer_id_val,
            line_items=[{"price": plan.plan_id, "quantity": 1}],
            mode="subscription",
            success_url=success_url or default_success_url,
            cancel_url=cancel_url or default_cancel_url,
            allow_promotion_codes=True,
            billing_address_collection="required",
            customer_email=user["email"] if not customer_id else None,
            client_reference_id=str(user["id"]),
            metadata={
                "plan_id": str(plan.id),
                "plan_name": plan.name,
                "user_id": str(user["id"]),
            },
        )
        return {"checkout_url": session.url}
    except Exception as e:
        logger.error(f"Stripe error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# --- Programmable Checkout Session Endpoint ---
@router.post("/checkout/programmable/")
async def programmable_checkout(
    request: Request,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user),
    payload: dict = Body(...),
):
    """Create a programmable Stripe Checkout Session."""
    mode = payload.get("mode", "subscription")
    if mode not in ["subscription", "payment", "setup"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid mode. Must be subscription, payment, or setup",
        )
    stripe = get_stripe_client()
    # Get or create customer
    customer = (
        db.query(StripeCustomer).filter(StripeCustomer.user_id == user["id"]).first()
    )
    if not customer:
        stripe_customer = stripe.Customer.create(
            email=user["email"],
            name=user.get("username"),
            metadata={"user_id": str(user["id"])},
        )
        customer = StripeCustomer(
            user_id=user["id"],
            customer_id=stripe_customer.id,
            livemode=not os.environ.get("STRIPE_SECRET_KEY", "").startswith("sk_test_"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
    customer_id = customer.customer_id
    session_params = {
        "customer": customer_id,
        "mode": mode,
        "client_reference_id": str(user["id"]),
        "metadata": {"user_id": str(user["id"])},
    }
    # URLs
    base_url = os.environ.get("BASE_URL", "https://example.com")
    session_params["success_url"] = (
        payload.get("success_url")
        or os.environ.get("STRIPE_SUCCESS_URL")
        or f"{base_url}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}"
    )
    session_params["cancel_url"] = (
        payload.get("cancel_url")
        or os.environ.get("STRIPE_CANCEL_URL")
        or f"{base_url}/subscription/cancel"
    )
    # Line items
    line_items = []
    if mode == "subscription":
        plan_id = payload.get("plan_id")
        if not plan_id:
            raise HTTPException(
                status_code=400, detail="plan_id is required for subscription mode"
            )
        plan = (
            db.query(StripePlan)
            .filter(StripePlan.plan_id == plan_id, StripePlan.active)
            .first()
        )
        if plan:
            session_params["metadata"]["plan_id"] = str(plan.id)
            session_params["metadata"]["plan_name"] = plan.name
        line_items.append({"price": plan_id, "quantity": payload.get("quantity", 1)})
    elif mode == "payment":
        amount = payload.get("amount")
        currency = payload.get("currency", "usd")
        product_name = payload.get("product_name", "One-time payment")
        if not amount:
            raise HTTPException(
                status_code=400, detail="amount is required for payment mode"
            )
        try:
            amount_in_cents = int(float(amount) * 100)
        except ValueError:
            raise HTTPException(status_code=400, detail="amount must be a valid number")
        line_items.append(
            {
                "price_data": {
                    "currency": currency.lower(),
                    "product_data": {"name": product_name},
                    "unit_amount": amount_in_cents,
                },
                "quantity": 1,
            }
        )
        session_params["metadata"]["payment_description"] = product_name
        session_params["metadata"]["amount"] = str(amount)
        session_params["metadata"]["currency"] = currency.lower()
    # Add line items
    if mode != "setup":
        session_params["line_items"] = line_items
    # Optional params
    if payload.get("allow_promotion_codes", True):
        session_params["allow_promotion_codes"] = True
    if payload.get("billing_address_collection", True):
        session_params["billing_address_collection"] = "required"
    if payload.get("tax_id_collection", False):
        session_params["tax_id_collection"] = {"enabled": True}
    # Advanced customization
    for k in ["ui_mode", "custom_text", "custom_fields", "payment_method_types"]:
        if payload.get(k):
            session_params[k] = payload[k]
    try:
        checkout_session = stripe.checkout.Session.create(**session_params)
        return {"sessionId": checkout_session.id, "url": checkout_session.url}
    except Exception as e:
        logger.error(f"Stripe error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# --- Customer Portal Endpoint ---
@router.post("/customer-portal/")
async def customer_portal(
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user),
    return_url: str | None = Body(default=None),
):
    stripe = get_stripe_client()
    customer = (
        db.query(StripeCustomer).filter(StripeCustomer.user_id == user["id"]).first()
    )
    if not customer:
        raise HTTPException(
            status_code=404, detail="No Stripe customer found for this user"
        )
    try:
        session = stripe.billing_portal.Session.create(
            customer=customer.customer_id,
            return_url=return_url
            or os.environ.get(
                "PORTAL_RETURN_URL", "https://example.com/account/subscriptions/"
            ),
        )
        return {"portal_url": session.url}
    except Exception as e:
        logger.error(f"Stripe error creating customer portal: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# --- Webhook Endpoint ---
@router.post("/webhook/")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    stripe = get_stripe_client()
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    endpoint_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return JSONResponse(status_code=400, content={"error": str(e)})
    logger.info(f"Stripe webhook received: {event['type']} - {event['id']}")

    # --- Event Routing ---
    event_type = event["type"]
    obj = event["data"]["object"]
    try:
        if event_type == "checkout.session.completed":
            # Handle new checkout session (subscription signup)
            user_id = obj.get("client_reference_id")
            customer_id = obj.get("customer")
            subscription_id = obj.get("subscription")
            plan_id = None
            if subscription_id:
                sub = stripe.Subscription.retrieve(subscription_id)
                if sub and sub["items"]["data"]:
                    plan_id = sub["items"]["data"][0]["price"]["id"]
            # Find user and plan in DB
            user = db.query(StripeCustomer).filter(StripeCustomer.customer_id == customer_id).first()
            plan = db.query(StripePlan).filter(StripePlan.plan_id == plan_id).first() if plan_id else None
            if user and plan:
                # Map plan name to subscription tier
                subscription_tier = map_plan_to_subscription_tier(plan.name)
                logger.info(f"User {user_id} assigned to tier: {subscription_tier}")
                allocate_subscription_credits(user, plan.initial_credits, f"Initial credits for {plan.name}", subscription_id)
            logger.info(f"Processed checkout.session.completed for user {user_id}")

        elif event_type == "customer.subscription.created":
            subscription_id = obj["id"]
            customer_id = obj["customer"]
            plan_id = obj["items"]["data"][0]["price"]["id"]
            status = obj["status"]
            # Find or create subscription in DB
            sub = db.query(StripeSubscription).filter(StripeSubscription.subscription_id == subscription_id).first()
            user = db.query(StripeCustomer).filter(StripeCustomer.customer_id == customer_id).first()
            plan = db.query(StripePlan).filter(StripePlan.plan_id == plan_id).first()
            if not sub and user and plan:
                # Map plan name to subscription tier
                subscription_tier = map_plan_to_subscription_tier(plan.name)
                logger.info(f"User {user.user_id} assigned to tier: {subscription_tier}")
                sub = StripeSubscription(
                    subscription_id=subscription_id,
                    user_id=user.user_id,
                    status=status,
                    plan_id=plan_id,
                    current_period_start=datetime.fromtimestamp(obj["current_period_start"]),
                    current_period_end=datetime.fromtimestamp(obj["current_period_end"]),
                    livemode=obj.get("livemode", False),
                )
                db.add(sub)
                db.commit()
                allocate_subscription_credits(user, plan.initial_credits, f"Initial credits for {plan.name}", subscription_id)
            logger.info(f"Processed customer.subscription.created for {subscription_id}")

        elif event_type == "customer.subscription.updated":
            subscription_id = obj["id"]
            customer_id = obj["customer"]
            plan_id = obj["items"]["data"][0]["price"]["id"]
            status = obj["status"]
            sub = db.query(StripeSubscription).filter(StripeSubscription.subscription_id == subscription_id).first()
            user = db.query(StripeCustomer).filter(StripeCustomer.customer_id == customer_id).first()
            plan = db.query(StripePlan).filter(StripePlan.plan_id == plan_id).first()
            if sub and user and plan:
                old_plan_id = sub.plan_id
                if old_plan_id != plan_id:
                    old_plan = db.query(StripePlan).filter(StripePlan.plan_id == old_plan_id).first()
                    old_tier = map_plan_to_subscription_tier(old_plan.name) if old_plan else None
                    new_tier = map_plan_to_subscription_tier(plan.name)
                    logger.info(f"User {user.user_id} changed from tier {old_tier} to {new_tier}")
                    handle_subscription_change(user, old_plan, plan, subscription_id)
                sub.plan_id = plan_id
                sub.status = status
                sub.current_period_start = datetime.fromtimestamp(obj["current_period_start"])
                sub.current_period_end = datetime.fromtimestamp(obj["current_period_end"])
                db.commit()
            logger.info(f"Processed customer.subscription.updated for {subscription_id}")

        elif event_type == "customer.subscription.deleted":
            subscription_id = obj["id"]
            sub = db.query(StripeSubscription).filter(StripeSubscription.subscription_id == subscription_id).first()
            if sub:
                sub.status = obj["status"]
                db.commit()
            logger.info(f"Processed customer.subscription.deleted for {subscription_id}")

        elif event_type == "invoice.payment_succeeded":
            subscription_id = obj.get("subscription")
            if subscription_id:
                sub = db.query(StripeSubscription).filter(StripeSubscription.subscription_id == subscription_id).first()
                if sub:
                    plan = db.query(StripePlan).filter(StripePlan.plan_id == sub.plan_id).first()
                    user = db.query(StripeCustomer).filter(StripeCustomer.user_id == sub.user_id).first()
                    if plan and user:
                        allocate_subscription_credits(user, plan.monthly_credits, f"Monthly credits for {plan.name}", subscription_id)
            logger.info(f"Processed invoice.payment_succeeded for subscription {subscription_id}")

        elif event_type == "invoice.payment_failed":
            subscription_id = obj.get("subscription")
            if subscription_id:
                sub = db.query(StripeSubscription).filter(StripeSubscription.subscription_id == subscription_id).first()
                if sub:
                    sub.status = "past_due"
                    db.commit()
            logger.info(f"Processed invoice.payment_failed for subscription {subscription_id}")

        # Add more event handlers as needed
        return {"status": "success", "event": event_type}
    except Exception as e:
        logger.error(f"Error handling webhook event {event_type}: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e), "event": event_type})


# --- Dashboard Endpoint (stub) ---
@router.get("/dashboard/")
async def customer_dashboard(
    db: Session = Depends(get_db), user: Any = Depends(get_current_user)
):
    cache_key = f"stripe:dashboard:{user['id']}"
    def fetch():
        # TODO: Implement dashboard logic (subscriptions, payment methods, etc.)
        return {"message": "Customer dashboard data."}
    dashboard_data = get_or_set_cache(cache_key, fetch, expire_seconds=120)
    return dashboard_data


# --- Products Endpoint ---
@router.get("/products/")
async def product_management(user: Any = Depends(get_current_user)):
    cache_key = f"stripe:products"
    def fetch():
        stripe = get_stripe_client()
        return stripe.Product.list(active=True).data
    products = get_or_set_cache(cache_key, fetch, expire_seconds=300)
    return {"products": products}
