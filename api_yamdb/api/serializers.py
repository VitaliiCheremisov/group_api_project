from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import CustomUser, Comment, Reviews

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
        
        
class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Reviews
        fields = (
            'id', 'text', 'author', 'mark',
            'public_date'
        )

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('Поле title')
        if Reviews.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'text', 'author', 'public_date')