from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    # TODO:  N+1 problem?
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(
        source='dislikes.count', read_only=True)
    is_liked = serializers.SerializerMethodField('is_liked_method')
    is_disliked = serializers.SerializerMethodField('is_disliked_method')

    class Meta:
        model = Comment
        fields = [
            "id",
            "text",
            "post_id",
            "author_id",
            "creation_data",
            "likes_count",
            "dislikes_count",
            "is_liked",
            "is_disliked"
        ]
        read_only_fields = [
            'post_id',
            "author_id",
            'creation_data',
            'likes_count',
            'dislikes_count',
            'is_liked',
            'is_disliked'
        ]

    def create(self, validated_data):
        return Comment.objects.create(**validated_data,
                post_id=self.context['post'], author_id=self.context['user'])

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance

    def is_liked_method(self, obj):
        try:
            obj.likes.get(pk=self.context['user'].id)
        except settings.AUTH_BASE_MODEL.DoesNotExist:
            return False
        return True

    def is_disliked_method(self, obj):
        try:
            obj.dislikes.get(pk=self.context['user'].id)
        except settings.AUTH_BASE_MODEL.DoesNotExist:
            return False
        return True
