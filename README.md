# Acme Coffee Club

A tiny demo app for **Acme Coffee Club**, a made-up coffee subscription. It's built with [FastAPI](https://fastapi.tiangolo.com/) and is part of the [Mintlify demo org](https://github.com/mintlify-demo).

Customer help lives in the **Acme Help Center**: [https://mintlify-demo.mintlify.site/acme](https://mintlify-demo.mintlify.site/acme) (public, no sign-in).

## The one file that matters

Every business rule is in [`acme/settings.py`](acme/settings.py), written in plain English:

| Setting | Today |
| --- | --- |
| `FREE_TRIAL_DAYS` | 14 days |
| `PLANS` | Free $0 (1 bag/month), Pro $12/month (3 bags), Team $29/month per person |
| `SHIPPING_COUNTRIES` | United States, Mexico |
| `REFUND_WINDOW_DAYS` | 30 days |
| `SUPPORT_HOURS` | Monday-Friday, 9am-5pm Pacific |
| `PASSWORD_MIN_LENGTH` | 8 characters |
| `DARK_MODE_ENABLED` | No |

Change a line there, open a pull request, and Mintlify's *Update from code changes* automation updates the Help Center to match.

## What the app does

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/plans` | Lists the plans and prices |
| `GET` | `/trial` | How long the free trial lasts |
| `GET` | `/shipping/countries` | Countries we ship to |
| `GET` | `/support/hours` | When support is open |
| `GET` | `/features` | Which optional features (like dark mode) are on |
| `POST` | `/signup` | Creates an account; rejects passwords shorter than `PASSWORD_MIN_LENGTH` |
| `POST` | `/refunds` | Requests a refund; rejects orders older than `REFUND_WINDOW_DAYS` |

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload        # http://localhost:8000  (Swagger UI at /docs)
```

## Test it

```bash
python -m pytest -q
```

## Docs

The Help Center pages live in the [`docs` repo, under `acme/`](https://github.com/mintlify-demo/docs/tree/main/acme), not here. This repo holds only code and tests.
