from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from security.models import ApplicationModel
from security.paginations import StandardResultsSetPagination
from security.permissions import AppAuthenticatedPermission, AppStaffPermission
from security.serializers import ApplicationSerializer


class ApplicationViewSet(ModelViewSet):
    permission_classes = [
        AppAuthenticatedPermission,
        AppStaffPermission,
        IsAuthenticated
    ]
    serializer_class = ApplicationSerializer
    queryset = ApplicationModel.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)

