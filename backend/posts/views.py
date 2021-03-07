from django.shortcuts import render
from .serializers import PostSerializer
from .models import Post
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json

# Create your views here.

class PostsView(APIView):
    def get(self, request):
        # all posts
        queryset = Post.objects.all()
        print(request.user)
        return Response(PostSerializer(queryset, many=True).data)

    # @swagger_auto_schema(method='post', manual_parameters=[title, text])
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        pass

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=request.data['post_id'])
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)