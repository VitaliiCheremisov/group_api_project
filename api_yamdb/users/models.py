from django.contrib.auth.models import AbstractUser
from django.db import models
from reviews import constants


class CustomUser(AbstractUser):
    CHOICES = [
        (constants.ADMIN, 'Администратор'),
        (constants.MODERATOR, 'Модератор'),
        (constants.USER, 'Пользователь')
    ]
    email = models.EmailField(
        max_length=constants.MAX_EMAIL_LENGTH,
        unique=True,
        blank=False,
        null=False
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=constants.MAX_ROLE_LENGTH,
        choices=CHOICES,
        default=constants.USER,
        blank=False
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == constants.ADMIN

    @property
    def is_moderator(self):
        return self.role == constants.MODERATOR