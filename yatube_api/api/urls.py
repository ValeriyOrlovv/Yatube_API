from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from api.views import PostViewSet, GroupViewSet, FollowViewSet, CommentViewSet


v1_router = SimpleRouter()
v1_router.register('posts', PostViewSet)
v1_router.register('groups', GroupViewSet)
v1_router.register(
    r'^posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
v1_router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/jwt/refresh/', TokenRefreshView.as_view()),
    path('v1/jwt/create/', TokenObtainPairView.as_view()),
    path('v1/jwt/verify/', TokenVerifyView.as_view()),
]
