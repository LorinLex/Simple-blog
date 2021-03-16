from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from .models import Comment
from posts.models import Post
from .serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Create your views here.

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_serializer_context(self):
        context = super(CommentViewSet, self).get_serializer_context()
        context.update({'user': self.request.user})
        return context

    def list(self, request, post_pk):
        queryset = Comment.objects.filter(post_id=post_pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(
                CommentSerializer(page, context={'user': request.user}, many=True).data
            )
        return Response(CommentSerializer(
            queryset, context={'user': request.user}, many=True
        ).data)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='like', url_name='comment_like')
    def like(self, request, post_pk, pk):
        comment = get_object_or_404(Post, pk=pk)
        response_status = status.HTTP_204_NO_CONTENT
        try:
            comment.likes.get(pk=request.user.id)
            comment.likes.remove(request.user.id)
        except User.DoesNotExist:
            comment.likes.add(request.user.id)
            comment.dislikes.remove(request.user.id)
            response_status = status.HTTP_201_CREATED
        finally:
            comment.save()
            return Response(status=response_status)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='dislike', url_name='comment_dislike')
    def dislike(self, request, post_pk, pk):
        comment = get_object_or_404(Post, pk=pk)
        response_status = status.HTTP_204_NO_CONTENT
        try:
            comment.dislikes.get(pk=request.user.id)
            comment.dislikes.remove(request.user.id)
        except User.DoesNotExist:
            comment.dislikes.add(request.user.id)
            comment.likes.remove(request.user.id)
            response_status = status.HTTP_201_CREATED
        finally:
            comment.save()
            return Response(status=response_status)
