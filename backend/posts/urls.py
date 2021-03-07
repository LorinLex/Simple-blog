from django.urls import path, include
from rest_framework import routers
from .views import PostsView

# router = routers.DefaultRouter()

# router.register('/', PostsView)

urlpatterns = [
    path('', PostsView.as_view()),
]