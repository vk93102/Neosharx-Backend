"""
backend/test_settings.py — CI / test-safe Django settings.

Used automatically by pytest via ``DJANGO_SETTINGS_MODULE = backend.test_settings``
(see pytest.ini).  No external services, no real credentials, no file-based DB.
"""

import os

# ── Step 1: set required env vars BEFORE NFA_Football.settings is imported ──
# decouple.config() reads these when the NFA_Football settings module loads.
_TEST_ENV = {
    "SECRET_KEY": "test-secret-key-not-for-production",
    "TWILIO_ACCOUNT_SID": "ACtest000000000000000000000000000000",
    "TWILIO_AUTH_TOKEN": "test_token_000000000000000000000000",
    "TWILIO_VERIFY_SERVICE_SID": "VAtest000000000000000000000000000000",
    "LINKEDIN_CLIENT_ID": "ci_linkedin_client_id",
    "LINKEDIN_CLIENT_SECRET": "ci_linkedin_client_secret",
    "GOOGLE_CLIENT_ID": "ci_google_client_id",
    "GOOGLE_CLIENT_SECRET": "ci_google_client_secret",
    "DATABASE_URL": "",  # forces SQLite fallback in NFA_Football.settings
}
for _k, _v in _TEST_ENV.items():
    os.environ.setdefault(_k, _v)

# ── Step 2: pull in all production settings ──────────────────────────────────
from NFA_Football.settings import *  # noqa: F401, F403, E402

# ── Step 3: override with test-safe values ───────────────────────────────────

SECRET_KEY = "test-secret-key-not-for-production"
DEBUG = True
ALLOWED_HOSTS = ["*", "testserver", "localhost", "127.0.0.1"]

# Fast, isolated, in-memory SQLite — wiped after every test run
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable security middleware that breaks the DRF test client
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0

# Mock Twilio — no real SMS sent during tests
USE_MOCK_OTP = True
MOCK_OTP_CODE = "123456"

# Silence deploy-checklist warnings that are irrelevant in CI
SILENCED_SYSTEM_CHECKS = [
    "security.W004",
    "security.W008",
    "security.W009",
    "security.W012",
]
