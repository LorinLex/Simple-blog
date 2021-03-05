from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Tag, PostLike, PostDislike

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField(method_name='get_post_likes')
    dislikes_count = serializers.SerializerMethodField(method_name='get_post_dislikes')

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'text',
            'author_id',
            'is_published',
            'creation_data',
            'last_modified',
            'tags_id',
            'likes_count',
            'dislikes_count',
        ]
        read_only_fields = [
            'author_id',
            'creation_data',
            'likes_count',
            'dislikes_count',
        ]

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        # instance.tags_id
        instance.save()
        return instance

    def get_post_likes(self, obj):
        return PostLike.objects.filter(post_id=obj.id).count()

    def get_post_dislikes(self, obj):
        return PostDislike.objects.filter(post_id=obj.id).count()
