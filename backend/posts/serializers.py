from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import serializers
from .models import Post, Tag
from django.core.exceptions import ObjectDoesNotExist


def is_liked_disliked_method(field_name, self, obj):
    try:
        getattr(obj, field_name).get(pk=self.context['user'].id)
    except settings.AUTH_BASE_MODEL.DoesNotExist:
        return False
    return True


class PostDetailSerializer(serializers.ModelSerializer):
    # TODO:  N+1 problem?
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislikes.count', read_only=True)
    is_liked = serializers.SerializerMethodField('is_liked_method')
    is_disliked = serializers.SerializerMethodField('is_disliked_method')
    tags_id = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )

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
        # TODO: popping tags is not healthy, need to work with slug (how?)
        tags_data = validated_data.pop('tags_id')
        post =  Post.objects.create(**validated_data, author_id=self.context['user'])
        tags = [Tag.objects.get_or_create(name=name)[0] for name in tags_data]
        post.tags_id.add(*tags)
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.is_published = validated_data.get(
            'is_published', instance.is_published)

        tags_data = validated_data.pop('tags_id')
        tags = [Tag.objects.get_or_create(name=name)[0] for name in tags_data]
        instance.tags_id.set(*tags)
        instance.save()
        return instance

    def is_liked_method(self, obj):
        return is_liked_disliked_method('likes', self, obj)

    def is_disliked_method(self, obj):
        return is_liked_disliked_method('dislikes', self, obj)

class PostListSerializer(serializers.ModelSerializer):
    # TODO:  N+1 problem?
    text = serializers.CharField(max_length=200)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislikes.count', read_only=True)
    is_liked = serializers.SerializerMethodField('is_liked_method')
    is_disliked = serializers.SerializerMethodField('is_disliked_method')
    tags_id = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'text',
            'author_id',
            'is_published',
            'creation_data',
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

    def is_liked_method(self, obj):
        return is_liked_disliked_method('likes', self, obj)

    def is_disliked_method(self, obj):
        return is_liked_disliked_method('dislikes', self, obj)

