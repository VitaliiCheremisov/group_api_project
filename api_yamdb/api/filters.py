import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """Фильтрует список всех произведений."""
    category = django_filters.CharFilter(field_name='category__slug',
                                         lookup_expr='iexact')
    genre = django_filters.CharFilter(field_name='genre__slug',
                                      lookup_expr='iexact')
    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
