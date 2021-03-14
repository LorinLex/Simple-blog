from django.urls import path, include
from rest_framework import routers
from .views import Dislike, Like, PostViewSet

router = routers.DefaultRouter()

router.register('', PostViewSet)

urlpatterns = [
    path('<int:pk>/like', Like.as_view()),
    path('<int:pk>/dislike', Dislike.as_view()),
    path('', include(router.urls))
]

# urlpatterns += router.urls