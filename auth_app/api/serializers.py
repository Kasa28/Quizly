"""Serializers for user registration and JWT login."""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Validate registration data and create a Django user."""

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        """Configure fields exposed during registration."""
        model = User
        fields = ("username", "email", "password", "confirmed_password")

    def validate_email(self, email):
        """Reject email addresses that are already registered."""
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email is already in use.")

        return email

    def validate(self, data):
        """Ensure that both submitted passwords match."""
        if data["password"] != data["confirmed_password"]:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })

        return data

    def create(self, validated_data):
        """Create a user while hashing the submitted password."""
        validated_data.pop("confirmed_password")
        return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    """Create JWTs while returning a generic login error."""

    def validate(self, attrs):
        """Validate credentials without exposing the incorrect field."""
        try:
            return super().validate(attrs)
        except AuthenticationFailed as error:
            message = "Username or password is incorrect."
            raise serializers.ValidationError({
                "detail": message
            }) from error
