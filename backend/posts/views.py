from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from .serializers import PostDetailSerializer, PostListSerializer
from .models import Post, Tag
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from operator import and_
from functools import reduce

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    serializers = {
        'list': PostListSerializer,
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializers.get(self.action, self.serializer_class)
        return super(PostViewSet, self).get_serializer_class()

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

    @action(methods=['get'], detail=False,
            url_path='tag', url_name='posts_with_tag')
    def posts_with_tag(self, request):
        tag_names = request.query_params.get('tags').split(',')
        tags = Tag.objects.filter(name__in=tag_names)
        posts = Post.objects
        for tag in tags:
            posts = posts.filter(tags_id=tag)
        return Response(PostListSerializer(
            posts,
            many=True,
            context={'user': request.user}
        ).data)

