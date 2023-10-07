from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.validators import ValidationError

from api_yamdb import constants


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
        default=constants.USER
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @classmethod
    def clean(cls):
        super().clean()
        if cls.username == 'me':
            raise ValidationError(
                'Создавать пользователя me нельзя'
            )

    @property
    def is_admin(self):
        return self.role == constants.ADMIN

    @property
    def is_moderator(self):
        return self.role == constants.MODERATOR
