"""
conftest.py — Pytest fixtures shared across the entire test suite.

All fixtures use Django's TestCase / pytest-django semantics so every test
runs inside a database transaction that is rolled back after each test,
keeping the test database clean.

Settings are provided by backend.test_settings (see pytest.ini).
No settings manipulation is needed here.
"""

import pytest


# ---------------------------------------------------------------------------
# REST Framework test client
# ---------------------------------------------------------------------------
@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def auth_api_client(db, api_client, regular_user):
    """Authenticated APIClient using token auth."""
    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=regular_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client


# ---------------------------------------------------------------------------
# User fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def regular_user(db):
    from authentication.models import CustomUser
    user = CustomUser.objects.create_user(
        username="testplayer",
        password="StrongPass123!",
        email="testplayer@neosharx.io",
        first_name="Test",
        last_name="Player",
    )
    return user


@pytest.fixture
def admin_user(db):
    from authentication.models import CustomUser
    user = CustomUser.objects.create_superuser(
        username="admin_test",
        password="AdminPass123!",
        email="admin@neosharx.io",
    )
    return user


@pytest.fixture
def admin_api_client(db, api_client, admin_user):
    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client


# ---------------------------------------------------------------------------
# Sports-related Event fixtures (NFL / NBA / Football)
# ---------------------------------------------------------------------------
@pytest.fixture
def nfl_super_bowl_event(db, admin_user):
    """NFL Super Bowl LX — upcoming event fixture."""
    from datetime import date, time
    from authentication.models import Event

    return Event.objects.create(
        name="NFL Super Bowl LX",
        description="The 60th edition of the NFL Super Bowl championship game.",
        details=(
            "Super Bowl LX will be played at Allegiant Stadium in Las Vegas, NV. "
            "Two of the AFC and NFC's best teams will compete for the Lombardi Trophy "
            "in the biggest annual sporting event in the United States."
        ),
        event_type="upcoming",
        category="conference",
        location="Allegiant Stadium, Las Vegas, NV",
        is_virtual=False,
        event_date=date(2026, 2, 8),
        start_time=time(18, 30),
        end_time=time(22, 0),
        event_timezone="America/Los_Angeles",
        featured_image="https://cdn.neosharx.io/events/super-bowl-lx.jpg",
        is_free=False,
        ticket_price="950.00",
        organizer_name="NFL",
        organizer_email="events@nfl.com",
        is_published=True,
        is_featured=True,
        benefits=[
            "Live entertainment & halftime show",
            "Fan zone access",
            "Official merchandise bag",
        ],
        key_highlights=[
            "60th anniversary Super Bowl",
            "World-class halftime performance",
            "Record attendance expected",
        ],
        speakers=[],
        created_by=admin_user,
    )


@pytest.fixture
def nba_finals_event(db, admin_user):
    """NBA Finals 2026 — upcoming event fixture."""
    from datetime import date, time
    from authentication.models import Event

    return Event.objects.create(
        name="NBA Finals 2026",
        description="The NBA Finals 2026 — battle for the Larry O'Brien Championship Trophy.",
        details=(
            "The NBA Finals is the annual championship series of the NBA. "
            "Top two teams from the Eastern and Western Conferences face off "
            "in a best-of-seven series. This year's Finals promises to be one "
            "for the history books."
        ),
        event_type="upcoming",
        category="conference",
        location="Chase Center, San Francisco, CA",
        is_virtual=False,
        event_date=date(2026, 6, 4),
        start_time=time(20, 0),
        end_time=time(23, 30),
        event_timezone="America/Los_Angeles",
        featured_image="https://cdn.neosharx.io/events/nba-finals-2026.jpg",
        is_free=False,
        ticket_price="1200.00",
        organizer_name="NBA",
        organizer_email="events@nba.com",
        is_published=True,
        is_featured=True,
        benefits=[
            "VIP courtside experience available",
            "Official NBA Finals merchandise",
            "Post-game trophy ceremony access",
        ],
        key_highlights=[
            "Best-of-7 series",
            "2025–26 season champion crowned",
            "Global live stream on NBA League Pass",
        ],
        speakers=[],
        created_by=admin_user,
    )


@pytest.fixture
def premier_league_event(db, admin_user):
    """Premier League Manchester Derby — past event fixture."""
    from datetime import date, time
    from authentication.models import Event

    return Event.objects.create(
        name="Premier League Manchester Derby",
        description="The legendary Manchester City vs Manchester United clash.",
        details=(
            "One of the most fiercely contested fixtures in world football. "
            "Both clubs meet at the Etihad Stadium in a critical top-of-the-table "
            "showdown with title implications on both sides."
        ),
        event_type="past",
        category="conference",
        location="Etihad Stadium, Manchester, UK",
        is_virtual=False,
        event_date=date(2025, 12, 14),
        start_time=time(16, 30),
        end_time=time(18, 30),
        event_timezone="Europe/London",
        featured_image="https://cdn.neosharx.io/events/man-derby-2025.jpg",
        is_free=False,
        ticket_price="85.00",
        organizer_name="Premier League",
        organizer_email="events@premierleague.com",
        is_published=True,
        is_featured=False,
        benefits=[
            "Match-day programme",
            "Stadium tour access (pre-match)",
        ],
        key_highlights=[
            "150th Manchester Derby",
            "Title-race implications",
            "Full stadium atmosphere",
        ],
        speakers=[],
        created_by=admin_user,
    )


@pytest.fixture
def nfl_draft_event(db, admin_user):
    """NFL Draft 2026 — recent event fixture."""
    from datetime import date, time
    from authentication.models import Event

    return Event.objects.create(
        name="NFL Draft 2026",
        description="The 2026 NFL Draft — 32 teams pick the next generation of stars.",
        details=(
            "The annual NFL Draft takes place over three days, where franchises "
            "select college players to bolster their rosters. The 2026 draft class "
            "is widely considered one of the deepest in a decade."
        ),
        event_type="recent",
        category="conference",
        location="Caesars Superdome, New Orleans, LA",
        is_virtual=False,
        event_date=date(2026, 4, 23),
        start_time=time(20, 0),
        end_time=time(23, 0),
        event_timezone="America/Chicago",
        featured_image="https://cdn.neosharx.io/events/nfl-draft-2026.jpg",
        is_free=True,
        ticket_price="0.00",
        organizer_name="NFL",
        organizer_email="draft@nfl.com",
        is_published=True,
        is_featured=True,
        benefits=[
            "Free general admission",
            "Live radio broadcast",
            "Fan interactive zone",
            "Player meet-and-greet opportunities",
        ],
        key_highlights=[
            "7 rounds over 3 days",
            "All 32 teams represented",
            "Live ESPN/NFL Network coverage",
        ],
        speakers=[],
        created_by=admin_user,
    )


@pytest.fixture
def fifa_world_cup_event(db, admin_user):
    """FIFA World Cup 2026 Final — upcoming event fixture."""
    from datetime import date, time
    from authentication.models import Event

    return Event.objects.create(
        name="FIFA World Cup 2026 Final",
        description="The grand finale of the 2026 FIFA World Cup hosted in North America.",
        details=(
            "For the first time in history, the FIFA World Cup Final will be held at "
            "MetLife Stadium in East Rutherford, New Jersey. 48 nations competed "
            "across the USA, Canada, and Mexico in the first expanded 48-team edition."
        ),
        event_type="upcoming",
        category="conference",
        location="MetLife Stadium, East Rutherford, NJ",
        is_virtual=False,
        event_date=date(2026, 7, 19),
        start_time=time(15, 0),
        end_time=time(18, 30),
        event_timezone="America/New_York",
        featured_image="https://cdn.neosharx.io/events/wc2026-final.jpg",
        is_free=False,
        ticket_price="2500.00",
        organizer_name="FIFA",
        organizer_email="worldcup2026@fifa.com",
        is_published=True,
        is_featured=True,
        benefits=[
            "Official World Cup Final experience",
            "Commemorative ticket & merchandise",
            "Trophy ceremony attendance",
            "Post-match celebrations",
        ],
        key_highlights=[
            "First 48-team World Cup",
            "Tri-nation co-hosted tournament",
            "Largest sports event of 2026",
        ],
        speakers=[],
        created_by=admin_user,
    )


@pytest.fixture
def nba_allstar_event(db, admin_user):
    """NBA All-Star Weekend 2026 — upcoming event fixture."""
    from datetime import date, time
    from authentication.models import Event

    return Event.objects.create(
        name="NBA All-Star Weekend 2026",
        description="Three days of star-powered NBA entertainment in San Francisco.",
        details=(
            "NBA All-Star Weekend features the Slam Dunk Contest, Three-Point Contest, "
            "Rising Stars Game, and culminates with the All-Star Game itself. "
            "The Golden State Warriors host this year's celebrations at Chase Center."
        ),
        event_type="upcoming",
        category="conference",
        location="Chase Center, San Francisco, CA",
        is_virtual=False,
        event_date=date(2026, 2, 15),
        start_time=time(19, 0),
        end_time=time(23, 0),
        event_timezone="America/Los_Angeles",
        featured_image="https://cdn.neosharx.io/events/nba-allstar-2026.jpg",
        is_free=False,
        ticket_price="500.00",
        organizer_name="NBA",
        organizer_email="allstar@nba.com",
        is_published=True,
        is_featured=False,
        benefits=[
            "All-Star Game ticket",
            "Skills competition access",
            "Fan experience zone",
        ],
        key_highlights=[
            "Slam Dunk Contest",
            "Three-Point Contest",
            "Celebrity All-Star Game",
        ],
        speakers=[],
        created_by=admin_user,
    )


@pytest.fixture
def all_sports_events(
    nfl_super_bowl_event,
    nba_finals_event,
    premier_league_event,
    nfl_draft_event,
    fifa_world_cup_event,
    nba_allstar_event,
):
    """Convenience fixture — all six sports events at once."""
    return [
        nfl_super_bowl_event,
        nba_finals_event,
        premier_league_event,
        nfl_draft_event,
        fifa_world_cup_event,
        nba_allstar_event,
    ]
