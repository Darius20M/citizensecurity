from rest_framework import permissions


class AppSecretValidatedPermission(permissions.BasePermission):
    message = 'App Secret of invalid application.'

    def has_permission(self, request, view):
        return request.application.client_secret == request.data.get('app_secret', '')
