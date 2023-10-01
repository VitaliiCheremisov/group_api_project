from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(data):
    """Проверка года выпуска."""
    if timezone.now().year < data:
        raise ValidationError(
            'Нельзя добавлять произведения, которые еще не вышли.'
        )
    return data
