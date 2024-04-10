from rest_framework import permissions


class AppStaffPermission(permissions.BasePermission):
    message = 'Client application does not have enough privileges to access this resource.'

    def has_permission(self, request, view):
        return request.application.is_staff
