from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()

class AuthenticationApiTestCase(APITestCase):

    def setUp(self):
        self.credentials = {"username": "quizzer", "password": "StrongPass123!"}
        self.user = User.objects.create_user(
            email="quizzer@example.com", **self.credentials
        )
