"""
factories.py — Lightweight model factories for test data creation.

Uses plain Django ORM (no factory_boy dependency) so tests work
out of the box with only the packages already in requirements.txt
plus pytest-django.
"""

from datetime import date, time, timedelta
from django.utils import timezone
import uuid


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def _uid(prefix: str = "") -> str:
    """Return a short unique string, optionally prefixed."""
    return f"{prefix}{uuid.uuid4().hex[:8]}"


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
class UserFactory:
    @staticmethod
    def create(**kwargs):
        from authentication.models import CustomUser
        defaults = {
            "username": _uid("user_"),
            "email": f"{_uid()}@test.io",
            "password": "TestPass123!",
        }
        defaults.update(kwargs)
        password = defaults.pop("password")
        user = CustomUser(**defaults)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def create_admin(**kwargs):
        from authentication.models import CustomUser
        defaults = {
            "username": _uid("admin_"),
            "email": f"{_uid()}@admin.io",
            "password": "AdminPass123!",
            "is_staff": True,
            "is_superuser": True,
        }
        defaults.update(kwargs)
        password = defaults.pop("password")
        user = CustomUser(**defaults)
        user.set_password(password)
        user.save()
        return user


# ---------------------------------------------------------------------------
# Sports Events — NFL, NBA, Football / Soccer
# ---------------------------------------------------------------------------
class SportEventFactory:
    """Factory for creating sports-themed Event objects."""

    SPORT_PRESETS = {
        "nfl": {
            "category": "conference",
            "location": "NFL Stadium, USA",
            "organizer_name": "NFL",
            "organizer_email": "events@nfl.com",
            "is_free": False,
            "ticket_price": "250.00",
        },
        "nba": {
            "category": "conference",
            "location": "NBA Arena, USA",
            "organizer_name": "NBA",
            "organizer_email": "events@nba.com",
            "is_free": False,
            "ticket_price": "150.00",
        },
        "football": {
            "category": "conference",
            "location": "Stadium, Europe",
            "organizer_name": "FIFA / UEFA",
            "organizer_email": "events@fifa.com",
            "is_free": False,
            "ticket_price": "95.00",
        },
    }

    @classmethod
    def create(cls, sport: str = "nfl", event_type: str = "upcoming", **kwargs):
        from authentication.models import Event

        preset = cls.SPORT_PRESETS.get(sport, cls.SPORT_PRESETS["nfl"])
        name = kwargs.pop("name", f"{sport.upper()} Event {_uid()}")
        event_date = kwargs.pop(
            "event_date",
            date.today() + timedelta(days=30) if event_type == "upcoming"
            else date.today() - timedelta(days=10),
        )

        defaults = {
            **preset,
            "name": name,
            "description": f"Professional {sport.upper()} sporting event.",
            "details": f"Full details for {name}.",
            "event_type": event_type,
            "event_date": event_date,
            "start_time": time(19, 0),
            "end_time": time(22, 0),
            "event_timezone": "UTC",
            "featured_image": f"https://cdn.neosharx.io/sports/{sport}-event.jpg",
            "is_published": True,
            "is_featured": False,
            "benefits": ["Live entertainment", "Fan experience"],
            "key_highlights": ["Top-tier athletes", "World-class venue"],
            "speakers": [],
        }
        defaults.update(kwargs)
        return Event.objects.create(**defaults)

    # Convenience shortcuts
    @classmethod
    def nfl(cls, **kwargs):
        return cls.create(sport="nfl", **kwargs)

    @classmethod
    def nba(cls, **kwargs):
        return cls.create(sport="nba", **kwargs)

    @classmethod
    def football(cls, **kwargs):
        return cls.create(sport="football", **kwargs)

    @classmethod
    def batch(cls, count: int = 3, sport: str = "nfl", **kwargs):
        return [cls.create(sport=sport, **kwargs) for _ in range(count)]


# ---------------------------------------------------------------------------
# Tech News
# ---------------------------------------------------------------------------
class TechNewsFactory:
    @staticmethod
    def create(**kwargs):
        from authentication.models import TechNews
        slug = _uid("tech-")
        defaults = {
            "title": f"Tech Article {_uid()}",
            "slug": slug,
            "excerpt": "Short excerpt for the article.",
            "content": "<p>Full article content goes here.</p>",
            "category": "ai_ml",
            "is_published": True,
            "is_featured": False,
            "priority": "medium",
        }
        defaults.update(kwargs)
        return TechNews.objects.create(**defaults)


# ---------------------------------------------------------------------------
# SharXathon (Hackathon)
# ---------------------------------------------------------------------------
class SharXathonFactory:
    @staticmethod
    def create(**kwargs):
        from authentication.models import SharXathon
        slug = _uid("hackathon-")
        now = timezone.now()
        defaults = {
            "name": f"SharXathon {_uid()}",
            "slug": slug,
            "description": "Hackathon for innovators.",
            "content": "Full hackathon details.",
            "location": "Tech Hub, San Francisco",
            "is_virtual": False,
            "start_datetime": now + timedelta(days=15),
            "end_datetime": now + timedelta(days=16),
            "registration_deadline": now + timedelta(days=10),
            "topic": "AI Innovation",
            "difficulty_level": "intermediate",
            "team_size": "4-5",
            "max_participants": 100,
            "prizes": [{"position": "1st", "prize": "$5000"}],
            "benefits": ["Networking", "Mentorship"],
            "rules": ["Teams of 4-5", "Original code only"],
            "judging_criteria": [{"criteria": "Innovation", "weight": "40%"}],
            "is_published": True,
            "is_featured": False,
            "status": "registration_open",
        }
        defaults.update(kwargs)
        return SharXathon.objects.create(**defaults)


# ---------------------------------------------------------------------------
# StartupStory
# ---------------------------------------------------------------------------
class StartupStoryFactory:
    @staticmethod
    def create(**kwargs):
        from authentication.models import StartupStory
        slug = _uid("story-")
        defaults = {
            "heading": f"Startup Story {_uid()}",
            "slug": slug,
            "summary": "Brief summary of this startup journey.",
            "content": "<p>Full startup story content.</p>",
            "key_takeaways": "Lesson 1\nLesson 2\nLesson 3",
            "company_name": f"StartupCo {_uid()}",
            "industry": "technology",
            "stage": "seed",
            "is_published": True,
            "is_featured": False,
        }
        defaults.update(kwargs)
        return StartupStory.objects.create(**defaults)


# ---------------------------------------------------------------------------
# NeoProject
# ---------------------------------------------------------------------------
class NeoProjectFactory:
    @staticmethod
    def create(**kwargs):
        from authentication.models import NeoProject
        slug = _uid("project-")
        defaults = {
            "title": f"Neo Project {_uid()}",
            "slug": slug,
            "description": "Innovative project description.",
            "category": "ai_ml",
            "technologies": "Python, Django, React",
            "status": "in_development",
            "difficulty_level": "intermediate",
            "features": ["Feature A", "Feature B"],
            "is_published": True,
            "is_featured": False,
        }
        defaults.update(kwargs)
        return NeoProject.objects.create(**defaults)
