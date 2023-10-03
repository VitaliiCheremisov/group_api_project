from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, mixins, permissions, serializers, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, CustomUser, Genre, Review, Title

from .filters import TitleFilter
from .permissions import (IsAdminIsModeratorIsAuthor, IsAdminIsUserOrReadOnly,
                          IsSuperUserOrIsAdmin)
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUserSerializer, GenreSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleChangeSerializer, TitleSerializer,
                          TokenSerializer)
from .utils import CreateDestroyListViewSet


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


class TitleViewSet(viewsets.ModelViewSet):
    """Работа с заголовками."""
    serializer_class = TitleSerializer
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminIsUserOrReadOnly,)
    http_method_names = settings.ALLOWED_METHODS

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
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as error:
            raise error
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user, _ = CustomUser.objects.get_or_create(
                username=username, email=email
            )
        except IntegrityError:
            raise serializers.ValidationError('Пользователь уже существует')
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Регистрация',
            message=f'Ваш код {confirmation_code}',
            from_email=settings.EMAIL_PROJECT,
            recipient_list=(email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIToken(APIView):
    """Получение токена."""
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(CustomUser, username=data['username'])
        if data['confirmation_code'] == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(str(token), status=status.HTTP_201_CREATED)
        return Response('Неверный код!', status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """Работа с пользователем."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsSuperUserOrIsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+)',
        url_name='get_user'
    )
    def get_user(self, request, username):
        user = get_object_or_404(
            CustomUser, username=username
        )
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me(self, request):
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Reviews."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminIsModeratorIsAuthor,)
    http_method_names = settings.ALLOWED_METHODS

    def get_title(self):
        """Возвращает объект текущего произведения."""
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

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
    permission_classes = (IsAdminIsModeratorIsAuthor,)
    http_method_names = settings.ALLOWED_METHODS

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
