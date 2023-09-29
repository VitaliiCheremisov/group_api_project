from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import CustomUser

from .validators import validate_username


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_username, ],
    )
    email = serializers.CharField(
        max_length=150,
        validators=[validate_email, ],
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            validate_username,
            UniqueValidator(queryset=CustomUser.objects.all()),
        ]
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
