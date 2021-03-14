from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

    def create(self, validated_data):
        obj, created = Tag.objects.get_or_create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    # TODO:  N+1 problem?
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislikes.count', read_only=True)
    is_liked = serializers.SerializerMethodField('is_liked_method')
    is_disliked = serializers.SerializerMethodField('is_disliked_method')
    tags_id = TagSerializer(many=True)

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
        tags_data = validated_data.pop('tags_id')
        post =  Post.objects.create(**validated_data)
        for tag in tags_data:
            obj, created = Tag.objects.get_or_create(name=tag['name'])
            obj.post_set.add(post)
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.is_published = validated_data.get('is_published', instance.is_published)

        tags_data = validated_data.pop('tags_id')
        tags_obj = []
        for tag in tags_data:
            obj, created = Tag.objects.get_or_create(name=tag['name'])
            tags_obj.append(obj)
        instance.tags_id.set(tags_obj)
        instance.save()
        return instance

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

