"""
backend/urls.py — URL configuration proxy.

ROOT_URLCONF = 'backend.urls' in settings.py points here.
We delegate to NFA_Football/urls.py which holds the canonical URL patterns.
"""

from NFA_Football.urls import urlpatterns  # noqa: F401

__all__ = ["urlpatterns"]
