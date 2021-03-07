from django.shortcuts import render
from .serializers import PostSerializer
from .models import Post
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json

# Create your views here.

class PostList(APIView):
    def get(self, request):
        # all posts
        queryset = Post.objects.all()
        return Response(PostSerializer(queryset, many=True, context={'user': request.user}).data)

    # @swagger_auto_schema(method='post', manual_parameters=[title, text])
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        obj = self.get_object(pk)
        # print(request.user)
        return Response(PostSerializer(obj, many=False).data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = PostSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
