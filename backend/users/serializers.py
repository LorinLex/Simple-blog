from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers
from posts.models import Post, Tag
from posts.serializers import PostListSerializer


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    is_staff = serializers.BooleanField(source='user.is_staff')
    date_joined = serializers.DataField(source='user.date_joined', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislikes.count', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'first_name',
            'last_name',
            'is_staff',
            'date_joined',
            'user_img',
            'likes',
            'dislikes'
        ]


class ProfileDetail(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    is_staff = serializers.BooleanField(source='user.is_staff')
    date_joined = serializers.DataField(source='user.date_joined')
    favourite_posts = PostListSerializer()
    user_posts = PostListSerializer()
    subscribe_users = UserSerializer()
    subscribe_tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Profile
        fields = [
            'id',
            'first_name',
            'last_name',
            'user_img',
            'is_staff',
            'date_joined',
            'likes',
            'dislikes',
            'status',
            'subscribe_tags',
            'favourite_posts',
        ]

    def create(self):
        pass

    def update(self):
        pass

    def save(self):
        pass

    def save(self):
        pass
