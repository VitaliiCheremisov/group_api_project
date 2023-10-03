import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError('Неверное имя пользователя')
    pattern = r'^[\w.@+-]+\Z'
    if re.match(pattern, value) is None:
        raise ValidationError('Неверное содержание поля')
