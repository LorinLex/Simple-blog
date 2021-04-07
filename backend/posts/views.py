from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .serializers import PostDetailSerializer, PostListSerializer
from .models import Post, Tag
from users.permissions import IsAuthorOrAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated,\
    IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.db.models import Count, Case, When, BooleanField, Q, Subquery

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    queryset_list = Post.objects.annotate(
        likes_count=Count('likes'),
        dislikes_count=Count('dislikes'),
    )
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

    # def get_queryset(self):
    #     if self.action == 'list':
    #         return self.queryset_list
    #     return self.queryset

    def list(self, request, *args, **kwargs):
        """
        List переопределен для использования аннотации с id пользователя
        """
        # FIXME: make False for anon without query
        user_id = request.user.id if not request.user.is_anonymous else 0
        queryset = Post.objects.annotate(
            likes_count=Count('likes'),
            dislikes_count=Count('dislikes'),
            is_liked=Case(
                When(likes__exact=request.user.id, then=True),
                default=False,
                output_field=BooleanField()
            ),
            is_disliked=Case(
                When(dislikes__exact=user_id, then=True),
                default=False,
                output_field=BooleanField()
            ),
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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

