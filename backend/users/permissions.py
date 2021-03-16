from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrAdminOrReadOnly(BasePermission):
    message = 'Only author can change!'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_staff or obj.author_id == request.user


class IsAuthorOrAdmin(BasePermission):
    message = 'Only author can change!'

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.author_id == request.user

