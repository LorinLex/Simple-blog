from django.urls import path, include
# from rest_framework import routers
from .views import PostList, PostDetail, Like

# router = routers.DefaultRouter()

# router.register('/', PostsView)

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('<int:pk>/like', Like.as_view()),
    path('<int:pk>/dislike', Like.as_view()),
]