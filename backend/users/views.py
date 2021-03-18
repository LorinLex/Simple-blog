from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from users.permissions import IsAuthorOrAdminOrReadOnly
from users.serializers import UserSerializer, UserDetailSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    serializer_class = UserDetailSerializer
    serializers = {
        'list': UserSerializer,
        'retrieve': UserDetailSerializer,
    }


    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializers.get(self.action, self.serializer_class)
        return super(UserViewSet, self).get_serializer_class()
