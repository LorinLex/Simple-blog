from django.urls import path, include
from rest_framework import routers
from .views import PostList, PostDetail

# router = routers.DefaultRouter()

# router.register('/', PostsView)

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
]