from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from quiz_app.models import QuestionforQuizly, QuizforQuizly
from quiz_app.services.quiz_storage import save_generated_quiz

User = get_user_model()

class QuizStorageTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="quizzer")
        self.video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    def create_question(self, number):
        return {
            "question_title": f"Question {number}",
            "question_options": ["A", "B", "C", "D"],
            "answer": "A"
        }

    def create_quiz(self):
        return {
            "title": "Generated Quiz",
            "description": "Test description",
            "questions": [self.create_question(i) for i in range(10)]
        }

    def test_quiz_and_questions_are_saved(self):
        quiz = save_generated_quiz(
            self.create_quiz(), self.user, self.video_url
        )
        self.assertEqual(QuizforQuizly.objects.count(), 1)
        self.assertEqual(QuestionforQuizly.objects.count(), 10)
        self.assertEqual(quiz.user, self.user)
        self.assertEqual(quiz.questions.count(), 10)

    def test_quiz_with_nine_questions_is_rejected(self):
        data = self.create_quiz()
        data["questions"].pop()
        with self.assertRaises(ValidationError):
            save_generated_quiz(data, self.user, self.video_url)
        self.assertEqual(QuizforQuizly.objects.count(), 0)

    def test_quiz_with_wrong_answer_is_rejected(self):
        data = self.create_quiz()
        data["questions"][0]["answer"] = "Wrong"
        with self.assertRaises(ValidationError):
            save_generated_quiz(data, self.user, self.video_url)
        self.assertEqual(QuizforQuizly.objects.count(), 0)

    def test_quiz_is_not_saved_when_questions_fail(self):
        target = "quiz_app.services.quiz_storage.QuestionforQuizly.objects.bulk_create"
        with patch(target, side_effect=RuntimeError("Database error")):
            with self.assertRaises(RuntimeError):
                save_generated_quiz(self.create_quiz(), self.user, self.video_url)
        self.assertEqual(QuizforQuizly.objects.count(), 0)