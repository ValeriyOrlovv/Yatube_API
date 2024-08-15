from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group',)
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'text', 'author', 'created',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.CharField()

    class Meta:
        fields = ('user', 'following',)
        model = Follow
        read_only_fields = ['user']

    def create(self, validated_data):
        """Переопределяем метод для обработки POST запроса."""
        following_username = validated_data.pop('following')
        following_user = get_object_or_404(User, username=following_username)
        follow = Follow.objects.create(
            user=self.context['request'].user,
            following=following_user
        )
        return follow

    def validate(self, data):
        """
        Переопределяем метод валидации данных,
        чтобы сериализатор обрабатывал строчные значения полей.
        """
        user = self.context['request'].user
        following_user = get_object_or_404(
            User,
            username=data.get('following')
        )

        if user == following_user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )

        if Follow.objects.filter(user=user, following=following_user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на данного пользователя'
            )
        data['following'] = following_user
        return data
