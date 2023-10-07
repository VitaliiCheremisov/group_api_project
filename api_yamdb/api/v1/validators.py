import re

from rest_framework.validators import ValidationError


def validate_username(value):
    """Проверка имени пользователя."""
    if value == 'me':
        raise ValidationError('Неверное имя пользователя')
    pattern = r'^[\w.@+-]+\Z'
    if re.match(pattern, value) is None:
        raise ValidationError('Неверное содержание поля')
    return value
