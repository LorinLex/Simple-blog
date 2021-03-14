from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import PostSerializer
from .models import Post, Tag
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets

# Create your views here.

def get_object(pk, model=Post):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        context.update({'user': self.request.user})
        return context


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
