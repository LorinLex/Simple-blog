from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers
from posts.models import Post


class User(serializers.ModelSerializer):
    # user_img = serializers.ImageField(source='Profile.user_img')
    likes = serializers.IntegerField(source='Profile.likes.count')
    dislikes = serializers.IntegerField(source='Profile.dislikes.count')
    class Meta:
        fields = [
            'id',
            'first_name',
            'last_name',
            # 'user_img',
            'is_stuff',
            'date_joined',
            'likes',
            'dislikes',
        ]


# class UserDetail(serializers.Serializer):
#     id = serializers.IntegerField()
#     username = serializers.CharField()
#     first_name = serializers.CharField(allow_blank=True)
#     last_name = serializers.CharField(allow_blank=True)
#     is_stuff = serializers.BooleanField(default=True)
#     email = serializers.EmailField(allow_blank=True)
#     status = serializers.CharField(max_length=100)
#     subscribe_tags = serializers.SlugRelatedField(
#         many=True,
#         read_only=True,
#         slug_field='name'
#      )
#     favourite_posts = serializers.Field(allow_blank=True)
#     user_posts = serializers.Field(allow_blank=True)
#
#
#     def create(self):
#         pass
#
#     def update(self):
#         pass
#
#     def save(self):
#         pass
#
#     def save(self):
#         pass
