# from django.contrib.auth.models import User
from .models import User
from rest_framework import serializers
from posts.models import Post, Tag
from posts.serializers import PostListSerializer


class UserListSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislikes.count', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'date_joined',
            'user_img',
            'likes_count',
            'dislikes_count',
        ]
        read_only_fields = [
            'id',
            'is_staff',
            'date_joined',
            'likes_count',
            'dislikes_count',
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    subscribe_tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all(),
        validators=None,
        required=False,
    )
    favourite_posts = PostListSerializer(many=True, required=False)
    user_posts = PostListSerializer(many=True, required=False)
    subscribe_users = UserListSerializer(many=True, required=False)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislikes.count', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'user_img',
            'is_staff',
            'date_joined',
            'likes_count',
            'dislikes_count',
            'status',
            'subscribe_tags',
            'favourite_posts',
            'user_posts',
            'subscribe_users',
        ]
        read_only_true = [
            'id',
            'is_staff',
            'date_joined',
            'likes_count',
            'dislikes_count',
            'subscribe_tags',
            'favourite_posts',
            'user_posts',
            'subscribe_users',
        ]

