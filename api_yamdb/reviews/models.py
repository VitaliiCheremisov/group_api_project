from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator)

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

CHOICES = [
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор'),
    (USER, 'Пользователь')
]


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=128,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=250,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=CHOICES,
        default=USER,
        blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=250,
        null=True,
        blank=False,
        default='0000'
    )

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Reviews(models.Model):

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор отзыва'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )

    mark = models.PositiveIntegerField(        
        verbose_name='Oценка',
        validators=[
            MinValueValidator(
                1,
                message='Используйте число от 1 до 10!'
            ),
            MaxValueValidator(
                10,
                message='Используйте число от 1 до 10!'
            ),
        ]
    )

    public_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        db_index=True
    )

    title = models.ForeignKey(
        'Тут будет название модели произведений',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        null=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-public_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'titles'],
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text[:20]


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
    public_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания'
    )
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзыву'
        ordering = ('-public_date',)

    def __str__(self):
        return self.text[:20]
