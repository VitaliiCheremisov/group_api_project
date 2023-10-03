from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, CustomUser, Genre, Review, Title

from .validators import validate_username


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для категории."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для жанров."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для заголовка c полями только для чтения."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category', 'rating'
        )


class TitleChangeSerializer(serializers.ModelSerializer):
    """Сериалайзер для изменения заголовка."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre',
            'category'
        )


class TokenSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения токена."""
    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания пользователя."""
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
    """Сериалайзер для собственной модели юзера."""
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
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для отзывов."""
    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score',
            'pub_date'
        )

    def validate(self, data):
        """Защита от повторных отзывов от одного автора."""
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Нельзя оставлять отзыв два раза на один фильм'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для комментов."""
    author = serializers.StringRelatedField(
        read_only=True
    )
    reviews = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'text', 'author', 'pub_date', 'reviews'
        )
