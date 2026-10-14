"""Shared setup for authentication API tests."""
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()

class AuthenticationApiTestCase(APITestCase):
    """Provide a user and credentials for authentication tests."""
    def setUp(self):
        """Create credentials shared by authentication tests."""
        self.credentials = {"username": "quizer", "password": "QuizerPass123!"}
        self.user = User.objects.create_user(
            email="quizer@gmail.com", **self.credentials
        )
