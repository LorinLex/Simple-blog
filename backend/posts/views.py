from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import PostSerializer
from .models import Post, Tag
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.

def get_object(pk):
    try:
        return Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class PostList(APIView):
    def get(self, request):
        # all posts
        queryset = Post.objects.all()
        return Response(PostSerializer(queryset, many=True, context={'user': request.user}).data)

    # @swagger_auto_schema(method='post', manual_parameters=[title, text])
    def post(self, request):
        # tags = []
        # for tag_name in request.data['tags']:
        #     obj, created = Tag.objects.get_or_create(name=tag_name)
        #     tags.append(obj)
        # print(tags)
        tags_string = request.data.pop('tags')
        tags = [ {'name': tag} for tag in tags_string]
        serializer = PostSerializer(data={**request.data, 'tags_id': tags}, context={'user': request.user})
        # it = iter(request.data['tags'])
        if serializer.is_valid():
            # serializer.data.tags_id.set(tags)
            serializer.save(author_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    def get(self, request, pk):
        print(request.data)
        obj = get_object(pk)
        return Response(PostSerializer(obj, many=False, context={'user': request.user}).data)

    def put(self, request, pk):
        obj = get_object(pk)
        serializer = PostSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Like(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        obj = get_object(pk)
        try:
            obj.likes.get(pk=request.user.id)
            obj.likes.remove(request.user.id)
            obj.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            obj.likes.add(request.user.id)
            obj.save()
            return Response(status=status.HTTP_201_CREATED)


class Dislike(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        obj = get_object(pk)
        try:
            obj.dislikes.get(pk=request.user.id)
            obj.dislikes.remove(request.user.id)
            obj.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            obj.dislikes.add(request.user.id)
            obj.save()
            return Response(status=status.HTTP_201_CREATED)
