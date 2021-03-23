from django.urls import path, include
from rest_framework_nested import routers
from .views import UserListViewSet, UserDetailViewSet, UserMeMethodsViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'users', UserListViewSet)

router.register(r'user', UserDetailViewSet)

router.register(r'user/me', UserMeMethodsViewSet, basename='User')


urlpatterns = [
    path('', include(router.urls))
]