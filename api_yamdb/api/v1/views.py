from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import CustomUser

from .filters import TitleFilter
from .permissions import (IsAdminIsModeratorIsAuthor, IsAdminIsUserOrReadOnly,
                          IsSuperUserOrIsAdmin)
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUserSerializer, GenreSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleChangeSerializer, TitleSerializer,
                          TokenSerializer)
from .utils import (CreateDestroyListViewSet, CreateListRetrieveDestroyViewSet,
                    send_code)


class CategoryViewSet(CreateDestroyListViewSet):
    """Работа с категориями."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminIsUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyListViewSet):
    """Работа с жанрами."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminIsUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(CreateListRetrieveDestroyViewSet):
    """Работа с заголовками."""
    serializer_class = TitleSerializer
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminIsUserOrReadOnly,)

    def get_serializer_class(self):
        """Выбор нужного сериалайзера."""
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return TitleChangeSerializer


class APISignUp(APIView):
    """Создание нового пользователя."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        # Если начинаю проверять в сериалайзере, падают тесты, не пойму почему...
        try:
            user, _ = CustomUser.objects.get_or_create(
                username=username, email=email
            )
        except IntegrityError:
            raise serializers.ValidationError('Пользователь уже существует')
        confirmation_code = default_token_generator.make_token(user)
        send_code(email=email, confirmation_code=confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIToken(APIView):
    """Получение токена."""
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(CustomUser, username=data['username'])
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Неверный код подтверждения'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class UsersViewSet(CreateListRetrieveDestroyViewSet):
    """Работа с пользователем."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsSuperUserOrIsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me(self, request):
        """Обработка GET-запроса."""
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @get_me.mapping.patch
    def path_me(self, request):
        """Обработка PATCH-запроса."""
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(CreateListRetrieveDestroyViewSet):
    """Вьюсет для обьектов модели Reviews."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminIsModeratorIsAuthor,)

    def get_title(self):
        """Возвращает объект текущего произведения."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

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


class CommentViewSet(CreateListRetrieveDestroyViewSet):
    """Вьюсет для обьектов модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAdminIsModeratorIsAuthor,)

    def get_reviews(self):
        reviews_id = self.kwargs.get('reviews_id')
        return get_object_or_404(Review, pk=reviews_id)

    def get_queryset(self):
        return self.get_reviews().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            reviews=self.get_reviews()
        )
