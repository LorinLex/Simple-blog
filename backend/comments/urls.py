from .views import CommentViewSet
from rest_framework import renderers
from django.urls import path, include
from rest_framework import routers as default_routers
from rest_framework_nested import routers
from posts.urls import router as post_router


router = routers.NestedDefaultRouter(post_router, r'posts', lookup='post')

router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls))
]