"""
test_models.py — Unit tests for Django model behaviour.

Tests cover model save logic, auto-slug generation, property calculations,
and validation for all major models including sports-themed Event objects,
SharXathon hackathons, TechNews articles, NeoProjects, and StartupStories.
"""

import pytest
from datetime import date, time, timedelta
from django.utils import timezone
from django.utils.text import slugify

pytestmark = pytest.mark.django_db


# ===========================================================================
# CustomUser Model
# ===========================================================================
class TestCustomUserModel:
    def test_create_user_with_defaults(self):
        from authentication.models import CustomUser
        user = CustomUser.objects.create_user(
            username="model_user",
            password="ModelPass123!",
        )
        assert user.is_phone_verified is False
        assert user.username == "model_user"

    def test_user_str_returns_username(self):
        from authentication.models import CustomUser
        user = CustomUser.objects.create_user(
            username="str_test_user",
            password="ModelPass123!",
        )
        assert str(user) == "str_test_user"

    def test_superuser_has_staff_flag(self):
        from authentication.models import CustomUser
        admin = CustomUser.objects.create_superuser(
            username="super_model_user",
            password="AdminPass123!",
        )
        assert admin.is_staff is True
        assert admin.is_superuser is True


# ===========================================================================
# Event Model — Sports Focus
# ===========================================================================
class TestEventModel:
    def _make_event(self, **kwargs):
        from authentication.models import Event
        defaults = {
            "name": "Test NFL Game",
            "description": "NFL test event",
            "details": "Detailed NFL test info",
            "event_type": "upcoming",
            "category": "conference",
            "location": "Test Stadium, USA",
            "event_date": date.today() + timedelta(days=10),
            "start_time": time(19, 0),
            "end_time": time(22, 0),
            "featured_image": "https://example.com/img.jpg",
            "is_published": True,
            "benefits": [],
            "key_highlights": [],
            "speakers": [],
        }
        defaults.update(kwargs)
        return Event.objects.create(**defaults)

    def test_event_slug_auto_generated(self):
        event = self._make_event(name="Super Bowl LXI Auto Slug")
        assert event.slug
        assert "super-bowl" in event.slug.lower()

    def test_event_published_at_set_on_publish(self):
        event = self._make_event(is_published=True)
        assert event.published_at is not None

    def test_event_unpublished_has_no_published_at(self):
        event = self._make_event(is_published=False)
        assert event.published_at is None

    def test_event_is_past_event_property_true(self):
        event = self._make_event(event_date=date.today() - timedelta(days=5))
        assert event.is_past_event is True

    def test_event_is_past_event_property_false_for_future(self):
        event = self._make_event(event_date=date.today() + timedelta(days=30))
        assert event.is_past_event is False

    def test_event_days_until_event_returns_correct_value(self):
        event = self._make_event(event_date=date.today() + timedelta(days=14))
        assert event.days_until_event == 14

    def test_event_days_until_event_returns_none_for_past(self):
        event = self._make_event(event_date=date.today() - timedelta(days=1))
        assert event.days_until_event is None

    def test_event_formatted_date_is_string(self):
        event = self._make_event(event_date=date(2026, 7, 19))
        assert event.formatted_date == "July 19, 2026"

    def test_event_is_today_false(self):
        event = self._make_event(event_date=date.today() + timedelta(days=1))
        assert event.is_today is False

    def test_event_is_today_true(self):
        event = self._make_event(event_date=date.today())
        assert event.is_today is True

    def test_event_str_contains_name_and_date(self):
        event = self._make_event(
            name="NFL Conference Championship",
            event_date=date(2026, 1, 19),
        )
        assert "NFL Conference Championship" in str(event)
        assert "2026-01-19" in str(event)

    def test_nba_event_benefits_stored_as_json(self):
        event = self._make_event(
            name="NBA Playoff Game",
            benefits=["Courtside seats", "Official jersey", "Post-game reception"],
        )
        assert len(event.benefits) == 3
        assert "Courtside seats" in event.benefits

    def test_event_ticket_price_decimal(self):
        event = self._make_event(ticket_price="1599.99", is_free=False)
        assert float(event.ticket_price) == 1599.99

    def test_free_event_zero_price(self):
        event = self._make_event(ticket_price="0.00", is_free=True)
        assert event.is_free is True
        assert float(event.ticket_price) == 0.00

    def test_event_unique_slug_per_record(self):
        e1 = self._make_event(name="NFL Wildcard 2026")
        e2 = self._make_event(name="NFL Wildcard 2027")
        assert e1.slug != e2.slug


# ===========================================================================
# SharXathon Model
# ===========================================================================
class TestSharXathonModel:
    def _make_hackathon(self, **kwargs):
        from authentication.models import SharXathon
        now = timezone.now()
        defaults = {
            "name": "Test Hackathon",
            "description": "A test hackathon event",
            "content": "Full hackathon content",
            "location": "Tech Hub",
            "start_datetime": now + timedelta(days=15),
            "end_datetime": now + timedelta(days=16),
            "registration_deadline": now + timedelta(days=10),
            "topic": "AI Innovation",
            "difficulty_level": "intermediate",
            "team_size": "4-5",
            "max_participants": 100,
            "prizes": [{"position": "1st", "prize": "$5000"}],
            "benefits": ["Networking"],
            "rules": ["Original code"],
            "judging_criteria": [{"criteria": "Innovation", "weight": "40%"}],
            "is_published": True,
        }
        defaults.update(kwargs)
        return SharXathon.objects.create(**defaults)

    def test_hackathon_slug_auto_generated(self):
        h = self._make_hackathon(name="NeoSharX AI Hackathon")
        assert h.slug
        assert "neosharx" in h.slug.lower()

    def test_hackathon_str(self):
        h = self._make_hackathon(name="Spring Hackathon", location="Online")
        assert "Spring Hackathon" in str(h)

    def test_hackathon_is_registration_open(self):
        h = self._make_hackathon()
        assert h.is_registration_open is True

    def test_hackathon_participation_percentage_zero(self):
        h = self._make_hackathon(max_participants=100, current_participants=0)
        assert h.participation_percentage == 0

    def test_hackathon_participation_percentage_half(self):
        h = self._make_hackathon(max_participants=100, current_participants=50)
        assert h.participation_percentage == 50.0

    def test_hackathon_participation_percentage_capped_at_100(self):
        h = self._make_hackathon(max_participants=10, current_participants=200)
        assert h.participation_percentage == 100


# ===========================================================================
# TechNews Model
# ===========================================================================
class TestTechNewsModel:
    def _make_article(self, **kwargs):
        from authentication.models import TechNews
        defaults = {
            "title": f"Tech Article {timezone.now().timestamp()}",
            "excerpt": "Brief excerpt for testing.",
            "content": "<p>Full content.</p>",
            "category": "ai_ml",
            "is_published": True,
        }
        defaults.update(kwargs)
        return TechNews.objects.create(**defaults)

    def test_article_slug_auto_generated(self):
        a = self._make_article(title="Breaking AI News Today")
        assert a.slug
        assert "breaking" in a.slug.lower()

    def test_article_published_at_set_on_save(self):
        a = self._make_article(is_published=True)
        assert a.published_at is not None

    def test_article_engagement_score_calculation(self):
        a = self._make_article()
        a.views_count = 100
        a.likes_count = 20
        a.shares_count = 5
        # score = views*1 + likes*5 + shares*10 = 100 + 100 + 50 = 250
        assert a.engagement_score == 250

    def test_article_is_recent_false_for_old_article(self):
        a = self._make_article()
        from datetime import timedelta
        a.published_at = timezone.now() - timedelta(days=2)
        assert a.is_recent is False

    def test_article_str_is_title(self):
        a = self._make_article(title="Quantum Computing Breakthrough")
        assert str(a) == "Quantum Computing Breakthrough"

    def test_article_get_absolute_url(self):
        a = self._make_article(title="Cloud Native Revolution")
        assert a.get_absolute_url().startswith("/tech/")


# ===========================================================================
# NeoProject Model
# ===========================================================================
class TestNeoProjectModel:
    def _make_project(self, **kwargs):
        from authentication.models import NeoProject
        defaults = {
            "title": f"Project {timezone.now().timestamp()}",
            "description": "Test project description",
            "category": "ai_ml",
            "technologies": "Python, TensorFlow, React",
            "status": "in_development",
            "difficulty_level": "intermediate",
            "features": ["Auth", "API", "Dashboard"],
            "is_published": True,
        }
        defaults.update(kwargs)
        return NeoProject.objects.create(**defaults)

    def test_project_slug_auto_generated(self):
        p = self._make_project(title="Sports Analytics Platform")
        assert p.slug
        assert "sports" in p.slug.lower()

    def test_technology_list_property(self):
        p = self._make_project(technologies="Python, Django, React")
        assert "Python" in p.technology_list
        assert "Django" in p.technology_list
        assert "React" in p.technology_list

    def test_tag_list_property(self):
        p = self._make_project(tags="nba, nfl, analytics")
        assert "nba" in p.tag_list
        assert "nfl" in p.tag_list

    def test_project_str_is_title(self):
        p = self._make_project(title="NFL Stats Engine")
        assert str(p) == "NFL Stats Engine"

    def test_project_is_open_source_default(self):
        p = self._make_project()
        assert p.is_open_source is True


# ===========================================================================
# StartupStory Model
# ===========================================================================
class TestStartupStoryModel:
    def _make_story(self, **kwargs):
        from authentication.models import StartupStory
        defaults = {
            "heading": f"Story {timezone.now().timestamp()}",
            "summary": "A brief startup summary.",
            "content": "<p>Full story content.</p>",
            "key_takeaways": "Lesson 1\nLesson 2",
            "company_name": "TestCo",
            "industry": "technology",
            "stage": "seed",
            "is_published": True,
        }
        defaults.update(kwargs)
        return StartupStory.objects.create(**defaults)

    def test_story_slug_auto_generated(self):
        s = self._make_story(heading="How We Built NBA Stats App")
        assert s.slug
        assert "nba" in s.slug.lower()

    def test_story_published_at_set(self):
        s = self._make_story(is_published=True)
        assert s.published_at is not None

    def test_story_str_is_heading(self):
        s = self._make_story(heading="The Football Startup Journey")
        assert str(s) == "The Football Startup Journey"


# ===========================================================================
# YouTubeVideo Model
# ===========================================================================
class TestYouTubeVideoModel:
    def test_extract_video_id_standard_url(self):
        from authentication.models import YouTubeVideo
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        vid_id = YouTubeVideo.extract_video_id(url)
        assert vid_id == "dQw4w9WgXcQ"

    def test_extract_video_id_short_url(self):
        from authentication.models import YouTubeVideo
        url = "https://youtu.be/dQw4w9WgXcQ"
        vid_id = YouTubeVideo.extract_video_id(url)
        assert vid_id == "dQw4w9WgXcQ"

    def test_extract_video_id_shorts_url(self):
        from authentication.models import YouTubeVideo
        url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
        vid_id = YouTubeVideo.extract_video_id(url)
        assert vid_id == "dQw4w9WgXcQ"

    def test_extract_video_id_invalid_url_returns_empty(self):
        from authentication.models import YouTubeVideo
        vid_id = YouTubeVideo.extract_video_id("https://example.com/not-youtube")
        assert vid_id == ""

    def test_video_save_sets_embed_url(self):
        from authentication.models import YouTubeVideo
        v = YouTubeVideo.objects.create(
            title="NFL Highlights 2026",
            youtube_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            video_id="",
            video_type="video",
            is_published=True,
        )
        assert "youtube.com/embed/dQw4w9WgXcQ" in v.embed_url

    def test_video_auto_thumbnail_generated(self):
        from authentication.models import YouTubeVideo
        v = YouTubeVideo.objects.create(
            title="NBA Dunk Compilation",
            youtube_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            video_id="",
            video_type="video",
            is_published=True,
        )
        assert "dQw4w9WgXcQ" in v.auto_thumbnail
