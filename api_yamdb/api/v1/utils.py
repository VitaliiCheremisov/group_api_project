from django.conf import settings
from django.core.mail import send_mail
from rest_framework import mixins, viewsets
from rest_framework.response import Response


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    """Создание своего вюьсета."""
    pass


class PatchModelMixin:
    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class CreateListRetrieveDestroyViewSet(mixins.CreateModelMixin,
                                       mixins.ListModelMixin,
                                       mixins.RetrieveModelMixin,
                                       mixins.DestroyModelMixin,
                                       PatchModelMixin,
                                       viewsets.GenericViewSet):
    """Собственный вьюсет без PUT-запроса."""
    pass


def send_code(email, confirmation_code):
    send_mail(
        subject='Регистрация',
        message=f'Ваш код {confirmation_code}',
        from_email=settings.EMAIL_PROJECT,
        recipient_list=(email,),
        fail_silently=False,
    )
