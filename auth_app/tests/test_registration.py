"""Tests for user registration."""

from rest_framework import status

from .base import AuthenticationApiTestCase, User


class RegistrationTests(AuthenticationApiTestCase):
    """Verify registration validation and user creation."""

    def test_registration_creates_user_with_hashed_password(self):
        """Registration creates a usable account without exposing passwords."""
        payload = {
            "username": "new_user", "email": "new@example.com",
            "password": "StrongPass456!", "confirmed_password": "StrongPass456!",
        }
        response = self.client.post("/api/register/", payload, format="json")
        user = User.objects.get(username="new_user")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)

    def test_registration_rejects_duplicate_email(self):
        """Email addresses cannot be registered twice, regardless of case."""
        payload = {
            "username": "other", "email": "QUIZZER@example.com",
            "password": "StrongPass456!", "confirmed_password": "StrongPass456!",
        }
        response = self.client.post("/api/register/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
