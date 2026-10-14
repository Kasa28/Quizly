"""URL routes for the authentication API."""

from django.urls import path

from .views import LoginCookieView, LogoutView, RefreshTokenView, RegistrationView


urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginCookieView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", RefreshTokenView.as_view(), name="token-refresh"),
]
