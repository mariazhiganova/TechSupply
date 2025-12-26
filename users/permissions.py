from rest_framework import permissions


class IsActiveUser(permissions.BasePermission):
    """
    Разрешение только для активных пользователей.
    Использует стандартное поле is_active.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
