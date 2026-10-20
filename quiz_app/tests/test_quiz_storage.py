"""Tests for validating and atomically storing generated quizzes."""

from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from quiz_app.models import QuestionforQuizly, QuizforQuizly
from quiz_app.services.quiz_storage import save_generated_quiz

User = get_user_model()

class QuizStorageTests(APITestCase):
    """Verify generated quiz validation and database transactions."""

    def setUp(self):
        """Create a user and reusable video URL."""
        self.user = User.objects.create_user(username="quizzer")
        self.video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    def create_question(self, number):
        """Build one valid generated question."""
        return {
            "question_title": f"Question {number}",
            "question_options": ["A", "B", "C", "D"],
            "answer": "A"
        }

    def create_quiz(self):
        """Build valid generated data containing ten questions."""
        return {
            "title": "Generated Quiz",
            "description": "Test description",
            "questions": [self.create_question(i) for i in range(10)]
        }

    def test_quiz_and_questions_are_saved(self):
        """Valid generated data creates one quiz and ten questions."""
        quiz = save_generated_quiz(
            self.create_quiz(), self.user, self.video_url
        )
        self.assertEqual(QuizforQuizly.objects.count(), 1)
        self.assertEqual(QuestionforQuizly.objects.count(), 10)
        self.assertEqual(quiz.user, self.user)
        self.assertEqual(quiz.questions.count(), 10)

    def test_quiz_with_nine_questions_is_rejected(self):
        """Generated data with fewer than ten questions is rejected."""
        data = self.create_quiz()
        data["questions"].pop()
        with self.assertRaises(ValidationError):
            save_generated_quiz(data, self.user, self.video_url)
        self.assertEqual(QuizforQuizly.objects.count(), 0)

    def test_quiz_with_wrong_answer_is_rejected(self):
        """An answer outside the available options is rejected."""
        data = self.create_quiz()
        data["questions"][0]["answer"] = "Wrong"
        with self.assertRaises(ValidationError):
            save_generated_quiz(data, self.user, self.video_url)
        self.assertEqual(QuizforQuizly.objects.count(), 0)

    def test_quiz_is_not_saved_when_questions_fail(self):
        """A question insert failure rolls back the complete quiz."""
        target = "quiz_app.services.quiz_storage.QuestionforQuizly.objects.bulk_create"
        with patch(target, side_effect=RuntimeError("Database error")):
            with self.assertRaises(RuntimeError):
                save_generated_quiz(self.create_quiz(), self.user, self.video_url)
        self.assertEqual(QuizforQuizly.objects.count(), 0)
