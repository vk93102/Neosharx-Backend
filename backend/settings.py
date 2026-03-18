"""
backend/settings.py — Proxy module for NFA_Football.settings.

The Django project was originally named 'backend'; this shim satisfies
``DJANGO_SETTINGS_MODULE = backend.settings`` without duplicating code.

For test environments, use backend.test_settings instead (see pytest.ini).
"""

import os

# Set safe placeholder defaults so this module can be imported even when
# a .env file is absent (e.g. Docker build stage, CI lint step, etc.).
# Real credentials come from .env or the host environment.
_PLACEHOLDERS = {
    "TWILIO_ACCOUNT_SID": "ACplaceholder000000000000000000000000",
    "TWILIO_AUTH_TOKEN": "placeholder_token_000000000000000000",
    "TWILIO_VERIFY_SERVICE_SID": "VAplaceholder000000000000000000000000",
    "LINKEDIN_CLIENT_ID": "placeholder_linkedin_id",
    "LINKEDIN_CLIENT_SECRET": "placeholder_linkedin_secret",
    "GOOGLE_CLIENT_ID": "placeholder_google_id",
    "GOOGLE_CLIENT_SECRET": "placeholder_google_secret",
    "SECRET_KEY": "django-insecure-placeholder-change-in-production",
}
for _k, _v in _PLACEHOLDERS.items():
    os.environ.setdefault(_k, _v)

# Delegate to the canonical settings module in NFA_Football/.
from NFA_Football.settings import *  # noqa: F401, F403, E402
