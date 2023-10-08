from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from api_yamdb import constants
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=constants.MAX_LENGTH
    )
    slug = models.SlugField(
        'Slug категории',
        unique=True,
        max_length=constants.SLUG_MAX_LENGTH
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:constants.SHORT_TEXT_LENGTH]


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=constants.MAX_LENGTH
    )
    slug = models.SlugField(
        'Slug жанра',
        unique=True,
        max_length=constants.SLUG_MAX_LENGTH
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:constants.SHORT_TEXT_LENGTH]


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=constants.MAX_LENGTH
    )
    year = models.PositiveIntegerField(
        'Год выпуска',
    )
    description = models.TextField(
        'Описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('-year', 'name')
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def validate(self, data):
        """Проверка года выпуска."""
        if data['year'] > timezone.now().year:
            raise ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли.'
            )

    def __str__(self):
        return self.name[:constants.SHORT_TEXT_LENGTH]


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
                constants.MIN_VALUE_VALIDATOR,
                message='Используйте число от 1 до 10!'
            ),
            MaxValueValidator(
                constants.MAX_VALUE_VALIDATOR,
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
        return self.text[:constants.SHORT_TEXT_LENGTH]


class Comment(models.Model):
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
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзыву'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:constants.SHORT_TEXT_LENGTH]
