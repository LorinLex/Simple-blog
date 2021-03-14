from .views import CommentViewSet
from rest_framework import renderers
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

router.register('', CommentViewSet)

urlpatterns = []

urlpatterns += router.urls