from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Comment
from posts.models import Post
from .serializers import CommentSerializer
from rest_framework.response import Response


# Create your views here.

def get_object(pk, model=CommentSerializer):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_context(self):
        context = super(CommentViewSet, self).get_serializer_context()
        print(self.request.user)
        context.update({'user': self.request.user})
        return context

    def list(self, request, post_pk):
        queryset = Comment.objects.filter(post_id=post_pk)
        return Response(CommentSerializer(queryset, context={'user': request.user}, many=True).data)



