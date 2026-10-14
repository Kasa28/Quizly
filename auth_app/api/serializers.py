from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "confirmed_password")

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email is already in use.")

        return email

    def validate(self, data):
        if data["password"] != data["confirmed_password"]:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })

        return data

    def create(self, validated_data):
        validated_data.pop("confirmed_password")
        return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except AuthenticationFailed as error:
            message = "Username or password is incorrect."
            raise serializers.ValidationError({
                "detail": message
            }) from error
