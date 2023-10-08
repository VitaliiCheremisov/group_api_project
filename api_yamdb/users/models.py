from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb import constants


class CustomUser(AbstractUser):
    CHOICES = [
        (constants.ADMIN, 'Администратор'),
        (constants.MODERATOR, 'Модератор'),
        (constants.USER, 'Пользователь')
    ]
    username = models.CharField(
        'Имя пользователя',
        max_length=constants.MAX_NAME_LENGTH,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Недопустимый символ'
        )]
    )
    email = models.EmailField(
        max_length=constants.MAX_EMAIL_LENGTH,
        unique=True
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

    @property
    def is_admin(self):
        return self.role == constants.ADMIN

    @property
    def is_moderator(self):
        return self.role == constants.MODERATOR
