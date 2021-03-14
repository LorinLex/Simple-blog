from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .serializers import PostSerializer
from .models import Post, Tag
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        context.update({'user': self.request.user})
        return context

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='like', url_name='post_like')
    def like(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        response_status = status.HTTP_204_NO_CONTENT
        try:
            post.likes.get(pk=request.user.id)
            post.likes.remove(request.user.id)
        except User.DoesNotExist:
            post.likes.add(request.user.id)
            post.dislikes.remove(request.user.id)
            response_status = status.HTTP_201_CREATED
        finally:
            post.save()
            return Response(status=response_status)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='dislike', url_name='post_dislike')
    def dislike(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        response_status = status.HTTP_204_NO_CONTENT
        try:
            post.dislikes.get(pk=request.user.id)
            post.dislikes.remove(request.user.id)
        except User.DoesNotExist:
            post.dislikes.add(request.user.id)
            post.likes.remove(request.user.id)
            response_status = status.HTTP_201_CREATED
        finally:
            post.save()
            return Response(status=response_status)

