from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import APISignUp, APIToken, UsersViewSet

router_v1 = SimpleRouter()
router_v1.register('users', UsersViewSet, basename='users')

auth_patterns = [
    path('signup/', APISignUp.as_view(), name='signup'),
    path('token/', APIToken.as_view(), name='token')
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls))
]
