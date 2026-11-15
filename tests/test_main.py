from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from acme import settings
from main import app, reset_store


@pytest.fixture()
def client():
    reset_store()
    return TestClient(app)


def test_plans(client):
    plans = client.get("/plans").json()["plans"]
    assert [p["name"] for p in plans] == ["Free", "Pro", "Team"]
    assert [p["price_per_month"] for p in plans] == [0, 12, 29]
    assert plans == settings.PLANS


def test_trial(client):
    assert client.get("/trial").json() == {"free_trial_days": settings.FREE_TRIAL_DAYS}


def test_shipping(client):
    assert client.get("/shipping/countries").json() == {"countries": settings.SHIPPING_COUNTRIES}


def test_support_hours(client):
    assert client.get("/support/hours").json() == {"support_hours": settings.SUPPORT_HOURS}


def test_features(client):
    assert client.get("/features").json() == {"dark_mode": settings.DARK_MODE_ENABLED}


def test_signup_ok(client):
    r = client.post("/signup", json={"email": "sam@example.com", "password": "x" * settings.PASSWORD_MIN_LENGTH})
    assert r.status_code == 201
    expected = date.today() + timedelta(days=settings.FREE_TRIAL_DAYS)
    assert r.json() == {"email": "sam@example.com", "plan": "Free", "trial_ends_on": expected.isoformat()}


def test_signup_short_password(client):
    r = client.post("/signup", json={"email": "sam@example.com", "password": "x" * (settings.PASSWORD_MIN_LENGTH - 1)})
    assert r.status_code == 400
    assert str(settings.PASSWORD_MIN_LENGTH) in r.json()["detail"]


def test_signup_unknown_plan_and_duplicate(client):
    good = {"email": "sam@example.com", "password": "correct-horse"}
    assert client.post("/signup", json={**good, "plan": "Gold"}).status_code == 400
    assert client.post("/signup", json=good).status_code == 201
    assert client.post("/signup", json=good).status_code == 409


def test_refund_inside_window(client):
    edge = date.today() - timedelta(days=settings.REFUND_WINDOW_DAYS)
    r = client.post("/refunds", json={"order_id": "A-100", "order_date": edge.isoformat()})
    assert r.status_code == 201 and r.json()["status"] == "approved"


def test_refund_outside_window(client):
    late = date.today() - timedelta(days=settings.REFUND_WINDOW_DAYS + 1)
    r = client.post("/refunds", json={"order_id": "A-101", "order_date": late.isoformat()})
    assert r.status_code == 400
    assert str(settings.REFUND_WINDOW_DAYS) in r.json()["detail"]


def test_refund_future_date(client):
    future = date.today() + timedelta(days=1)
    assert client.post("/refunds", json={"order_id": "A-102", "order_date": future.isoformat()}).status_code == 400
