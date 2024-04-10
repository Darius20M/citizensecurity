from rest_framework import permissions


class UserAdminPermission(permissions.BasePermission):
    message = 'User does not have enough privileges to access this resource.'

    def has_permission(self, request, view):
        return request.user.is_superuser

