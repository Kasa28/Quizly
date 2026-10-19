from rest_framework.exceptions import ValidationError
from rest_framework.test import APISimpleTestCase
from quiz_app.services.youtube import get_video_id, validate_youtube_url

class YouTubeUrlTests(APISimpleTestCase):

    def test_normal_youtube_link(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.assertEqual(validate_youtube_url(url), url)

    def test_short_youtube_link(self):
        url = "https://youtu.be/dQw4w9WgXcQ"
        self.assertEqual(validate_youtube_url(url), url)

    def test_get_video_id_from_shorts(self):
        url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
        self.assertEqual(get_video_id(url), "dQw4w9WgXcQ")

    def test_invalid_website(self):
        url = "https://example.com/watch?v=dQw4w9WgXcQ"
        with self.assertRaises(ValidationError):
            validate_youtube_url(url)

    def test_missing_link(self):
        with self.assertRaises(ValidationError):
            validate_youtube_url(None)

    def test_invalid_video_id(self):
        url = "https://www.youtube.com/watch?v=short"
        with self.assertRaises(ValidationError):
            validate_youtube_url(url)