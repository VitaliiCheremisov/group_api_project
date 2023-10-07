from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(data):
    """Проверка года выпуска."""
    if data > timezone.now().year:
        raise ValidationError(
            'Нельзя добавлять произведения, которые еще не вышли.'
        )
