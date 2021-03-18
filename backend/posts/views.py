from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .serializers import PostDetailSerializer, PostListSerializer
from .models import Post, Tag
from users.permissions import IsAuthorOrAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrAdminOrReadOnly]
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

    @action(methods=['post'], detail=True,
            url_path='like', url_name='post_like')
    def like(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        response_status = status.HTTP_204_NO_CONTENT
        try:
            post.likes.get(pk=request.user.id)
            post.likes.remove(request.user.id)
        except settings.AUTH_USER_MODEL.DoesNotExist:
            post.likes.add(request.user.id)
            post.dislikes.remove(request.user.id)
            response_status = status.HTTP_201_CREATED
        finally:
            post.save()
            return Response(status=response_status)

    @action(methods=['post'], detail=True,
            url_path='dislike', url_name='post_dislike')
    def dislike(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        response_status = status.HTTP_204_NO_CONTENT
        try:
            post.dislikes.get(pk=request.user.id)
            post.dislikes.remove(request.user.id)
        except settings.AUTH_USER_MODEL.DoesNotExist:
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

