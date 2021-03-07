from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Tag

class PostSerializer(serializers.ModelSerializer):
    # TODO:  N+1 problem?
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislikes.count', read_only=True)
    is_liked = serializers.SerializerMethodField('is_liked_method')
    is_disliked = serializers.SerializerMethodField('is_disliked_method')

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
            'is_liked',
            'is_disliked'
        ]
        read_only_fields = [
            'author_id',
            'creation_data',
            'likes_count',
            'dislikes_count',
            'is_liked',
            'is_disliked'
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

    def is_liked_method(self, obj):
        try:
            obj.likes.get(pk=self.context['user'].id)
        except User.DoesNotExist:
            return False
        return True

    def is_disliked_method(self, obj):
        try:
            obj.dislikes.get(pk=self.context['user'].id)
        except User.DoesNotExist:
            return False
        return True