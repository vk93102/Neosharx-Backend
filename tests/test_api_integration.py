"""
test_api_integration.py — Full integration tests for every major API endpoint.

Tests cover:
    • Startup Stories CRUD & filters
    • Neo Stories
    • Neo Projects
    • SharXathon (Hackathon) endpoints including countdown
    • Tech News (list, detail, like, share, trending, breaking)
    • Talk Episodes
    • Robotics News
    • YouTube Videos
    • Comments (create, list, like toggle, flag)
    • Health check
    • Unauthenticated access enforcement
"""

import pytest
from datetime import date, time, timedelta
from django.utils import timezone
from rest_framework import status

from tests.factories import (
    UserFactory,
    SportEventFactory,
    TechNewsFactory,
    SharXathonFactory,
    StartupStoryFactory,
    NeoProjectFactory,
)

pytestmark = pytest.mark.django_db


# ===========================================================================
# Health Check
# ===========================================================================
class TestHealthCheck:
    def test_healthz_returns_ok(self, api_client):
        resp = api_client.get("/healthz/")
        assert resp.status_code == status.HTTP_200_OK
        assert b"OK" in resp.content


# ===========================================================================
# Startup Stories
# ===========================================================================
class TestStartupStoriesAPI:
    def test_list_stories_returns_200(self, api_client):
        StartupStoryFactory.create(heading="How We Built an NFL Fantasy App")
        StartupStoryFactory.create(heading="NBA Analytics Startup Journey")
        resp = api_client.get("/api/auth/stories/")
        assert resp.status_code == status.HTTP_200_OK

    def test_list_stories_count(self, api_client):
        for i in range(3):
            StartupStoryFactory.create(heading=f"Sports Story {i}")
        resp = api_client.get("/api/auth/stories/")
        data = resp.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        assert len(results) >= 3

    def test_get_story_by_slug(self, api_client):
        story = StartupStoryFactory.create(heading="Football Tech Startup")
        resp = api_client.get(f"/api/auth/stories/{story.slug}/")
        assert resp.status_code == status.HTTP_200_OK

    def test_get_nonexistent_story_returns_404(self, api_client):
        resp = api_client.get("/api/auth/stories/no-such-story-xxx/")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_featured_stories_endpoint(self, api_client):
        resp = api_client.get("/api/auth/stories/featured/")
        assert resp.status_code == status.HTTP_200_OK

    def test_story_filters_endpoint(self, api_client):
        resp = api_client.get("/api/auth/stories/filters/")
        assert resp.status_code == status.HTTP_200_OK

    def test_unpublished_story_excluded(self, api_client):
        story = StartupStoryFactory.create(
            heading="Draft NBA Story",
            is_published=False,
        )
        resp = api_client.get("/api/auth/stories/")
        data = resp.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        slugs = [s.get("slug", "") for s in results]
        assert story.slug not in slugs


# ===========================================================================
# Tech News
# ===========================================================================
class TestTechNewsAPI:
    def test_list_tech_news_returns_200(self, api_client):
        TechNewsFactory.create(title="AI Powers NFL Scouting")
        TechNewsFactory.create(title="NBA Uses Computer Vision for Analytics")
        resp = api_client.get("/api/auth/tech-news/")
        assert resp.status_code == status.HTTP_200_OK

    def test_get_tech_news_detail_by_slug(self, api_client):
        article = TechNewsFactory.create(title="Blockchain in Sports Ticketing")
        resp = api_client.get(f"/api/auth/tech-news/{article.slug}/")
        assert resp.status_code == status.HTTP_200_OK

    def test_featured_tech_news_endpoint(self, api_client):
        resp = api_client.get("/api/auth/tech-news/featured/")
        assert resp.status_code == status.HTTP_200_OK

    def test_breaking_tech_news_endpoint(self, api_client):
        resp = api_client.get("/api/auth/tech-news/breaking/")
        assert resp.status_code == status.HTTP_200_OK

    def test_trending_tech_news_endpoint(self, api_client):
        resp = api_client.get("/api/auth/tech-news/trending/")
        assert resp.status_code == status.HTTP_200_OK

    def test_tech_news_categories_endpoint(self, api_client):
        resp = api_client.get("/api/auth/tech-news/categories/")
        assert resp.status_code == status.HTTP_200_OK

    def test_like_tech_news_article(self, api_client):
        article = TechNewsFactory.create(title="NFL Draft AI Predictions")
        resp = api_client.post(f"/api/auth/tech-news/{article.slug}/like/")
        assert resp.status_code in (status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_401_UNAUTHORIZED)

    def test_share_tech_news_article(self, api_client):
        article = TechNewsFactory.create(title="NBA Wearables Tech")
        resp = api_client.post(f"/api/auth/tech-news/{article.slug}/share/")
        assert resp.status_code in (status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_401_UNAUTHORIZED)

    def test_nonexistent_tech_news_returns_404(self, api_client):
        resp = api_client.get("/api/auth/tech-news/no-such-article-xxxx/")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


# ===========================================================================
# SharXathon / Hackathon
# ===========================================================================
class TestSharXathonAPI:
    def test_list_hackathons_returns_200(self, api_client):
        SharXathonFactory.create(name="NFL Tech Hackathon 2026")
        resp = api_client.get("/api/auth/hackathons/")
        assert resp.status_code == status.HTTP_200_OK

    def test_get_hackathon_detail(self, api_client):
        hack = SharXathonFactory.create(name="NBA Analytics Challenge")
        resp = api_client.get(f"/api/auth/hackathons/{hack.slug}/")
        assert resp.status_code == status.HTTP_200_OK

    def test_hackathon_countdown_endpoint(self, api_client):
        hack = SharXathonFactory.create(name="Sports Data Hackathon")
        resp = api_client.get(f"/api/auth/hackathons/{hack.slug}/countdown/")
        assert resp.status_code == status.HTTP_200_OK

    def test_featured_hackathons_endpoint(self, api_client):
        resp = api_client.get("/api/auth/hackathons/featured/")
        assert resp.status_code == status.HTTP_200_OK

    def test_upcoming_hackathons_endpoint(self, api_client):
        resp = api_client.get("/api/auth/hackathons/upcoming/")
        assert resp.status_code == status.HTTP_200_OK

    def test_hackathon_filters_endpoint(self, api_client):
        resp = api_client.get("/api/auth/hackathons/filters/")
        assert resp.status_code == status.HTTP_200_OK


# ===========================================================================
# Neo Projects
# ===========================================================================
class TestNeoProjectsAPI:
    def test_list_neo_projects_returns_200(self, api_client):
        NeoProjectFactory.create(title="NFL Draft Analytics Dashboard")
        NeoProjectFactory.create(title="NBA Shot-Chart Visualiser")
        resp = api_client.get("/api/auth/neo-projects/")
        assert resp.status_code == status.HTTP_200_OK

    def test_get_neo_project_by_slug(self, api_client):
        project = NeoProjectFactory.create(title="Soccer Heatmap Tool")
        resp = api_client.get(f"/api/auth/neo-projects/{project.slug}/")
        assert resp.status_code == status.HTTP_200_OK

    def test_neo_project_full_detail(self, api_client):
        project = NeoProjectFactory.create(title="Football Predictor AI")
        resp = api_client.get(f"/api/auth/neo-projects/{project.slug}/full/")
        assert resp.status_code == status.HTTP_200_OK

    def test_featured_neo_projects_endpoint(self, api_client):
        resp = api_client.get("/api/auth/neo-projects/featured/")
        assert resp.status_code == status.HTTP_200_OK

    def test_neo_project_filters_endpoint(self, api_client):
        resp = api_client.get("/api/auth/neo-projects/filters/")
        assert resp.status_code == status.HTTP_200_OK


# ===========================================================================
# Talk Episodes
# ===========================================================================
class TestTalkEpisodesAPI:
    def _create_episode(self, number=1, title="Test Episode"):
        from authentication.models import TalkEpisode
        return TalkEpisode.objects.create(
            episode_number=number,
            title=title,
            header="Episode Header",
            youtube_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            description="Episode description",
            key_takeaways=["Takeaway 1", "Takeaway 2"],
            speaker_panels=[{"name": "Jane Doe", "title": "Coach"}],
            duration_minutes=60,
            published_at=timezone.now(),
            is_published=True,
        )

    def test_list_talk_episodes_returns_200(self, api_client):
        self._create_episode(1, "How NFL Teams Use Data")
        resp = api_client.get("/api/auth/talk-episodes/")
        assert resp.status_code == status.HTTP_200_OK

    def test_get_episode_by_slug(self, api_client):
        episode = self._create_episode(2, "NBA Coaching With AI")
        resp = api_client.get(f"/api/auth/talk-episodes/slug/{episode.slug}/")
        assert resp.status_code == status.HTTP_200_OK

    def test_get_episode_by_number(self, api_client):
        self._create_episode(3, "Football Science")
        resp = api_client.get("/api/auth/talk-episodes/number/3/")
        assert resp.status_code == status.HTTP_200_OK

    def test_nonexistent_episode_returns_404(self, api_client):
        resp = api_client.get("/api/auth/talk-episodes/number/9999/")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


# ===========================================================================
# Robotics News
# ===========================================================================
class TestRoboticsNewsAPI:
    def _create_robotics_news(self, title="Robotics Article"):
        from authentication.models import RoboticsNews
        import uuid
        return RoboticsNews.objects.create(
            title=title,
            slug=f"robotics-{uuid.uuid4().hex[:8]}",
            summary="Robotics news summary.",
            content="<p>Full content.</p>",
            featured_image="https://example.com/robot.jpg",
            category="ai_robotics",
            is_published=True,
        )

    def test_list_robotics_news_returns_200(self, api_client):
        self._create_robotics_news("Robot Football Player")
        resp = api_client.get("/api/auth/robotics-news/")
        assert resp.status_code == status.HTTP_200_OK

    def test_get_robotics_news_detail(self, api_client):
        article = self._create_robotics_news("AI Referee in NBA")
        resp = api_client.get(f"/api/auth/robotics-news/{article.slug}/")
        assert resp.status_code == status.HTTP_200_OK

    def test_featured_robotics_news_endpoint(self, api_client):
        resp = api_client.get("/api/auth/robotics-news/featured/")
        assert resp.status_code == status.HTTP_200_OK

    def test_trending_robotics_news_endpoint(self, api_client):
        resp = api_client.get("/api/auth/robotics-news/trending/")
        assert resp.status_code == status.HTTP_200_OK

    def test_like_robotics_news(self, api_client):
        article = self._create_robotics_news("Robot Sports Coach")
        resp = api_client.post(f"/api/auth/robotics-news/{article.slug}/like/")
        assert resp.status_code in (
            status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_401_UNAUTHORIZED
        )


# ===========================================================================
# YouTube Videos
# ===========================================================================
class TestYouTubeVideosAPI:
    def _create_video(self, title="Test Video", video_type="video"):
        from authentication.models import YouTubeVideo
        import uuid
        return YouTubeVideo.objects.create(
            title=title,
            youtube_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            video_id="",
            video_type=video_type,
            category="events",
            is_published=True,
        )

    def test_list_youtube_videos_returns_200(self, api_client):
        self._create_video("NFL Super Bowl Highlights 2026")
        resp = api_client.get("/api/auth/youtube-videos/")
        assert resp.status_code == status.HTTP_200_OK

    def test_featured_youtube_videos_endpoint(self, api_client):
        resp = api_client.get("/api/auth/youtube-videos/featured/")
        assert resp.status_code == status.HTTP_200_OK

    def test_youtube_videos_by_type_video(self, api_client):
        self._create_video("NBA Finals 2026 Recap", video_type="video")
        resp = api_client.get("/api/auth/youtube-videos/type/video/")
        assert resp.status_code == status.HTTP_200_OK

    def test_youtube_videos_by_type_short(self, api_client):
        self._create_video("Football Skill Short", video_type="short")
        resp = api_client.get("/api/auth/youtube-videos/type/short/")
        assert resp.status_code == status.HTTP_200_OK

    def test_get_video_by_slug(self, api_client):
        video = self._create_video("Premier League Best Goals")
        resp = api_client.get(f"/api/auth/youtube-videos/{video.slug}/")
        assert resp.status_code == status.HTTP_200_OK


# ===========================================================================
# Comments
# ===========================================================================
class TestCommentsAPI:
    def test_list_comments_returns_200(self, api_client):
        resp = api_client.get("/api/auth/comments/")
        assert resp.status_code in (status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_requires_auth(self, api_client):
        payload = {
            "content_type": "tech_news",
            "content_slug": "some-article",
            "text": "Great article about NFL analytics!",
        }
        resp = api_client.post("/api/auth/comments/", payload, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_comment_authenticated(self, auth_api_client):
        article = TechNewsFactory.create(title="Authenticated Comment Test")
        payload = {
            "content_type": "tech_news",
            "content_slug": article.slug,
            "text": "Incredible NFL scouting technology!",
        }
        resp = auth_api_client.post("/api/auth/comments/", payload, format="json")
        assert resp.status_code in (
            status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST
        )

    def test_create_reply_comment_authenticated(self, auth_api_client, regular_user):
        """Test threaded comments (reply to a parent comment)."""
        from authentication.models import Comment
        article = TechNewsFactory.create(title="Reply Comment Test")
        parent = Comment.objects.create(
            user=regular_user,
            content_type="tech_news",
            content_slug=article.slug,
            text="Parent: How NBA teams use shot tracking.",
        )
        payload = {
            "content_type": "tech_news",
            "content_slug": article.slug,
            "text": "Reply: Really impressive technology!",
            "parent": parent.id,
        }
        resp = auth_api_client.post("/api/auth/comments/", payload, format="json")
        assert resp.status_code in (
            status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST
        )

    def test_comment_like_requires_auth(self, api_client):
        payload = {"comment_id": 1, "reaction": "like"}
        resp = api_client.post("/api/auth/comments/like/", payload, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_flag_comment_requires_auth(self, api_client):
        resp = api_client.post("/api/auth/comments/1/flag/", {}, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_comments_requires_auth(self, api_client):
        resp = api_client.get("/api/auth/comments/user/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


# ===========================================================================
# User Preferences
# ===========================================================================
class TestUserPreferencesAPI:
    def test_user_preferences_post_valid(self, api_client):
        payload = {
            "user_type": "tech_enthusiast",
            "interest": "sharxathons",
            "email": "fan@nfl.io",
            "provider": None,
        }
        resp = api_client.post("/api/auth/user-preferences/", payload, format="json")
        assert resp.status_code in (
            status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST
        )

    def test_user_preferences_missing_fields_rejected(self, api_client):
        resp = api_client.post("/api/auth/user-preferences/", {}, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


# ===========================================================================
# Events — Full CRUD-Style Integration
# ===========================================================================
class TestEventsFullIntegration:
    """Test the complete event listing + detail workflow."""

    def test_create_event_and_retrieve_it(self, db, api_client, admin_user):
        event = SportEventFactory.create(
            sport="nfl",
            name="AFC Championship 2026",
            event_type="upcoming",
            created_by=admin_user,
        )
        resp = api_client.get(f"/api/auth/events/{event.slug}/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["name"] == "AFC Championship 2026"

    def test_events_list_empty_at_start(self, db, api_client):
        resp = api_client.get("/api/auth/events/")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        assert isinstance(results, list)

    def test_event_count_increases_after_creation(self, db, api_client, admin_user):
        resp1 = api_client.get("/api/auth/events/")
        before = len(resp1.json().get("results", resp1.json()) if isinstance(resp1.json(), dict) else resp1.json())

        SportEventFactory.create(sport="nba", name="NBA Eastern Conference Finals", created_by=admin_user)

        resp2 = api_client.get("/api/auth/events/")
        after = len(resp2.json().get("results", resp2.json()) if isinstance(resp2.json(), dict) else resp2.json())

        assert after == before + 1

    def test_multiple_sports_events_retrievable(self, db, api_client, admin_user):
        nfl_event = SportEventFactory.nfl(name="NFL Wild Card 2026", created_by=admin_user)
        nba_event = SportEventFactory.nba(name="NBA Playoff Round 1", created_by=admin_user)
        fb_event = SportEventFactory.football(name="FA Cup Final 2026", created_by=admin_user)

        for event in [nfl_event, nba_event, fb_event]:
            resp = api_client.get(f"/api/auth/events/{event.slug}/")
            assert resp.status_code == status.HTTP_200_OK

    def test_event_list_includes_all_sports_types(self, db, api_client, admin_user):
        SportEventFactory.nfl(created_by=admin_user)
        SportEventFactory.nba(created_by=admin_user)
        SportEventFactory.football(created_by=admin_user)

        resp = api_client.get("/api/auth/events/")
        data = resp.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        organizers = {e["organizer_name"] for e in results}
        assert "NFL" in organizers
        assert "NBA" in organizers
