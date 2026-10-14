"""Tests for user login."""

from rest_framework import status

from .base import AuthenticationApiTestCase


class LoginTests(AuthenticationApiTestCase):
    """Verify successful and failed login attempts."""

    def test_login_sets_httponly_token_cookies(self):
        """A valid login stores both tokens without returning their values."""
        response = self.client.post("/api/login/", self.credentials, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.cookies["access_token"]["httponly"])
        self.assertTrue(response.cookies["refresh_token"]["httponly"])
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_login_uses_generic_error_message(self):
        """Invalid credentials do not reveal which value was incorrect."""
        payload = {"username": "quizzer", "password": "wrong"}
        response = self.client.post("/api/login/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Username or password is incorrect.")
