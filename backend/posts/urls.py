from django.urls import path, include
from rest_framework_nested import routers
from .views import PostViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls))
]
