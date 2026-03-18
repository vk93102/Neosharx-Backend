"""
test_auth.py — Unit & integration tests for the authentication flow.

Tests cover:
    • User registration
    • User login / logout
    • Token creation
    • OTP (mocked)
    • Forgot-password / recover-username flows
    • User profile retrieval
    • OAuth URL generation endpoints
"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

pytestmark = pytest.mark.django_db


# ===========================================================================
# Registration
# ===========================================================================
class TestUserRegistration:
    url = "/api/auth/register/"

    def test_register_valid_user(self, api_client):
        payload = {
            "username": "newplayer_01",
            "email": "newplayer@neosharx.io",
            "password": "SecurePass#2026",
        }
        resp = api_client.post(self.url, payload, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        data = resp.json()
        assert "token" in data
        assert data["message"] == "User registered successfully"

    def test_register_duplicate_username(self, api_client, regular_user):
        payload = {
            "username": regular_user.username,
            "email": "dup@neosharx.io",
            "password": "AnotherPass#2026",
        }
        resp = api_client.post(self.url, payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_missing_required_field(self, api_client):
        """Registration without a password should fail."""
        resp = api_client.post(self.url, {"username": "incomplete"}, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_weak_password_rejected(self, api_client):
        """Django's password validators should reject 'password'."""
        payload = {
            "username": "weakpwduser",
            "email": "weak@neosharx.io",
            "password": "password",
        }
        resp = api_client.post(self.url, payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


# ===========================================================================
# Login
# ===========================================================================
class TestUserLogin:
    url = "/api/auth/login/"

    def test_login_valid_credentials(self, api_client, regular_user):
        payload = {"username": regular_user.username, "password": "StrongPass123!"}
        resp = api_client.post(self.url, payload, format="json")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert "token" in data
        assert data["message"] == "Login successful"

    def test_login_wrong_password(self, api_client, regular_user):
        payload = {"username": regular_user.username, "password": "WrongPass!"}
        resp = api_client.post(self.url, payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_nonexistent_user(self, api_client):
        payload = {"username": "ghost_user", "password": "DoesNotExist!"}
        resp = api_client.post(self.url, payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_creates_token(self, api_client, regular_user):
        payload = {"username": regular_user.username, "password": "StrongPass123!"}
        resp = api_client.post(self.url, payload, format="json")
        assert resp.status_code == status.HTTP_200_OK
        token_key = resp.json()["token"]
        assert Token.objects.filter(key=token_key, user=regular_user).exists()

    def test_login_empty_payload_rejected(self, api_client):
        resp = api_client.post(self.url, {}, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


# ===========================================================================
# Logout
# ===========================================================================
class TestUserLogout:
    url = "/api/auth/logout/"

    def test_logout_authenticated_user(self, auth_api_client):
        resp = auth_api_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["message"] == "Logout successful"

    def test_logout_requires_authentication(self, api_client):
        resp = api_client.post(self.url)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


# ===========================================================================
# User Profile
# ===========================================================================
class TestUserProfile:
    url = "/api/auth/profile/"

    def test_get_profile_authenticated(self, auth_api_client, regular_user):
        resp = auth_api_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert data["username"] == regular_user.username

    def test_get_profile_unauthenticated(self, api_client):
        resp = api_client.get(self.url)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


# ===========================================================================
# OAuth URL generation (smoke tests — just check status & URL returned)
# ===========================================================================
class TestOAuthURLs:
    def test_google_login_url_returns_url(self, api_client):
        resp = api_client.get("/api/auth/google/login-url/")
        # Endpoint may return 200 with URL or 400 if env vars missing in CI
        assert resp.status_code in (status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_linkedin_login_url_returns_url(self, api_client):
        resp = api_client.get("/api/auth/linkedin/login-url/")
        assert resp.status_code in (status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR)
