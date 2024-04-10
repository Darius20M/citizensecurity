from rest_framework import permissions


class AppAuthenticatedPermission(permissions.BasePermission):
    message = 'Unrecognized client application.'

    def has_permission(self, request, view):
        return request.application is not None
