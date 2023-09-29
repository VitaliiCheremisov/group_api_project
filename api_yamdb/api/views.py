from django.conf import settings
from django.db import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets, status, permissions, mixins, filters, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from reviews.models import CustomUser

from .serializers import TokenSerializer, SignUpSerializer, CustomUserSerializer

from .permissions import IsSuperUserOrIsAdmin


class APISignUp(APIView):
    """Создание нового пользователя"""
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
            user, _ = CustomUser.objects.get_or_create(username=username, email=email)
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
    """Полчения токена"""
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
    """Работа с пользователем"""
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
        user = get_object_or_404(CustomUser, username=username)
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(user, data=request.data, partial=True)
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
