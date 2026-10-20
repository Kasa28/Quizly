"""Tests for the authenticated quiz generation endpoint."""
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from quiz_app.models import QuizforQuizly

User = get_user_model()

class QuizGenerationTests(APITestCase):
    """Verify generation input, authentication, and quiz ownership."""

    def setUp(self):
        """Create a user and reusable generation request data."""
        self.user = User.objects.create_user(username="quizzer")
        self.url = reverse("quiz-list")
        self.video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    def create_question(self, number):
        """Build one valid generated question."""
        return {
            "question_title": f"Question {number}",
            "question_options": ["A", "B", "C", "D"],
            "answer": "A",
        }

    def create_quiz_data(self):
        """Build valid generated data containing ten questions."""
        return {
            "title": "Generated Quiz",
            "description": "Test description",
            "questions": [self.create_question(i) for i in range(10)],
        }

    def assert_saved_quiz(self, response):
        """Assert that the response and stored quiz contain expected data."""
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Generated Quiz")
        self.assertEqual(len(response.data["questions"]), 10)
        quiz = QuizforQuizly.objects.get()
        self.assertEqual(quiz.user, self.user)
        self.assertEqual(quiz.video_url, self.video_url)

    def test_authentication_is_required(self):
        """Anonymous users cannot generate quizzes."""
        response = self.client.post(
            self.url,
            {"url": self.video_url},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_url_is_required(self):
        """Generation rejects a request without a URL."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("quiz_app.api.views.generate_quiz_from_youtube")
    def test_generated_quiz_is_saved_for_user(self, generate_quiz):
        """Generated data is stored for the authenticated user."""
        generate_quiz.return_value = self.create_quiz_data()
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.url,
            {"url": self.video_url},
            format="json",
        )
        self.assert_saved_quiz(response)
        generate_quiz.assert_called_once_with(self.video_url)
