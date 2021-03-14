from django.urls import path, include
from rest_framework import routers as default_routers
from rest_framework_nested import routers
from .views import Dislike, Like, PostViewSet

router = routers.DefaultRouter()

router.register(r'posts', PostViewSet)

urlpatterns = [
    path('posts/<int:pk>/like', Like.as_view()),
    path('posts/<int:pk>/dislike', Dislike.as_view()),
    path('', include(router.urls))
]
