from django.urls import path, include
from rest_framework import routers
from .views import UserSerializer, UserDetailSerializer

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'users', UserSerializer.as_view({
    'get': 'list',
}))
router.register(r'user', UserDetailSerializer.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
}))
