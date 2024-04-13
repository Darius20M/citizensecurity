
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from security.permissions import AppAuthenticatedPermission, AppStaffPermission
from security.serializers import ResendCodeSerializer


class ResendCodeViewSet(GenericAPIView):
    serializer_class = ResendCodeSerializer
    permission_classes = (
        AppAuthenticatedPermission,
        AppStaffPermission,
    )
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({"detail": "Verification code resent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
