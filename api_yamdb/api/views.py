from rest_framework import viewsets
from rest_framework.views import APIView
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from reviews.models import  Category, Comment, Genre, Reviews, Title
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleChangeSerializer,
    TitleSerializer
)
from api.filters import TitleFilter
from rest_framework import filters, mixins, permissions, status, viewsets
# from .permissions import ("Братка, тут твои разрешения")


class CategoryViewSet(GetPostDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (,)
    filter_backends = (TitleFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (,)
    filter_backends = (TitleFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    filter_backends = (TitleFilter,)
    filterset_class = TitleFilter
    # permission_classes = (,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return TitleChangeSerializer


class UsersViewSet(viewsets.ModelViewSet):
    pass


class SignUp(APIView):
    pass


class Token(APIView):
    pass


class ReviewsViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (
        # Здесь мне нужно разрешение в зависимости от роли
        permissions.IsAuthenticatedOrReadOnly,

    )

    def get_title(self):
        """Возвращает объект текущего произведения."""
        title_id = self.kwargs.get('title_id')
        return get_object_or_404("Модель произведения", pk=title_id)

    def get_queryset(self):
        """Возвращает queryset c отзывами для текущего произведения."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создает отзыв для текущего произведения,
        где автором является текущий пользователь."""
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (
        # Здесь мне нужно разрешение в зависимости от роли
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )