"""Tests for validation and parsing of supported YouTube URLs."""

from rest_framework.exceptions import ValidationError
from rest_framework.test import APISimpleTestCase
from quiz_app.services.youtube import get_video_id, validate_youtube_url

class YouTubeUrlTests(APISimpleTestCase):
    """Verify accepted YouTube formats and rejected invalid URLs."""

    def test_normal_youtube_link(self):
        """A standard YouTube watch URL is accepted."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.assertEqual(validate_youtube_url(url), url)

    def test_short_youtube_link(self):
        """A shortened youtu.be URL is accepted."""
        url = "https://youtu.be/dQw4w9WgXcQ"
        self.assertEqual(validate_youtube_url(url), url)

    def test_get_video_id_from_shorts(self):
        """The video ID is extracted from a YouTube Shorts URL."""
        url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
        self.assertEqual(get_video_id(url), "dQw4w9WgXcQ")

    def test_invalid_website(self):
        """A URL from a non-YouTube host is rejected."""
        url = "https://example.com/watch?v=dQw4w9WgXcQ"
        with self.assertRaises(ValidationError):
            validate_youtube_url(url)

    def test_missing_link(self):
        """A missing URL is rejected."""
        with self.assertRaises(ValidationError):
            validate_youtube_url(None)

    def test_invalid_video_id(self):
        """A YouTube URL containing an invalid video ID is rejected."""
        url = "https://www.youtube.com/watch?v=short"
        with self.assertRaises(ValidationError):
            validate_youtube_url(url)
