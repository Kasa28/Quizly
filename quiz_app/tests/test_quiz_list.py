from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from quiz_app.models import QuizforQuizly

User = get_user_model()


class QuizListTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="quizzer")
        self.other_user = User.objects.create_user(username="other")
        self.quiz = self.create_quiz(self.user, "My Quiz")
        self.create_quiz(self.other_user, "Other Quiz")
        self.url = reverse("quiz-list")

    def create_quiz(self, user, title):
        return QuizforQuizly.objects.create(
            title=title,
            description="Test",
            user=user,
        )

    def test_authentication_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_own_can_see_quizzes(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.quiz.id)
