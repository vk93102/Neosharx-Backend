"""
backend/wsgi.py — WSGI application entry-point proxy.
WSGI_APPLICATION = 'backend.wsgi.application' in settings.py points here.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

application = get_wsgi_application()
