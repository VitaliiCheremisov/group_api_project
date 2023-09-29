from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import APISignUp, APIToken, UsersViewSet, CommentViewSet, ReviewsViewSet

router_v1 = SimpleRouter()
router_v1.register('users', UsersViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_patterns = [
    path('signup/', APISignUp.as_view(), name='signup'),
    path('token/', APIToken.as_view(), name='token')
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls))
]
