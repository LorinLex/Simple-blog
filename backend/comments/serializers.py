from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    # TODO:  N+1 problem?
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislikes.count', read_only=True)
    is_liked = serializers.SerializerMethodField('is_liked_method')
    is_disliked = serializers.SerializerMethodField('is_disliked_method')

    class Meta:
        model = Comment
        fields = [
            "text",
            "post_id",
            "author_id",
            "creation_data",
            "likes_count",
            "dislikes_count",
            "is_liked",
            "is_disliked"
        ]
        read_only_fields =
            'post_id',
            'creation_data',
            'likes_count',
            'dislikes_count',
            'is_liked',
            'is_disliked'
        ]


    # Todo: Duplicated in PostSerializer, should make file with that
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
