from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from .permissions import IsAuthorOrAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .serializers import UserListSerializer
from .serializers import UserDetailSerializer
from .models import User
from posts.models import Post, Tag


# Create your views here.

class UserListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetailViewSet(viewsets.GenericViewSet,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    serializer_class = UserDetailSerializer

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated],
            url_name='user_me')
    def me(self, request):
        return Response(self.get_serializer_class()(request.user).data)

    @action(methods=['put'], url_path='me/update', url_name='user_me_update', detail=False, permission_classes=[IsAuthenticated])
    def profile_update(self, request):
        instance = User.objects.get(id=request.user.id)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(request.data)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, pk):
        # TODO: may be the error for likes from same users
        get_object_or_404(User, pk=pk).likes.add(request.user)
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def unlike(self, request, pk):
        get_object_or_404(User, pk=pk).likes.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def dislike(self, request, pk):
        # TODO: may be the error for dislikes from same users
        get_object_or_404(User, pk=pk).dislikes.add(request.user)
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def undislike(self, request, pk):
        get_object_or_404(User, pk=pk).dislikes.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk):
        request.user.subscribe_users.add(get_object_or_404(User, pk=pk))
        return Response(UserDetailSerializer(request.user).data, status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def unsubscribe(self, request, pk):
        request.user.subscribe_users.remove(get_object_or_404(User, pk=pk))
        return Response(UserDetailSerializer(request.user).data, status.HTTP_204_NO_CONTENT)



class UserMeMethodsViewSet(viewsets.GenericViewSet):
    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def subscribe_tag(self, request):
        request.user.subscribe_tags.add(*Tag.objects.filter(name__in=request.tags_id))
        return Response(UserDetailSerializer(request.user).data, status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def unsubscribe_tag(self, request):
        request.user.subscribe_tags.remove(*Tag.objects.filter(name__in=request.tags_id))
        return Response(UserDetailSerializer(request.user).data, status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def add_favourite_post(self, request):
        print(request.data)
        posts = Post.objects.filter(pk__in=request.data['post_id'])
        request.user.favourite_posts.add(*posts)
        return Response(UserDetailSerializer(
                request.user,
                context={'user': request.user}).data,
            status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def remove_favourite_post(self, request):
        posts = Post.objects.filter(pk__in=request.data['post_id'])
        request.user.favourite_posts.remove(*posts)
        return Response(UserDetailSerializer(
                request.user,
                context={'user': request.user}).data,
            status.HTTP_204_NO_CONTENT)

    @action(methods=['delete'], detail=False, permission_classes=[IsAuthenticated])
    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
