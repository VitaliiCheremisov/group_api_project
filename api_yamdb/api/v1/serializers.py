from django.core.validators import validate_email
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from reviews.constants import MAX_NAME_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser

from .validators import validate_username

now = timezone.now()


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
        fields = ('username',)


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания пользователя."""
    username = serializers.CharField(
        max_length=MAX_NAME_LENGTH,
        required=True,
        validators=[validate_username]
    )
    email = serializers.CharField(
        # Без перепроверки ниже падает тест,
        # поэтому оставил
        max_length=MAX_NAME_LENGTH,
        validators=[validate_email]
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериалайзер для собственной модели юзера."""
    username = serializers.CharField(
        max_length=MAX_NAME_LENGTH,
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


class GetTitleId:
    """Получение title_id для ReviewSerializers."""
    requires_context = True

    def __call__(self, serializer_field):
        return (serializer_field.context['request']
                .parser_context['kwargs']['title_id'])


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для отзывов."""
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    title = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=GetTitleId()
    )

    class Meta:
        model = Review
        fields = (
            '__all__'
        )

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message='Вы уже оценили это произведение.'
            )
        ]


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
