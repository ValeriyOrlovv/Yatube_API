from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from posts.models import  Group, Post
from api.permissions import IsOwnerOrReadOnly, CustomIsAuthenticated
from api.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer
)


class ListCreateMixIn(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Кастомный миксин для веюсетов,
    обрабатывающих только GET и POST запросы.
    """


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с постами."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly
    )

    def perform_create(self, serializer):
        """Метод для сохранения изменений поста с заданным значением автора."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с группами"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly,)

    def get_posts_for_comments(self):
        """Получаем пост, к которому относятся комментарии или 404."""
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        """
        Получаем объект поста и возвращаем все,
        связанные с ним,
        комментарии.
        """
        post = self.get_posts_for_comments()
        return post.comments.all()

    def perform_create(self, serializer):
        """
        При создании комментария так же получаем пост, для которого хотим
        создать комментарий. Далее сохраняем, передав значение id
        из полученного объекта
        и значение author из объекта авторизованного пользователя.
        """
        post = self.get_posts_for_comments()
        serializer.save(post=post, author=self.request.user)


class FollowViewSet(ListCreateMixIn):
    """Вьюсет для работы с подписками."""
    serializer_class = FollowSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Получаем подписки пользователя, который сделал запрос."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """
        При POST запросе автоматически задаём поле автора,
        передав значение имени авторизованного пользователя.
        """
        serializer.save(user=self.request.user)
