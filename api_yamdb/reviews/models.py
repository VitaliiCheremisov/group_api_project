from django.contrib.auth.models import AbstractUser
from django.db import models

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
