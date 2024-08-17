from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group',)


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'post', 'text', 'author', 'created',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ('user', 'following',)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Вы уже подписаны на этого пользователя.'
            )
        ]

    def validate(self, data):
        """
        Переопределяем метод валидации данных,
        чтобы сериализатор не пропускал записи
        с одинаковыми полями.
        """
        user = self.context['request'].user
        if user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data
