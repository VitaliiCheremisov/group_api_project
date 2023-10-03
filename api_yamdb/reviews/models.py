from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator)

from .validators import validate_year


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=settings.MAX_NAME_LENGTH,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=settings.MAX_EMAIL_LENGTH,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        'имя',
        max_length=settings.MAX_NAME_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=settings.MAX_NAME_LENGTH,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True
    )
    role = models.CharField(
        'роль',
        max_length=settings.MAX_ROLE_LENGTH,
        choices=settings.CHOICES,
        default=settings.USER,
        blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=settings.MAX_NAME_LENGTH,
        null=True,
        blank=False,
        default='0000'
    )

    @property
    def is_admin(self):
        return self.role == settings.ADMIN

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR

    @property
    def is_user(self):
        return self.role == settings.USER

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=settings.MAX_LENGTH
    )
    slug = models.SlugField(
        'Slug категории',
        unique=True,
        max_length=settings.SLUG_MAX_LENGTH
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:settings.SHORT_TEXT_LENGTH]


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=settings.MAX_LENGTH
    )
    slug = models.SlugField(
        'Slug жанра',
        unique=True,
        max_length=settings.SLUG_MAX_LENGTH
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:settings.SHORT_TEXT_LENGTH]


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=settings.MAX_LENGTH
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=(validate_year,),
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-year', 'name')
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:settings.SHORT_TEXT_LENGTH]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title} - это {self.genre} жанр.'


class Review(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    score = models.PositiveIntegerField(
        verbose_name='Oценка',
        validators=[
            MinValueValidator(
                settings.MIN_VALUE_VALIDATOR,
                message='Используйте число от 1 до 10!'
            ),
            MaxValueValidator(
                settings.MAX_VALUE_VALIDATOR,
                message='Используйте число от 1 до 10!'
            ), ])
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        null=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text[:settings.SHORT_TEXT_LENGTH]


class Comment(models.Model):
    """Тут мы отрабатываем комментарии к отзывам."""
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Aвтор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания'
    )
    reviews = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзыву'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:settings.SHORT_TEXT_LENGTH]
