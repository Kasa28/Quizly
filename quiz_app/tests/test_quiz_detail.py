"""Tests for retrieving, editing, and deleting individual quizzes."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from quiz_app.models import QuizforQuizly, QuestionforQuizly

User = get_user_model()

class QuizDetailTests(APITestCase):
    """Verify quiz detail operations and ownership protection."""

    def setUp(self):
        """Create authenticated test data for two different users."""
        self.user = User.objects.create_user(username="quizzer")
        self.other_user = User.objects.create_user(username="other")
        self.my_quiz = self.create_quiz(self.user, "My Quiz")
        self.other_quiz = self.create_quiz(self.other_user, "Other Quiz")
        self.create_question()
        self.client.force_authenticate(user=self.user)

    def create_quiz(self, user, title):
        """Create a quiz owned by the supplied user."""
        return QuizforQuizly.objects.create(
            title=title,
            description="Test description",
            user=user
        )

    def create_question(self):
        """Create one question for the authenticated user's quiz."""
        QuestionforQuizly.objects.create(
            quizz=self.my_quiz,
            question_title="What is Python?",
            question_options=["Language", "Browser", "Database", "Game"],
            answer="Language"
        )

    def test_user_can_see_own_quiz(self):
        """A user can retrieve an owned quiz and its questions."""
        url = reverse("quiz-detail", args=[self.my_quiz.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.my_quiz.id)
        self.assertEqual(len(response.data["questions"]), 1)

    def test_user_cannot_see_other_quiz(self):
        """A quiz owned by another user is hidden."""
        url = reverse("quiz-detail", args=[self.other_quiz.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_user_can_update_own_quiz(self):
        """A user can update the title and description of an owned quiz."""
        url = reverse("quiz-detail", args=[self.my_quiz.id])
        data = {"title": "New Title", "description": "New Description"}
        response = self.client.patch(url, data, format="json")
        self.my_quiz.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.my_quiz.title, "New Title")
        self.assertEqual(self.my_quiz.description, "New Description")

    def test_user_cannot_update_other_quiz(self):
        """A user cannot update a quiz owned by another user."""
        url = reverse("quiz-detail", args=[self.other_quiz.id])
        data = {"title": "Changed Title"}
        response = self.client.patch(url, data, format="json")
        self.other_quiz.refresh_from_db()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.other_quiz.title, "Other Quiz")

    def test_user_can_delete_own_quiz(self):
        """Deleting an owned quiz also deletes its questions."""
        url = reverse("quiz-detail", args=[self.my_quiz.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(QuizforQuizly.objects.filter(id=self.my_quiz.id).exists())
        self.assertFalse(QuestionforQuizly.objects.filter(quizz=self.my_quiz).exists())

    def test_user_cannot_delete_other_quiz(self):
        """A user cannot delete a quiz owned by another user."""
        url = reverse("quiz-detail", args=[self.other_quiz.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(QuizforQuizly.objects.filter(id=self.other_quiz.id).exists())
