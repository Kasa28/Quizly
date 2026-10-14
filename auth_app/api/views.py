"""Authentication API views."""

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from auth_app.cookies import clear_auth_cookies, set_auth_cookies

from .serializers import LoginSerializer, RegistrationSerializer


class RegistrationView(generics.CreateAPIView):
    """Create a new user account."""

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer


class LoginCookieView(TokenObtainPairView):
    """Authenticate a user and store both JWTs in HttpOnly cookies."""

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """Return a generic result and attach generated JWT cookies."""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = {"detail": "Username or password is incorrect."}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        response = Response({"detail": "Login successful."})
        set_auth_cookies(response, serializer.validated_data)
        return response


class LogoutView(APIView):
    """Blacklist the refresh token and remove both JWT cookies."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Invalidate the session represented by the refresh cookie."""
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "Refresh token not found."}, status=400)
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            return Response({"detail": "Refresh token is invalid."}, status=401)
        response = Response({"detail": "Logout successful."})
        clear_auth_cookies(response)
        return response


class RefreshTokenView(TokenRefreshView):
    """Create a new access token from the HttpOnly refresh cookie."""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Refresh access without exposing the refresh token."""
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "Refresh token not found."}, status=401)
        serializer = self.get_serializer(data={"refresh": refresh_token})
        serializer.is_valid(raise_exception=True)
        response = Response({"detail": "Token refreshed."})
        set_auth_cookies(response, serializer.validated_data)
        return response
