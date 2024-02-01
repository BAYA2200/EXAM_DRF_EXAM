from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class NewsPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить GET, HEAD, OPTIONS запросы (чтение записи всем)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить PUT, PATCH, DELETE запросы только автору записи
        return obj.author == request.user


class IsAdminUserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff == True:
            return True
        else:
            return False
