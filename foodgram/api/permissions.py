from rest_framework import permissions, status
from rest_framework.exceptions import APIException


class AnonForbidden(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user
                or request.user.is_admin)


class IsAuthUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated):
            return True
        raise AnonForbidden
