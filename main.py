"""Acme Coffee Club API.

Every answer comes straight from acme/settings.py, so the app and the
Acme Help Center always tell customers the same thing.
"""

from datetime import date, timedelta

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

from acme import settings

app = FastAPI(
    title="Acme Coffee Club API",
    version="1.0.0",
    description="Demo coffee subscription app. Business settings live in acme/settings.py.",
)

_members: dict[str, dict] = {}


def reset_store() -> None:
    """Forget every member (used by the tests)."""
    _members.clear()


@app.get("/plans")
def list_plans():
    """The plans you can pick, with monthly prices in US dollars."""
    return {"plans": settings.PLANS}


@app.get("/trial")
def trial():
    """How long the free trial lasts."""
    return {"free_trial_days": settings.FREE_TRIAL_DAYS}


@app.get("/shipping/countries")
def shipping_countries():
    """Countries we ship to."""
    return {"countries": settings.SHIPPING_COUNTRIES}


@app.get("/support/hours")
def support_hours():
    """When the support team is available."""
    return {"support_hours": settings.SUPPORT_HOURS}


@app.get("/features")
def features():
    """Optional app features that are switched on or off."""
    return {"dark_mode": settings.DARK_MODE_ENABLED}


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    plan: str = "Free"


@app.post("/signup", status_code=201)
def signup(body: SignupRequest):
    """Create an account. Passwords must be at least PASSWORD_MIN_LENGTH characters."""
    if len(body.password) < settings.PASSWORD_MIN_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters.",
        )
    plan_names = [p["name"] for p in settings.PLANS]
    if body.plan not in plan_names:
        raise HTTPException(status_code=400, detail=f"Plan must be one of: {', '.join(plan_names)}.")
    if body.email in _members:
        raise HTTPException(status_code=409, detail="That email already has an account.")
    trial_ends = date.today() + timedelta(days=settings.FREE_TRIAL_DAYS)
    _members[body.email] = {"email": body.email, "plan": body.plan}
    return {"email": body.email, "plan": body.plan, "trial_ends_on": trial_ends.isoformat()}


class RefundRequest(BaseModel):
    order_id: str
    order_date: date


@app.post("/refunds", status_code=201)
def request_refund(body: RefundRequest):
    """Ask for a refund. Orders older than REFUND_WINDOW_DAYS can't be refunded."""
    age_days = (date.today() - body.order_date).days
    if age_days < 0:
        raise HTTPException(status_code=400, detail="Order date can't be in the future.")
    if age_days > settings.REFUND_WINDOW_DAYS:
        raise HTTPException(
            status_code=400,
            detail=f"Refunds are only available within {settings.REFUND_WINDOW_DAYS} days of your order.",
        )
    return {"order_id": body.order_id, "status": "approved"}
