
from allauth.account.models import EmailAddress

from django.utils.translation import gettext_lazy as _
from rest_framework import status

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from security.serializers import ResendEmailVerificationSerializer


class ResendEmailVerificationViewSet(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResendEmailVerificationSerializer
    queryset = EmailAddress.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        if not email.verified:
            email.send_confirmation(request)
            return Response({'detail': _('Email verification has been sent to your email')}, status=status.HTTP_200_OK)
        else :
            return Response({'detail': _('Email already verified')}, status=status.HTTP_400_BAD_REQUEST)

