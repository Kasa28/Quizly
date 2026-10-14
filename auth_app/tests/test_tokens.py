"""Tests for refreshing and revoking JWT cookies."""

from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from .base import AuthenticationApiTestCase


class TokenTests(AuthenticationApiTestCase):
    """Verify refresh and logout behavior."""

    def test_refresh_uses_refresh_cookie(self):
        """The refresh cookie produces a replacement access cookie."""
        self.client.post("/api/login/", self.credentials, format="json")
        response = self.client.post("/api/token/refresh/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.cookies)

    def test_logout_blacklists_refresh_and_deletes_cookies(self):
        """Logout invalidates the refresh token and expires both cookies."""
        self.client.post("/api/login/", self.credentials, format="json")
        response = self.client.post("/api/logout/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BlacklistedToken.objects.count(), 1)
        self.assertEqual(response.cookies["access_token"]["max-age"], 0)
        self.assertEqual(response.cookies["refresh_token"]["max-age"], 0)
